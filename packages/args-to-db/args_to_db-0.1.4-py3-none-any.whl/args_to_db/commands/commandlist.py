from typing import Any, List

from args_to_db.commands.command import Command


class CommandList():
    @classmethod
    def empty(cls):
        return cls([])

    def __init__(self, commands: List[Command]):
        self._commands = commands

    def __add__(self, other):
        assert isinstance(other, CommandList)

        if self == CommandList.empty():
            return CommandList(other.commands().copy())

        if other == CommandList.empty():
            return Command(self._commands.copy())

        commands = []
        for s_cmds in self.commands():
            for o_cmds in other.commands():
                commands += [Command(s_cmds.args() + o_cmds.args())]

        return CommandList(commands)

    def commands(self) -> List[Command]:
        return self._commands

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CommandList):
            return False

        return self._commands == other.commands()

    def __len__(self) -> int:
        return len(self._commands)

    def __repr__(self) -> str:
        return f'CommandList({str(self._commands)})'
