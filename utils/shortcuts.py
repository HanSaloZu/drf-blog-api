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
