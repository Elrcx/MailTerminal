from modele import User


def format_menu_title(text):
    row_length = len(text) + 4 + 10
    formatted_text = ""
    for i in range(row_length):
        formatted_text += "="
    formatted_text += f"\n====== {text} ======\n"
    for i in range(row_length):
        formatted_text += "="
    return formatted_text


def format_message(message):
    sender = User.get_by_id(message.from_id)
    text = f"> {sender.username} ({message.creation_date}): {message.text}"
    return text
