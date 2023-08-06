import dataclasses


@dataclasses.dataclass(frozen=True)
class Event:
    """Any event.

    An event can fail, i.e. it is not essential for the system to be stable.

    """
