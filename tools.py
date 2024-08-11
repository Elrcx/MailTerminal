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


def display_menu(text):
    print(f"""====== {text} ======""")