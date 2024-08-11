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
        Selection(user_show_messages, "Pokaż wiadomości"),
        Selection(None, "Wyślij nową wiadomość"),
        Selection(None, "Zmień dane konta")
    ]

    Selection.display_menu(selections)
    Selection.execute_input(selections, main_menu)


def user_show_messages():
    global current_user
    user_id = current_user.id()
    messages = Message.get_by_receiver_id(user_id)
    for message in messages:
        print(format_message(message))
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
