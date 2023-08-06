from cosmics.service_layer import unit_of_work
from cosmics.testing.fakes.repository import FakeRepository


class FakeUnitOfWork(unit_of_work.UnitOfWork):
    pass


class FakeDatabaseUnitOfWork(unit_of_work.DatabaseUnitOfWork):
    repository: FakeRepository

    def _initialize_repositories(self) -> None:
        self.repository = FakeRepository(self._client)
