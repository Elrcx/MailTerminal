from local_settings import database_settings
from psycopg2 import connect


def execute_query(query):
    with connect(**database_settings) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(query)
            try:
                result = cursor.fetchall()
            except:
                result = None
            return result
