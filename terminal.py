from tools import execute_query
from modele import User, Message, Selection


def user_menu():
    print("user_menu")
    pass


def message_menu():
    print("message_menu")
    pass


def admin_menu():
    print("admin_menu")
    pass


def main_menu():
    text = ""
    text += f"Menu Główne\n"

    selections = [
        Selection(message_menu, "Wiadomości"),
        Selection(user_menu, "Użytkownicy"),
        Selection(admin_menu, "Administrator")]

    Selection.display_menu(selections)
    Selection.execute_input(selections)


if __name__ == '__main__':
    while True:
        main_menu()
