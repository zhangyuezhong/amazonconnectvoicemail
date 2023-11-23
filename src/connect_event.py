import functions


def get_contact_id(event: dict):
    return functions.get(event, "Details.ContactData.ContactId")


def get_channel(event: dict):
    return functions.get(event, "Details.ContactData.Channel")


def get_customer_endpoint_address(event: dict):
    return functions.get(event, "Details.ContactData.CustomerEndpoint.Address")


def get_attributes(event: dict):
    return functions.get(event, "Details.ContactData.Attributes", {})


def get_customer_audio_stream_arn(event: dict):
    return functions.get(event, "Details.ContactData.MediaStreams.Customer.Audio.StreamARN", None)


def get_customer_audio_start_fragment_number(event: dict):
    return functions.get(event, "Details.ContactData.MediaStreams.Customer.Audio.StartFragmentNumber", None)


def get_attribute(event: dict, name: str, case_sensitive: bool = False):
    if (functions.is_empty(name)):
        return None
    if (case_sensitive):
        return functions.get(event, "Details.ContactData.Attributes." + name, None)
    else:
        attributes = functions.get(event, "Details.ContactData.Attributes", {})
        return next((value for key, value in attributes.items() if key.lower() == name.lower()), None)


def get_parameters(event: dict):
    return functions.get(event, "Details.Parameters", {})


def get_parameter(event: dict, name: str, case_sensitive: bool = False):
    if (functions.is_empty(name)):
        return None
    if (case_sensitive):
        return functions.get(event, "Details.Parameters." + name, None)
    else:
        parameters = functions.get(event, "Details.Parameters", {})
        return next((value for key, value in parameters.items() if key.lower() == name.lower()), None)
