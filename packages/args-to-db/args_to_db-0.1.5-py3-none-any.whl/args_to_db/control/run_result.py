from typing import Dict, List

import pandas
from args_to_db.commands.command import Command
from args_to_db.control.state import State


class RunResult:
    def __init__(self,
                 states: Dict[Command, State],
                 data: pandas.DataFrame) -> None:
        self._states = states
        self._data = data

    def write_data(self, path):
        self._data.to_pickle(path)
        # if debug
        # self.data.to_csv(f'{path}.csv')

    @property
    def data(self) -> pandas.DataFrame:
        return self._data

    @data.setter
    def data(self, data: pandas.DataFrame):
        self._data = data

    @property
    def states(self) -> Dict[Command, State]:
        return self._states

    @states.setter
    def states(self, states: Dict[Command, State]) -> None:
        self._states = states

    def states_filtered(self, state: State) -> List[Command]:
        return [cmd for cmd, st in self._states.items() if st == state]
