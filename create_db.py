from tools import execute_query
from modele import User


def create_tables():
    try:
        User.create_table()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    create_tables()
