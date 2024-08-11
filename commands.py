from datetime import datetime
from modele import User, Message


def change_credentials(user, new_username, new_password):
    if len(new_username) > 0:
        if len(new_username) >= 5:
            user.username = new_username
            print(f"Zmieniono nazwę użytkownika na {new_username}.")
        else:
            print("Nazwa użytkownika musi mieć przynajmniej 5 znaków!")

    if len(new_password) > 0:
        if len(new_password) >= 8:
            user.password = new_password
            print(f"Zmieniono hasło użytkownika na {new_password}.")
        else:
            print("Hasło użytkownika musi mieć przynajmniej 8 znaków!")

    user.save()


def send_message(user_id, to_id, text):
    try:
        message = Message(from_id=user_id, to_id=to_id, creation_date=datetime.now(), text=text)
        message.save()

        receiver = User.get_by_id(to_id)
        print(f"Wysłano wiadomość do użytkownika '{receiver.username}'")
    except:
        print("Wystąpił błąd przy wysyłaniu wiadomości.")
