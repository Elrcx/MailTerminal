from modele import User, Message, Selection
from local_settings import admin_password
from format_display import format_message_from, format_message_to, format_menu_title
from commands import send_message, change_credentials, register_user, delete_user, check_credentials, print_user_list, received_messages_by_id
import argparse


current_user = None
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--list", help="Lista użytkowników", action="store_true")
parser.add_argument("-c", "--create", help="Stwórz użytkownika (musi być podane razem z -u i -p", action="store_true")
parser.add_argument("-u", "--username", help="Nazwa użytkownika")
parser.add_argument("-p", "--password", help="Hasło użytkownika")
parser.add_argument("-d", "--delete", help="Po zalogowaniu, usuwanie użytkownika", action="store_true")
parser.add_argument("-e", "--edit", help="Po zalogowaniu, edycja użytkownika", action="store_true")
parser.add_argument("-n", "--new_pass", help="Nowe hasło (po włączeniu edycji)")
parser.add_argument("-m", "--messages", help="Po zalogowaniu, wyświetla listę wiadomości do użytkownika", action="store_true")


def user_submenu():
    print(format_menu_title("Użytkownicy"))

    selections = [
        Selection(user_login_menu, "Zaloguj się"),
        Selection(user_register_menu, "Zarejestruj nowego użytkownika")]

    Selection.display_menu(selections)
    Selection.execute_input(selections, main_menu)


def user_register_menu():
    global current_user
    username = input("Wpisz nazwę użytkownika: ")
    password = input("Wpisz hasło: ")

    user = register_user(username, password)
    if user is None:
        print("Wystąpił błąd przy rejestracji!")
        user_submenu()
    else:
        print("Użytkownik pomyślnie utworzony!")
        current_user = user
        user_menu()


def user_login_menu():
    global current_user
    login = input("Wpisz login: ")
    password = input("Wpisz hasło: ")
    user = check_credentials(login, password)
    if user is not None:
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
        Selection(user_change_credentials, "Zmień dane konta"),
        Selection(user_delete_account, "Usuń konto")
    ]

    Selection.display_menu(selections)
    Selection.execute_input(selections, main_menu)


def user_show_received_messages():
    global current_user
    user_id = current_user.id()
    received_messages_by_id(user_id)
    print()
    input("Naciśnij ENTER aby wrócić.")
    user_menu()


def user_show_sent_messages():
    global current_user
    user_id = current_user.id()
    messages = Message.get_by_sender_id(user_id)
    print()
    print("Wysłane wiadomości (najnowsze na dole):")
    print()
    for message in messages:
        print(format_message_to(message))
    print()
    input("Naciśnij ENTER aby wrócić.")
    user_menu()


def user_send_message():
    global current_user
    user_id = current_user.id()
    to_id = input("Wprowadź id odbiorcy: ")
    text = input("Treść wiadomości: ")

    send_message(user_id, to_id, text)
    user_menu()

def user_change_credentials():
    global current_user
    new_username = input(f"Wpisz nową nazwę użytkownika (zostaw puste aby pominąć) [{current_user.username}]: ")
    new_password = input(f"Wpisz nowe hasło (zostaw puste aby pominąć) [{current_user.password}]: ")

    change_credentials(current_user, new_username, new_password)
    user_menu()


def user_delete_account():
    global current_user
    confirmation = input("Czy na pewno chcesz usunąć konto? [t/n]: ")
    if confirmation.lower() == "t":
        delete_user(current_user)
        print("Użytkownik został usunięty.")
        main_menu()
    else:
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
    print_user_list()
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
        Selection(user_submenu, "Użytkownicy"),
        Selection(admin_login_menu, "Administrator")]

    Selection.display_menu(selections)
    Selection.execute_input(selections)


def parse_provided_arguments(args):
    global current_user
    if args.list is True:
        print_user_list()
        return None
    if args.create is True:
        user = register_user(args.username, args.password)
        if user is None:
            print("Wystąpił błąd przy rejestracji!")
        else:
            print("Użytkownik pomyślnie utworzony!")
        return None

    user = check_credentials(args.username, args.password)
    if user is not None:
        current_user = user
        perform_action_from_arguments(args)
    else:
        parser.print_help()


def perform_action_from_arguments(args):
    global current_user
    user_id = current_user.id()
    if args.edit is True:
        if len(args.new_pass) > 8:
            current_user.password = args.new_pass
            current_user.save()
            print("Hasło zmienione pomyślnie!")
        else:
            print("Hasło musi mieć przynajmniej 8 znaków!")
    if args.delete is True:
        current_user.delete()
        print("Użytkownik usunięty.")
    if args.messages is True:
        received_messages_by_id(user_id)


if __name__ == '__main__':
    args = parser.parse_args()
    if args.username is None and args.list is False:
        main_menu()
    else:
        parse_provided_arguments(args)
