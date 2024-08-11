from local_settings import database_settings
from psycopg2 import connect

def execute_query(query):
    with connect(**database_settings) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            try:
                cursor.execute(query)
                result = cursor.fetchall()
            except Exception as e:
                print(e)
                result = None
            return result


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
