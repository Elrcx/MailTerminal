from datetime import datetime

from tools import execute_query
from modele import User, Message, Selection
from local_settings import admin_password
from format_display import format_message, format_menu_title


current_user = None


def user_login_menu():
    global current_user
    login = input("Wpisz login: ")
    password = input("Wpisz hasło: ")
    user = None
    try:
        user = User.get_by_username(login)
    except:
        pass
    if user is not None and user.password == password:
        current_user = user
        user_menu()
    else:
        print("Nieprawidłowy login lub hasło.")
        main_menu()


def user_menu():
    print(format_menu_title(f"Witaj {current_user.username}"))

    selections = [
        Selection(user_show_received_messages, "Skrzynka odbiorcza"),
        Selection(user_show_sent_messages, "Skrzynka nadawcza"),
        Selection(user_send_message, "Wyślij nową wiadomość"),
        Selection(user_change_data, "Zmień dane konta")
    ]

    Selection.display_menu(selections)
    Selection.execute_input(selections, main_menu)


def user_show_received_messages():
    global current_user
    user_id = current_user.id()
    messages = Message.get_by_receiver_id(user_id)
    for message in messages:
        print(format_message(message))
    user_menu()


def user_show_sent_messages():
    global current_user
    user_id = current_user.id()
    messages = Message.get_by_sender_id(user_id)
    for message in messages:
        print(format_message(message))
    user_menu()


def user_send_message():
    global current_user
    user_id = current_user.id()
    to_id = input("Wprowadź id odbiorcy: ")
    text = input("Treść wiadomości: ")

    try:
        message = Message(from_id=user_id, to_id=to_id, creation_date=datetime.now(), text=text)
        message.save()

        receiver = User.get_by_id(to_id)
        print(f"Wysłano wiadomość do użytkownika '{receiver.username}'")
    except:
        print("Wystąpił błąd przy wysyłaniu wiadomości.")
    user_menu()


def user_change_data():
    global current_user
    new_username = input(f"Wpisz nową nazwę użytkownika (zostaw puste aby pominąć) [{current_user.username}]: ")
    new_password = input(f"Wpisz nowe hasło (zostaw puste aby pominąć) [{current_user.password}]: ")

    if len(new_username) > 0:
        if len(new_username) >= 5:
            current_user.username = new_username
            print(f"Zmieniono nazwę użytkownika na {new_username}.")
        else:
            print("Nazwa użytkownika musi mieć przynajmniej 5 znaków!")

    if len(new_password) > 0:
        if len(new_password) >= 8:
            current_user.password = new_password
            print(f"Zmieniono hasło użytkownika na {new_password}.")
        else:
            print("Hasło użytkownika musi mieć przynajmniej 8 znaków!")

    current_user.save()
    user_menu()


def admin_login_menu():
    login = input("Wpisz login admina: ")
    password = input("Wpisz hasło admina: ")
    if login == "admin" and password == admin_password:
        admin_menu()
    else:
        print("Nieprawidłowy login lub hasło.")
        main_menu()


def admin_menu():
    print(format_menu_title("Menu Administratora"))

    selections = [
        Selection(admin_user_list, "Lista użytkowników"),
        Selection(admin_message_list, "Lista wiadomości")
    ]

    Selection.display_menu(selections)
    Selection.execute_input(selections, main_menu)


def admin_user_list():
    u = User.get_all()
    for user in u:
        print(user)
    admin_menu()


def admin_message_list():
    m = Message.get_all()
    for message in m:
        print(message)
    admin_menu()


def main_menu():
    global current_user
    current_user = None
    print(format_menu_title("Menu Główne"))

    selections = [
        Selection(user_login_menu, "Użytkownicy"),
        Selection(admin_login_menu, "Administrator")]

    Selection.display_menu(selections)
    Selection.execute_input(selections)


if __name__ == '__main__':
    main_menu()
