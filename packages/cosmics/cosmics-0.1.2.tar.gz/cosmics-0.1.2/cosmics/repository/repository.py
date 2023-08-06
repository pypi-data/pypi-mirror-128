from __future__ import annotations

import abc
import logging

import psycopg2.errorcodes
import psycopg2.errors

from cosmics.domain import model
from cosmics.repository import database

logger = logging.getLogger(__name__)

ForeignKeyViolation = psycopg2.errors.lookup(psycopg2.errorcodes.FOREIGN_KEY_VIOLATION)
UniqueViolation = psycopg2.errors.lookup(psycopg2.errorcodes.UNIQUE_VIOLATION)
DatabaseModel = model.AbstractModel


class NotFoundInDatabaseException(Exception):
    """Raised when a requested entry was not found in the database."""


class DuplicateItemException(Exception):
    """An item is a duplicate."""


class ReferenceViolationException(Exception):
    """Item is referenced by another item."""


class AbstractRepository(abc.ABC):
    """Represents an abstract database target.

    Parameters
    ----------
    client : cosmics.database.AbstractClient
        Client for interaction with the database.

    A target can e.g. be a table in an SQL database.

    """

    _target: str
    _model: type[DatabaseModel]

    def __init__(self, client: database.AbstractClient):
        """Initialize the repository."""
        self._client = client
        self.added: list[AbstractRepository._model] = []
        self.fetched: list[AbstractRepository._model] = []
        self.updated: list[AbstractRepository._model] = []
        self.deleted: list[AbstractRepository._model] = []

    @property
    def target(self) -> str:
        """Construct target name."""
        return self._target

    @property
    def items(self) -> list[AbstractRepository._model]:
        """Get all items from the repository."""
        return self.get_all()

    def add(self, item: AbstractRepository._model) -> None:
        """Add item to database.

        Parameters
        ----------
        item : model.AbstractModel
            The item to add.

        """
        logger.debug("Adding to target %s item %s", self.target, item)
        self._add(item)
        self.added.append(item)

    def get(self, identifier: database.Info) -> AbstractRepository._model:
        """Get item as model instance.

        Parameters
        ----------
        identifier : dict
            Identifier by which to select the item(s).

        Raises
        ------
        NotFoundInDatabaseError
            If the respective identifier was not found.

        """
        logger.debug(
            "Trying to get item from target %s by identifier %s",
            self.target,
            identifier,
        )
        match = self._get(identifier)
        item = self._model(**match)
        logger.debug("Found matching item %s for identifier %s", item, identifier)
        self.fetched.append(item)
        return item

    def get_all(self) -> list[AbstractRepository._model]:
        """Get all items as model instances."""
        logger.debug("Getting all items in %s", self.target)
        items = [self._model(**item) for item in self._get_all()]
        self.fetched.extend(items)
        logger.debug("Items are: %s", items)
        return items

    def update(self, item: AbstractRepository._model) -> None:
        """Update item.

        Parameters
        ----------
        item : model.AbstractModel
            The item to update.

        """
        logger.debug("Updating item in %s to %s", self.target, item)
        self._update(item)
        self.updated.append(item)

    def delete(self, item: AbstractRepository._model) -> None:
        """Delete item(s).

        Parameters
        ----------
        item : model.AbstractModel
            The item to delete.

        """
        logger.debug("Deleting from target %s item %s", self.target, item)
        self._delete(item)
        self.deleted.append(item)

    def _add(self, item: AbstractRepository._model) -> None:
        with self._client as client:
            try:
                client.insert(
                    target=self.target,
                    data=item.to_dict(),
                )
            except UniqueViolation as e:
                raise DuplicateItemException(f"{item} is a duplicate:\n{e}")

    def _get(self, identifier: database.Info) -> database.Info:
        with self._client as client:
            try:
                [match] = client.select(target=self.target, where=identifier)
            except ValueError:
                raise NotFoundInDatabaseException(
                    "No entry in target %s with identifier(s) %s",
                    self.target,
                    identifier,
                )
            else:
                return match

    def _get_all(self) -> list[database.Info]:
        with self._client as client:
            return client.select(target=self.target)

    def _update(self, item: AbstractRepository._model) -> None:
        with self._client as client:
            client.update(
                target=self.target,
                data=item.to_dict(),
                where=item.identifier,
            )

    def _delete(self, item: AbstractRepository._model) -> None:
        with self._client as client:
            try:
                client.delete(
                    target=self.target,
                    where=item.identifier,
                )
            except ForeignKeyViolation as e:
                raise ReferenceViolationException(
                    f"{item} cannot be deleted because it is still referenced "
                    f"by at least one database entry:\n{e}"
                )
