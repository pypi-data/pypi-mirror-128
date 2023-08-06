from cosmics import repository
from cosmics.testing.fakes.domain import model
from cosmics.testing.fakes.repository import database


class FakeRepository(repository.AbstractRepository):
    _target = "test_target"
    _model: model.FakeModel = model.FakeModel

    def __init__(self, client: database.FakeClient):
        self.contains = client.contains
        super().__init__(client)
