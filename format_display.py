from modele import User


def format_menu_title(text):
    print(f"""\n====== {text} ======""")


def format_message(message):
    sender = User.get_by_id(message.from_id)
    text = f"> {sender.username} ({message.creation_date}): {message.text}"
    return text
