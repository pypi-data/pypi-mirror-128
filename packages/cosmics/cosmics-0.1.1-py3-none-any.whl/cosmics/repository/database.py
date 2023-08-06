import abc
import logging
from typing import Any
from typing import Optional

logger = logging.getLogger(__name__)

Key = str
Value = Any
Info = dict[str, Any]


class AbstractClient(abc.ABC):
    """A client for database interaction."""

    def __enter__(self):
        """Return instance when entering context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection on exit."""
        self.__del__()

    @abc.abstractmethod
    def __del__(self) -> None:
        """Close the connection to the database and delete any other resources."""

    def insert(self, target: str, data: Info) -> None:
        """Insert data into a database target.

        Parameters
        ----------
        target : str
            Target object in which to update an entry.
        data : dict[str, Any]
            Data (entry) to insert into the target.

        """
        logger.debug("Inserting into target %s data %s", target, data)
        self._insert(target=target, data=data)

    @abc.abstractmethod
    def _insert(self, target: str, data: Info) -> None:
        """Insert item into database target."""

    def select(
        self,
        target: str,
        where: Optional[Info] = None,
    ) -> list[Info]:
        """Select data from a target.

        Parameters
        ----------
        target : str
            Target object in which to update an entry.
        where : dict[str, Any], optional
            Criteria for the entry that should be selected.
            Selects all entries in a target by default.

        Returns
        -------
        list[dict[str, Any]]
            All entries matching the criteria.

        """
        logger.debug("Selecting from target %s where %s", target, where)
        return self._select(target=target, where=where)

    @abc.abstractmethod
    def _select(
        self,
        target: str,
        where: Optional[Info],
    ) -> list[Info]:
        """Select data from a database target."""

    def update(
        self,
        target: str,
        data: Info,
        where: Info,
    ) -> None:
        """Update data in a target.

        Parameters
        ----------
        target : str
            Target object in which to update an entry.
        data : dict[str, Any]
            Data to update for a certain entry in a target.
        where : dict[str, Any]
            Criteria the entry that should be updated has to match.

        """
        logger.debug("Updating in target %s where %s with %s", target, where, data)
        self._update(target=target, data=data, where=where)

    @abc.abstractmethod
    def _update(
        self,
        target: str,
        data: Info,
        where: Info,
    ) -> None:
        """Update data in a target."""

    def delete(self, target: str, where: Info) -> None:
        """Delete data from a target.

        Parameters
        ----------
        target : str
            Target object in which to delete an entry.
        where : dict[str, Any]
            Criteria the entry that should be deleted has to match.
        force : bool, default False
            Whether the deletion should be forced.

        """
        logger.debug("Deleting in target %s where %s", target, where)
        self._delete(target=target, where=where)

    @abc.abstractmethod
    def _delete(self, target: str, where: Info) -> None:
        """Delete data from a target."""
