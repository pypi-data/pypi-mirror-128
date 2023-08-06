from cosmics.repository.postgresql import database
from cosmics.testing.fakes.repository.database import FakeClient


class FakePostgresqlClient(FakeClient, database.Client):
    def insert_and_return_row_id(self, target: str, data: dict) -> int:
        return 1
