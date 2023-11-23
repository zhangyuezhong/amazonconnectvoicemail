
from aws_lambda_powertools.utilities.typing import LambdaContext
from lex.lex_event import LexEvent
import lex.lex_helper


class LexIntentRouter:
    def __init__(self):
        self.intent_handlers = {}

    def handle_intent(self, intent_name):
        def decorator(handler_func):
            self.intent_handlers[intent_name] = handler_func
            return handler_func
        return decorator

    def resolve(self, event: LexEvent, context):
        intent_name = event.get_intent_name()
        handler_func = self.intent_handlers.get(intent_name)

        if handler_func:
            return handler_func(event, context)
        else:
            return self.handle_default_intent(event, context)

    def handle_default_intent(self, event: LexEvent, context):
        message = "I'm sorry, I don't know how to handle that request."
        return lex.lex_helper.close(event, event.get_session_attributes(), "Fulfilled", message)
