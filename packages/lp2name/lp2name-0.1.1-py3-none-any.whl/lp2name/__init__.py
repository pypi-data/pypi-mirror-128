from lp2name.models import *


class User:
    def __init__(
        self,
        db,
        uuid,
        username) -> None:
        self.db = db
        self.uuid = uuid
        self.username = username


class LuckPerms:
    def __init__(
        self,
        database: DB,
        columns: Columns = Columns(),
    ):
        self.db = database.database
        self.columns = columns
        self.model: list[str] = []
        self.describe_table()

    def describe_table(self):
        with self.db.cursor() as cursor:
            cursor.execute(f"DESCRIBE {self.columns.table}")
            result = cursor.fetchall()
            for i in result:
                self.model.append(i[0])

    def get_user_by_name(self, name: str):
        name = name.lower()
        with self.db.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM `{self.columns.table}` WHERE `{self.columns.username}` = %s",
                [name],
            )
            result = cursor.fetchall()
            result = result[0]
            return User(
                db=self,
                uuid=result[0],
                username=name)
    
    def get_user_by_uuid(self, uuid: str):
        uuid = uuid.lower()
        with self.db.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM `{self.columns.table}` WHERE `{self.columns.uuid}` = %s",
                [uuid],
            )
            result = cursor.fetchall()
            result = result[0]
            return User(
                db=self,
                uuid=uuid,
                username=result[1])
