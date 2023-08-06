import dataclasses


@dataclasses.dataclass(frozen=True)
class Command:
    """Any command.

    Commands are essential to the system and are not allowed to fail. If
    they fail, the respective exception is raised.

    """
