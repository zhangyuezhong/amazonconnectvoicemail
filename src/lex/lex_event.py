
from functions import get


class LexEvent:
    def __init__(self, event: dict):
        self.event = event

    def get_invocation_source(self):
        return get(self.event, "invocationSource", None)

    def get_session_id(self):
        return get(self.event, "sessionId", None)

    def get_response_content_type(self):
        return get(self.event, "responseContentType", None)

    def get_input_transcript(self):
        return get(self.event, "inputTranscript", None)

    def get_invocation_label(self):
        return get(self.event, "invocationLabel", None)

    def get_bot(self):
        return get(self.event, "bot", {})

    def get_interpretations(self):
        return get(self.event, "interpretations", {})

    def get_proposed_next_state(self):
        return get(self.event, "proposedNextState", {})

    def get_request_attributes(self):
        return get(self.event, "requestAttributes", {})

    def get_session_state(self):
        return get(self.event, "sessionState", {})

    def get_session_attributes(self) -> dict:
        return get(self.event, "sessionState.sessionAttributes", {})

    def get_session_attribute(self, name, default_value=None):
        return get(self.event, f"sessionState.sessionAttributes.{name}", default_value)
    
    def get_dialog_action(self):
        return get(self.event, "sessionState.dialogAction", {})

    def get_intent(self):
        return get(self.event, "sessionState.intent", {})

    def get_intent_name(self):
        return get(self.event, "sessionState.intent.name", None)

    def get_slots(self):
        return get(self.event, "sessionState.intent.slots")

    def get_slot_value(self, slotName):
        return get(self.event, f"sessionState.intent.slots.{slotName}.value.interpretedValue", None)

    def get_transcriptions(self):
        return get(self.event, "transcriptions", {})

    def to_dict(self):
        return self.event
