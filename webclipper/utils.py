def remove_spaces(text: str):
    text = " ".join(text.split())
    return text


def is_valid_string(text: str):
    result = text and not text.isspace()
    return result
