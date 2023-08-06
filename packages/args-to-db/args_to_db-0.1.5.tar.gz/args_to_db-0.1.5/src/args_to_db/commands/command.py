from typing import Any, List


class Command():
    def __init__(self, args: List[str], dependencies: List[str] = None):
        self._args = args
        self._dependencies = dependencies
        if self._dependencies is None:
            self._dependencies = []

    def args(self):
        return self._args

    def dependencies(self):
        return self._dependencies

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Command):
            return False

        return (self.args() == other.args()) and \
               (self.dependencies() == other.dependencies())

    def __repr__(self) -> str:
        return ' '.join(self._args)

    def __hash__(self) -> int:
        return hash((*self._args, *self._dependencies))  # type: ignore
