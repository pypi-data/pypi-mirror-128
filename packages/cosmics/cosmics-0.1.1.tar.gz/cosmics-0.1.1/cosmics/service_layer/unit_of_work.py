import abc
from typing import Iterator

from cosmics import domain
from cosmics import repository


class AbstractUnitOfWork(abc.ABC):
    """Unit of Work pattern."""

    def __init__(self):
        """Initialze the uow."""
        self.events: list[domain.Event] = []

    def __enter__(self) -> "AbstractUnitOfWork":
        """Return the uow."""
        return self

    def __exit__(self, *args) -> None:
        """Do nothing."""
        pass

    def add_event(self, event: domain.Event) -> None:
        """Add new event to collected events."""
        self.events.append(event)

    def add_events(self, events: list[domain.Event]) -> None:
        """Add a list of events to collected events."""
        for event in events:
            self.add_event(event)

    def collect_new_events(self) -> Iterator[domain.Event]:
        """Collect and return all new events."""
        while self.events:
            yield self.events.pop(0)


class UnitOfWork(AbstractUnitOfWork):
    """A simple unit of work without database access."""


class DatabaseUnitOfWork(AbstractUnitOfWork):
    """Unit of work for the the database.

    Parameters
    ----------
    client : cosmics.repository.AbstractClient
        The client for interaction with the database.

    """

    def __init__(self, client: repository.AbstractClient):
        """Initialize the uow without connecting yet."""
        super().__init__()
        self._client = client

    def __enter__(self) -> "DatabaseUnitOfWork":
        """Initialize each repository."""
        self._initialize_repositories()
        return super().__enter__()

    @abc.abstractmethod
    def _initialize_repositories(self) -> None:
        """Initialize all repositories.

        E.g. if you have a repository named `items` that allows access via the
        repository class `ItemsRepository` (which is a child class of `AbstractRepository`),
        this method should look like
        ```Python
        self.items = ItemsRepository(client=self._client)
        ```
        You can set as many repositories as desired. These can then be accessed in handlers as
        ```Python
        with uow:
            uow.items.get(...)
        ```

        **Note:** You should also set this repository as an attribute in the
        `DatabaseUnitOfWork` class, i.e.
        ```Python
        class DatabaseUnitOfWork(AbstractUnitOfWork):
            ...

            items = ItemsRepository
        ```
        to ensure correct type checking.

        """
