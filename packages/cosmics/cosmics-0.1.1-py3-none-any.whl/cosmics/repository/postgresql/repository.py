import logging

from cosmics.domain import model
from cosmics.repository import repository

logger = logging.getLogger(__name__)

DatabaseModel = model.AbstractModel


class Repository(repository.AbstractRepository):
    """Represents an abstract database target in a Postgresql database."""

    def add_and_return_row_id(self, item: DatabaseModel) -> int:
        """Add row to database."""
        logger.debug("Adding item %s", item)
        inserted_row_id = self._add_and_return_row_id(item)
        self.added.append(item)
        logger.debug("Inserted item %s and received row ID %s", item, inserted_row_id)
        return inserted_row_id

    def _add_and_return_row_id(self, item: DatabaseModel) -> int:
        """Insert row."""
        with self._client as client:
            return client.insert_and_return_row_id(
                target=self.target,
                data=item.to_dict(),
            )
