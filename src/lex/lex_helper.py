from functions import get, to_e164_number, is_empty
from lex.lex_event import LexEvent


def close(event: LexEvent, session_attributes, fulfillment_state, message):
    intent = event.get_intent()
    intent['state'] = fulfillment_state
    session_id = event.get_session_id()
    message = _text_message(message)
    requestAttributes = event.get_request_attributes()
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent
        },
        'messages': message,
        'sessionId': session_id,
        'requestAttributes': requestAttributes
    }


def elicit_intent(intent_request, session_attributes, message):
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitIntent'
            },
            'sessionAttributes': session_attributes
        },
        'messages': [message] if message != None else None,
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }


def _text_message(message) -> list[dict]:
    if message is None:
        return []
    if (isinstance(message, str)):
        return [{
            'contentType': 'PlainText',
            'content': message
        }]
    if (isinstance(message, list)):
        if all(isinstance(s, str) for s in message):
            return list(map(lambda x: {
                'contentType': 'PlainText',
                'content': x
            }), message)
    if (isinstance(message, dict) and message["contentType"] is not None and message["content"] is not None):
        return [message]

    return []
