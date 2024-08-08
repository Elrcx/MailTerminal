from datetime import datetime

from tools import execute_query


class User:
    def __init__(self, _id=None, username=None, password=None):
        self._id = _id
        self.username = username
        self.password = password
        pass

    def save(self):
        if self._id is None:
            self._create()
        else:
            self._update()

    def _create(self):
        query = f"""
        INSERT INTO users (username, password)
        values ('{self.username}', '{self.password}')
        returning id;"""
        id = execute_query(query)[0][0]
        self._id = id

    def _update(self):
        query = f"""
        UPDATE users SET
        username = '{self.username}',
        password = '{self.password}'
        WHERE id = {self._id};"""
        execute_query(query)

    def delete(self):
        query = f"""
        DELETE FROM users WHERE id = {self._id};"""
        execute_query(query)
        self._id = None

    @classmethod
    def create_table(cls):
        query = """
            create table users (
                id serial primary key,
                username varchar(255),
                password varchar(80)
            );
        """
        execute_query(query)

    @classmethod
    def get_all(cls):
        query = f"""
        SELECT * FROM users;"""
        users = []
        entries = execute_query(query)
        for entry in entries:
            u = User(*entry)
            users.append(u)
        return users

    @classmethod
    def get_by_id(cls, id):
        query = f"""
        SELECT * FROM users
        WHERE id = {id}
        LIMIT 1;"""
        try:
            entry = execute_query(query)[0]
            u = User(*entry)
        except IndexError:
            u = None
        return u

    @classmethod
    def get_by_username(cls, username):
        query = f"""
        SELECT * FROM users
        WHERE username = '{username}'
        LIMIT 1;"""
        try:
            entry = execute_query(query)[0]
            u = User(*entry)
        except IndexError:
            u = None
        return u

    def __str__(self):
        return f"{self._id} {self.username} {self.password}"


class Message:
    @classmethod
    def create_table(cls):
        query = """
            create table messages (
                id serial primary key,
                from_id int NOT NULL,
                to_id int NOT NULL,
                creation_date timestamp,
                text varchar(255),
                FOREIGN KEY (from_id) REFERENCES users (id),
                FOREIGN KEY (to_id) REFERENCES users (id)
            );
        """
        execute_query(query)

    def __init__(self, id=None, from_id=None, to_id=None, creation_date=None, text=None):
        self._id = id
        self.from_id = from_id
        self.to_id = to_id
        self.creation_date = creation_date
        self.text = text

    @property
    def id(self):
        return self._id

    def save(self):
        query = f"""
        INSERT INTO messages (from_id, to_id, creation_date, text)
        VALUES ({self.from_id}, {self.to_id}, '{self.creation_date}', '{self.text}')
        RETURNING id;"""
        id = execute_query(query)[0][0]
        self._id = id

    @classmethod
    def get_all(cls):
        query = f"""
        SELECT * FROM messages;"""
        messages = []
        entries = execute_query(query)
        for entry in entries:
            m = Message(*entry)
            messages.append(m)
        return messages

    @classmethod
    def get_by_sender_id(cls, id):
        query = f"""
        SELECT * FROM messages
        WHERE from_id = {id};"""
        messages = []
        entries = execute_query(query)
        for entry in entries:
            m = Message(*entry)
            messages.append(m)
        return messages

    @classmethod
    def get_by_receiver_id(cls, id):
        query = f"""
        SELECT * FROM messages
        WHERE to_id = {id};"""
        messages = []
        entries = execute_query(query)
        for entry in entries:
            m = Message(*entry)
            messages.append(m)
        return messages

    def __str__(self):
        return f"{self.from_id} {self.to_id} {self.creation_date} '{self.text}'"


if __name__ == '__main__':
    m = Message.get_by_receiver_id(4)
    for message in m:
        print(message)

