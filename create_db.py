from tools import execute_query
from modele import User, Message


def create_tables():
    User.create_table()
    Message.create_table()


if __name__ == '__main__':
    create_tables()
