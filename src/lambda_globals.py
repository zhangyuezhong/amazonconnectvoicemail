import os
import tempfile


def get_s3_bucket_name():
    return os.getenv("OUTPUT_S3_BUCKET_NAME")


def get_s3_key_prefix():
    return os.getenv("OUTPUT_S3_KEY_PREFIX")


def get_s3_presigned_url_expires_in():
    return os.getenv("OUTPUT_S3_PRESIGNED_URL_EXPIRES_IN")


def get_whisper_download_root():
    download_root = os.getenv("WHISPER_DOWNLOAD_ROOT")
    if (download_root is None):
        if (os.getenv("LAMBDA_TASK_ROOT")):
            return tempfile.gettempdir()
        else:
            return None
    else:
        return download_root


def get_whisper_model_name():
    model_name = os.getenv("WHISPER_MODEL_NAME")
    _MODELS = ["tiny.en", "tiny", "base.en", "base", "small.en", "small",
               "medium.en", "medium", "large-v1", "large-v2", "large-v3", "large"]
    if (model_name in _MODELS):
        return model_name
    return "base.en"


def get_whisper_preload_model_in_memory():
    return os.getenv("WHISPER_PRELOAD_MODEL_IN_MEMORY", "False").lower() == 'true'


def get_from_email():
    return os.getenv("FROM_EMAIL")


def get_to_email():
    return os.getenv("TO_EMAIL")


def get_to_teams_channel_webhook():
    return os.getenv("TEAMS_CHANNEL_WEBHOOK")
