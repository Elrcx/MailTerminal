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


def register_user(new_username, new_password):
    if len(new_username) < 5:
        print("Nazwa użytkownika musi mieć przynajmniej 5 znaków!")
        return None

    if len(new_password) < 8:
        print("Hasło użytkownika musi mieć przynajmniej 8 znaków!")
        return None

    if User.get_by_username(new_username) is not None:
        print("Użytkownik o takiej nazwie już istnieje!")
        return None

    user = User(username=new_username, password=new_password)
    user.save()
    return user


def delete_user(user):
    user.delete()


def send_message(user_id, to_id, text):
    try:
        message = Message(from_id=user_id, to_id=to_id, creation_date=datetime.now(), text=text)
        message.save()

        receiver = User.get_by_id(to_id)
        print(f"Wysłano wiadomość do użytkownika '{receiver.username}'")
    except:
        print("Wystąpił błąd przy wysyłaniu wiadomości.")
