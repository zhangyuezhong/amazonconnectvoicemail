from aws_lambda_powertools.utilities.typing import LambdaContext
import uuid
import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, "src"
)
sys.path.append(SOURCE_PATH)


class MockContext(LambdaContext):
    def __init__(self, name: str, version: int = 1, region: str = "ap-southeast-2", account_id: str = "111122223333"):
        self._function_name = name
        self._function_version = str(version)
        self._memory_limit_in_mb = 128
        self._invoked_function_arn = f"arn:aws:lambda:{region}:{account_id}:function:{name}:{version}"
        self._aws_request_id = str(uuid.uuid4())
        self._log_group_name = f"/aws/lambda/{name}"
        self._log_stream_name = str(uuid.uuid4())

# load_test_data_from file
# the filename can be
# 1  absolution file path
# 2  a sub directory path of the current folder, e.g  tests/data/file.json
# 3  or file.json ,  it will lookup file at cwd()/tests/data/file.json


def load_test_data_from(filename):
    normalized_filename = os.path.normpath(filename)
    if os.path.isabs(normalized_filename) and os.path.exists(normalized_filename):
        file_path = normalized_filename
    else:
        if os.path.sep in normalized_filename:
            if normalized_filename.startswith(os.path.sep):
                normalized_filename = normalized_filename[1:]
            file_path = os.path.join(os.getcwd(), normalized_filename)
        else:
            file_path = os.path.join(os.getcwd(), "tests", "data", filename)

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
