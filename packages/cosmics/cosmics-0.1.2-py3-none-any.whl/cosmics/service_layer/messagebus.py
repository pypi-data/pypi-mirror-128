import functools
import inspect
import logging
from typing import Any
from typing import Callable
from typing import Iterator
from typing import Union

from . import unit_of_work
from cosmics import domain

logger = logging.getLogger(__name__)


Message = Union[domain.Command, domain.Event]
Messages = list[Message]
Handler = Callable
Handlers = list[Handler]
Command = domain.Command
Event = domain.Event
Events = Iterator[Event]
CommandHandlers = dict[Command, Handler]
EventHandlers = dict[Event, Handlers]


class MissingHandlerException(Exception):
    """The given command does not have a handler."""


class MessageBus:
    """Processes commands and events and passes them to the respective handler(s).

    Parameters
    ----------
    uow : AbstractUnitOfWork
    command_handlers : dict[Command, Callable]
        Handler for each command.
    event_handlers : dict[Event, list[Callable]]
        All handlers for each event.
    dependencies
        Additional dependencies to inject into a handler.
        These are only injected if the handler needs any of them.

    Commands are emitted by the entrypoint(s) (i.e. Cogs). Events are the response of
    handlers.

    """

    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        command_handlers: CommandHandlers,
        event_handlers: EventHandlers,
        **dependencies,
    ):
        """Initialize messagebus with Unit of Work and Handlers."""
        self._uow = uow
        self._command_handlers = command_handlers
        self._event_handlers = event_handlers
        self._dependencies = dependencies | {"uow": self._uow}

    async def handle(self, message: Message, **dependencies) -> None:
        """Handle a message.

        Parameters
        ----------
        message : Command or Event
        dependencies
            Additional dependencies to inject into handlers.
            These dependencies are only injected if a handler needs any of them.

        """
        logger.debug(
            "Handling message %s with additional dependencies %s", message, dependencies
        )
        queue = [message]
        while queue:
            message_to_handle = queue.pop(0)
            new_events = await self._handle_message(message_to_handle, **dependencies)
            logger.error(
                "Handling message %s pushed new events %s",
                message_to_handle,
                new_events,
            )
            queue.extend(new_events)
            logger.error("Events waiting in queue: %s", queue)

    @functools.singledispatchmethod
    async def _handle_message(self, message: Any, **dependencies) -> Events:
        """Handle a given message."""
        raise NotImplementedError("Message not an event or command: %s", message)

    @_handle_message.register
    async def _handle_command(self, message: domain.Command, **dependencies) -> Events:
        """Handle command with respective handler.

        Commands are not allowed to fail. Hence, any exception is logged
        and raised.

        """
        logger.debug("Handling command %s", message)
        handler = self._get_command_handler(message)
        return await self._handle_command_with_handler(
            command=message, handler=handler, **dependencies
        )

    @_handle_message.register
    async def _handle_event(self, message: domain.Event, **dependencies) -> Events:
        """Handle event with respective handlers.

        Events are allowed to fail. Hence, any exception is logged but does
        not abort the procedure.

        """
        handlers = self._get_event_handlers(message)
        return await self._handle_event_with_handlers(
            event=message, handlers=handlers, **dependencies
        )

    def _get_command_handler(self, command: domain.Command) -> Handler:
        try:
            return self._command_handlers[type(command)]
        except KeyError:
            raise MissingHandlerException(
                "Handler not defined for command %s", type(command)
            )

    def _get_event_handlers(self, event: domain.Event) -> Handlers:
        try:
            return self._event_handlers[type(event)]
        except KeyError:
            raise MissingHandlerException("No handler(s) defined for event %s", event)

    async def _handle_command_with_handler(
        self, command: domain.Command, handler: Handler, **dependencies
    ) -> Events:
        try:
            return await self._handle_and_collect_new_events(
                message=command, handler=handler, **dependencies
            )
        except Exception:  # noqa: B902
            logger.error(
                "Exception raised handling command %s with handler %s", command, handler
            )
            raise

    async def _handle_event_with_handlers(
        self, event: domain.Event, handlers: Handlers, **dependencies
    ) -> Events:
        collected_events: list[Event] = []
        for handler in handlers:
            logger.debug("Handling event %s with handler %s", event, handler)
            try:
                new_events = await self._handle_and_collect_new_events(
                    message=event, handler=handler, **dependencies
                )
            except Exception:  # noqa: B902
                logger.error(
                    "Exception raised handling event %s with handler %s",
                    event,
                    handler,
                    exc_info=True,
                )
            else:
                collected_events.extend(new_events)
        return iter(collected_events)

    async def _handle_and_collect_new_events(
        self, message: Message, handler: Handler, **dependencies
    ) -> Events:
        """Handle a message and collect all recently published events."""
        handler_with_dependencies = self._inject_dependencies(handler, **dependencies)
        if inspect.iscoroutinefunction(handler_with_dependencies):
            await handler_with_dependencies(message)
        else:
            handler_with_dependencies(message)
        return self._uow.collect_new_events()

    def _inject_dependencies(
        self, handler: Handler, **dependencies
    ) -> functools.partial:
        dependencies_filtered = self._filter_dependencies(handler, **dependencies)
        return functools.partial(handler, **dependencies_filtered)

    def _filter_dependencies(self, handler: Handler, **dependencies) -> dict:
        signature = inspect.signature(handler)
        all_dependencies = self._dependencies | dependencies
        return {
            parameter: value
            for parameter, value in all_dependencies.items()
            if parameter in signature.parameters
        }
