import os
import json
import boto3
from botocore.client import Config
from functools import lru_cache
from kvs_parser import KVSParser

from connect_event import get_customer_audio_stream_arn
from connect_event import get_customer_audio_start_fragment_number
from bytearray_to_wav import convert_bytearray_to_wav


config = Config(connect_timeout=5, retries={'max_attempts': 0})

kinesis_client = boto3.client('kinesisvideo', config=config)


def get_data_endpoint(stream_arn):
    endpoint_response = kinesis_client.get_data_endpoint(
        StreamARN=stream_arn, APIName='GET_MEDIA')
    return endpoint_response['DataEndpoint']


@lru_cache(maxsize=5)
def get_kinesis_video_client(data_endpoint):
    return boto3.client('kinesis-video-media', endpoint_url=data_endpoint)


def download_kvs_stream(stream_arn, start_fragment_number, output_dir: str):
    data_endpoint = get_data_endpoint(stream_arn)
    kinesis_video_client = get_kinesis_video_client(data_endpoint)
    media_response = kinesis_video_client.get_media(
        StreamARN=stream_arn,
        StartSelector={
            'StartSelectorType': 'FRAGMENT_NUMBER',
            'AfterFragmentNumber': start_fragment_number
        }
    )
    parser = KVSParser(media_response)
    fragments = parser.fragments

    samples = bytearray()
    margin = 4
    for fragment in fragments:
        for block in fragment.simple_blocks:
            samples.extend(block.value[margin:])

    wav = convert_bytearray_to_wav(samples)
    output_file = os.path.join(output_dir, f"{start_fragment_number}.wav")
    with open(output_file, 'wb') as file:
        file.write(wav)
    return output_file
