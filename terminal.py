from tools import execute_query, display_menu
from modele import User, Message, Selection
from local_settings import admin_password


def user_login_menu():
    print("user_menu")
    pass


def admin_login_menu():
    login = input("Enter admin login: ")
    password = input("Enter admin password: ")
    if login == "admin" and password == admin_password:
        admin_menu()
    else:
        print("Incorrect login or password.")
        main_menu()


def admin_menu():
    display_menu("Menu Administratora")

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
    display_menu("Menu Główne")

    selections = [
        Selection(user_login_menu, "Użytkownicy"),
        Selection(admin_login_menu, "Administrator")]

    Selection.display_menu(selections)
    Selection.execute_input(selections)


if __name__ == '__main__':
    while True:
        main_menu()
