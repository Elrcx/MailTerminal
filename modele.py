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
        UPDATE user SET
        username = {self.username},
        password = {self.password}
        WHERE id = {self._id};"""

    def delete(self):
        pass

    @classmethod
    def create_table(cls):
        query = """
                    create table users (
                        id serial primary key,
                        username varchar(255),
                        password varchar(80)
                    );
                """
        pass


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


if __name__ == '__main__':
    u = User(username='Jacek', password='hunter22')
    u.save()
