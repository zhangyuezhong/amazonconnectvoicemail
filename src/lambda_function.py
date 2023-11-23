import os
import tempfile
import functions
import requests
import boto3
import json
import time
from datetime import datetime

from http import HTTPStatus
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from lambda_globals import get_s3_bucket_name, get_s3_key_prefix, get_s3_presigned_url_expires_in
from lambda_globals import get_whisper_download_root, get_whisper_model_name, get_whisper_preload_model_in_memory
from lambda_globals import get_from_email, get_to_email, get_to_teams_channel_webhook

from connect_event import get_parameter, get_customer_endpoint_address, get_customer_audio_stream_arn, get_customer_audio_start_fragment_number
from kvs_stream import download_kvs_stream
from time_converter import convert_time_to_seconds


client = boto3.client('lambda')
s3 = boto3.client('s3')
sesv2 = boto3.client('sesv2')

logger = Logger(service="lambda_handler")

model = None


@logger.inject_lambda_context(log_event=True, clear_state=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    try:
        if (is_asynchronous_invocation(event)):
            return handle_event(event, context)
        else:
            return async_invoke(event, context)
    except Exception as e:
        logger.exception(str(e))
        return functions.to_dict(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))


def is_asynchronous_invocation(event):
    return "InvocationType" in event and event["InvocationType"] == "Event"


def async_invoke(event, context):
    event["InvocationType"] = "Event"
    response = client.invoke(
        FunctionName=context.function_name,
        InvocationType='Event',
        Payload=json.dumps(event)
    )
    return functions.ok()


def handle_event(event, context):
    try:
        output_file = download_kvs_stream_to_file(event)
        text = transcribe_wav_file(output_file)
        logger.info(f"text={text}")
        if (functions.is_not_empty(text)):
            presigned_url = upload_file_to_s3_bucket(output_file)
            send_email_notification(event, text, presigned_url)
            send_teams_channel_notification(event, text, presigned_url)
        else:
            logger.info("transcribe_wav_file text is empty")
        return functions.ok()
    except Exception as e:
        logger.exception(str(e))
        return functions.to_dict(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))


def download_kvs_stream_to_file(event):
    logger.info(f"Begin the download of the KVS stream")
    start_time = time.time()
    stream_arn = get_customer_audio_stream_arn(event)
    start_fragment_number = get_customer_audio_start_fragment_number(event)
    output_dir = tempfile.gettempdir()
    output_file = download_kvs_stream(
        stream_arn, start_fragment_number, output_dir)
    logger.info(
        f"download_kvs_stream time: {time.time() - start_time} seconds , output_file={output_file}")
    return output_file


def upload_file_to_s3_bucket(file):
    try:
        bucket_name = get_s3_bucket_name()
        s3_key_prefix = get_s3_key_prefix()
        if (functions.is_not_empty(bucket_name)):
            filename = os.path.basename(file)
            s3_key = build_s3_key(s3_key_prefix, filename)
            s3.upload_file(file, bucket_name, s3_key)
            expiration_time = get_s3_presigned_url_expires_in()
            expiration_time = safe_call(
                convert_time_to_seconds, expiration_time, default_value=604800)
            presigned_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': s3_key},
                                                      ExpiresIn=expiration_time
                                                      )
            return presigned_url
        else:
            logger.info(f"upload_file_to_s3_bucket bucket_name is empty")
    except Exception as ex:
        logger.error(f"Exception caught: {str(e)}")
    return None


def build_s3_key(s3_key_prefix, key_name):
    if (s3_key_prefix):
        s3_key_prefix = s3_key_prefix.lstrip('/')
        s3_key_prefix = s3_key_prefix.rstrip('/')
        s3_key_prefix = s3_key_prefix.strip()
    if (functions.is_not_empty(s3_key_prefix)):
        return f"{s3_key_prefix}/{key_name}"
    return key_name


def safe_call(func, *args, default_value=None, **kwargs):
    try:
        result = func(*args, **kwargs)
        return result
    except Exception as e:
        logger.error(f"Exception caught: {str(e)}")
        return default_value


def transcribe_wav_file(file):
    global model
    if model is None:
        model_name = get_whisper_model_name()
        download_root = get_whisper_download_root()
        in_memory = get_whisper_preload_model_in_memory()
        initialize_model(name=model_name, device="cpu",
                         download_root=download_root, in_memory=in_memory)
    result = model.transcribe(audio=file, fp16=False, language="en")
    return result["text"] if "text" in result else None


def initialize_model(name="base.en", device="cpu", download_root=None, in_memory=False):
    logger.debug(
        f"initializing the model. name={name}, device={device}, download_root={download_root}, in_memory={in_memory}")
    global model
    start_time = time.time()
    import whisper
    logger.info(f"import whisper time: {time.time()-start_time} seconds")
    start_time = time.time()
    model = whisper.load_model(
        name=name, device=device, download_root=download_root, in_memory=in_memory)
    logger.info(f"whisper.load_model time: {time.time() - start_time} seconds")


def send_email_notification(event, text, presigned_url):
    try:
        from_email = get_from_email()
        if (functions.is_not_empty(from_email)):
            to_email = get_parameter(event, "to_email") or get_to_email()
            if (functions.is_not_empty(to_email)):
                from_phone = get_customer_endpoint_address(event)
                subject = f"Voicemail from {from_phone }"
                response = sesv2.send_email(FromEmailAddress=from_email,
                                            Destination={
                                                "ToAddresses": [to_email]},
                                            Content={
                                                'Simple': {
                                                    'Subject': {
                                                        'Data': subject
                                                    },
                                                    'Body': {
                                                        'Text': {
                                                            'Data': f'{text} \n\n {presigned_url}'
                                                        },
                                                        'Html': {
                                                            'Data': f'<html><head></head><body><p>Date and Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p><p>From: {from_phone}</p><p>{text}</p><p><a href="{presigned_url}" target="_blank">Listen</a></p></body></html>'
                                                        }
                                                    }
                                                }
                                            })
                logger.info("email sent")
            else:
                logger.info("the to email is empty")
        else:
            logger.info("the from email is empty")
    except Exception as ex:
        logger.error(f"Exception caught: {str(e)}")


def send_teams_channel_notification(event, text, presigned_url):
    try:
        webhook_url = get_parameter(
            event, "webhook_url") or get_to_teams_channel_webhook()
        if (functions.is_not_empty(webhook_url)):
            subject = f"Voicemail from { get_customer_endpoint_address(event) }"
            payload = {
                "type": "message",
                "attachments": [
                    {
                        "contentType": "application/vnd.microsoft.card.adaptive",
                        "contentUrl": None,
                        "content": {
                            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                            "type": "AdaptiveCard",
                            "version": "1.2",
                            "body": [
                                {
                                    "type": "TextBlock",
                                    "text": subject,
                                    "wrap": True
                                },
                                {
                                    "type": "TextBlock",
                                    "text": text,
                                    "wrap": True
                                },
                                {
                                    "type": "ActionSet",
                                    "actions": [
                                        {
                                            "type": "Action.OpenUrl",
                                            "title": "Listen",
                                            "url": presigned_url
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ]
            }
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            logger.info("team webhook sent")
        else:
            logger.info("webhook url is empty")
    except Exception as ex:
        logger.error(f"Exception caught: {str(e)}")
