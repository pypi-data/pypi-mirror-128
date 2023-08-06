from . import database
from cosmics.repository import postgresql
from cosmics.testing.fakes.repository.repository import FakeRepository


class FakePostgresqlRepository(FakeRepository, postgresql.Repository):
    def __init__(self, client: database.FakePostgresqlClient):
        self.contains = client.contains
        super().__init__(client)
