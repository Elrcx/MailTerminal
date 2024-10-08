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


def format_message_from(message):
    sender = User.get_by_id(message.from_id)
    text = f"> Od {sender.username} [ID:{sender.id()}] ({message.creation_date}):\n {message.text}"
    return text


def format_message_to(message):
    receiver = User.get_by_id(message.to_id)
    text = f"> Do {receiver.username} [ID:{receiver.id()}] ({message.creation_date}):\n {message.text}"
    return text
