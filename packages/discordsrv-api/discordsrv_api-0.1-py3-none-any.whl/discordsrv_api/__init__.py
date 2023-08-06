from discordsrv_api.models import *


class User:
    def __init__(
        self,
        db,
        link,
        discord,
        uuid) -> None:
        self.db = db
        self.uuid = uuid
        self.link = link
        self.discord = discord


class DiscordSRV:
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

    def get_discord(self, uuid: str):
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
                link=result[0],
                discord=result[1],
                uuid=result[2])
    
    def get_uuid(self, discord: str):
        with self.db.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM `{self.columns.table}` WHERE `{self.columns.discord}` = %s",
                [discord],
            )
            result = cursor.fetchall()
            result = result[0]
            return User(
                db=self,
                link=result[0],
                discord=result[1],
                uuid=result[2])
