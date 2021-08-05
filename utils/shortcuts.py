from .exceptions import BadRequest400


def generate_messages_list_by_serializer_errors(errors):
    messages = []

    for field_name in errors:
        field_error = errors[field_name]

        if isinstance(field_error, dict):
            messages.extend(
                generate_messages_list_by_serializer_errors(errors[field_name]))
        else:
            message = errors[field_name][0]
            messages.append(message)

    return messages


def raise_400_based_on_serializer(serializer):
    if serializer.is_valid():
        raise ValueError(
            "Can't raise BadRequest400 based on a valid serializer")

    errors = serializer.errors
    messages = generate_messages_list_by_serializer_errors(errors)

    raise BadRequest400(messages, errors)
