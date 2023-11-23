
from http import HTTPStatus
from functools import reduce
import base64
from functools import reduce


def get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)


def is_not_empty(string: str):
    return string is not None and len(string.strip()) > 0


def is_empty(string: str):
    return string is None or len(string.strip()) == 0


def to_dict(httpStatus: HTTPStatus, msg: str = ''):
    return {
        "_status_code": str(httpStatus.value),
        "_status_msg": httpStatus.phrase + ("" if is_empty(msg) else ". " + msg)
    }


def to_http_status(status_code: int):
    for x in list(HTTPStatus):
        if (x.value == status_code):
            return to_dict(x)
    return None


def ok(data: dict = None):
    status = to_dict(HTTPStatus.OK)
    if (data is None):
        return status
    return {**status, **data}  # merge the two dict


def b64decode(base64_message: str):
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message


def b64encode(message: str):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('utf-8')
    return base64_message


def to_e164_number(number: str):
    if (is_empty(number)):
        return ''
    # Geographical areas and Mobile phone numbers
    if (number.startswith('0') and len(number) == 10 and number.isnumeric()):
        return "+61" + number[1:]

    # if number starts with +61
    if (number.startswith("+61") and len(number) == 12 and (number[3:].isnumeric())):
        return number

    # 13 xx xx and 1300 xxx xxx – "Local Rate" calls, except for VoIP and mobile phone users
    if (number.startswith('13') and len(number) == 6 and number.isnumeric()):
        return "+61" + number

    if (number.startswith('1300') and len(number) == 10 and number.isnumeric()):
        return "+61" + number

    # 180 xxxx and 1800 xxx xxx – FreeCall
    if (number.startswith('180') and len(number) == 7 and number.isnumeric()):
        return "+61" + number

    if (number.startswith('1800') and len(number) == 10 and number.isnumeric()):
        return "+61" + number

    # if number starts with +61
    if (number.startswith("+61") and len(number) < 14 and (number[3:].isnumeric())):
        return number

    return ''


def is_mobile_number(number: str):
    number = to_e164_number(number)
    return number and number.startswith("+614")


def random_num():
    return (decimal.Decimal(random.randrange(1000, 50000))/100)


def mask(input_string: str):
    if is_empty(input_string):
        return input_string

    length = len(input_string)
    half_length = length // 2

    masked_string = '*' * half_length + input_string[half_length:]
    return masked_string



