from typing import Any
from typing import Optional

from cosmics.repository import database


class FakeClient(database.AbstractClient):
    def __init__(self, contains: dict[str, list[dict[str, Any]]]):
        self.contains = contains

    def __del__(self, commit: bool = False):
        pass

    def _insert(self, target: str, data: database.Info) -> None:
        self.contains[target].append(data)

    def _select(
        self,
        target: str,
        where: Optional[database.Info],
    ) -> list[database.Info]:
        if where is None:
            return self.contains[target]
        return [d for d in self.contains[target] if _all_values_match(d, where)]

    def _update(
        self,
        target: str,
        data: database.Info,
        where: database.Info,
    ) -> None:
        self.contains[target] = [
            d if not _all_values_match(d, where) else _update_dict(d, data)
            for d in self.contains[target]
        ]

    def _delete(self, target: str, where: database.Info) -> None:
        self.contains[target] = [
            d for d in self.contains[target] if not _all_values_match(d, where)
        ]


def _all_values_match(left: dict, right: dict) -> bool:
    return all(left[k] == v for k, v in right.items())


def _update_dict(target: dict, updates: dict) -> dict:
    for k, v in updates.items():
        if k in target:
            target[k] = v
    return target
