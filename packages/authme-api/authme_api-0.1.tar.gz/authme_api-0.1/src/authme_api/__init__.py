from authme_api.hash_types.sha256 import SHA256
from authme_api.hash_types import HashType
from authme_api.models import *


def find_hash_type(hash_str: str) -> HashType:
    mapping = {"SHA": SHA256}
    spl = hash_str.split("$")
    return mapping[spl[1]]


class AuthMe:
    def __init__(
        self,
        database: DB,
        default_hash: HashType = SHA256,
        columns: Columns = Columns(),
    ):
        self.db = database.database
        self.default_hash = default_hash
        self.columns = columns
        self.model: [str] = []
        self.describe_table()

    def describe_table(self):
        with self.db.cursor() as cursor:
            cursor.execute(f"DESCRIBE {self.columns.table}")
            result = cursor.fetchall()
            for i in result:
                self.model.append(i[0])
        print(self.model)

    def get_user_by_name(self, name: str):
        with self.db.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM {self.columns.table} WHERE {self.columns.Name} = '{name}'"
            )
            result = cursor.fetchall()
            print(result)
