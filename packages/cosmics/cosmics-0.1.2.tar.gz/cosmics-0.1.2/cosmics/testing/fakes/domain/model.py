import dataclasses
from typing import Any
from typing import Union

from cosmics.domain import model


@dataclasses.dataclass(eq=False)
class FakeModel(model.AbstractModel):
    id: int
    test_key: str = "test_value"

    @property
    def _key(self) -> Union[Any, tuple[Any]]:
        return (self.id, self.test_key)

    @property
    def identifier(self) -> dict[str, Any]:
        return {"id": self.id}
