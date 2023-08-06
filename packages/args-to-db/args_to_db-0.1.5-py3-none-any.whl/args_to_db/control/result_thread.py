import sys
import threading
import time
from typing import Dict, List, Optional

import cursor
from args_to_db.commands.command import Command

from .state import State


class SpinngingAnimation():
    _frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self) -> None:
        self._frame_index = 0

    def next_frame(self):
        self._frame_index = (self._frame_index + 1) % len(self._frames)

    def current_frame(self):
        return self._frames[self._frame_index]


class ResultThread(threading.Thread):
    _update_interval = 0.2

    def __init__(self, states: Dict[Command, State], print_status=True):
        super().__init__()

        self._newly_finished: List[Command] = []
        self._print_status = print_status
        self._spinning_animation = SpinngingAnimation()
        self._states = states
        self._stopevent = threading.Event()

    def update_state(self, cmd: Command, state: State) -> None:
        assert state in State

        self._states[cmd] = state
        if state in (State.SUCCESS, State.FAILED):
            self._newly_finished.append(cmd)

    def _print_states(self, overwrite=True):
        def _by_state(state):
            return {k: v for k, v in self._states.items() if v == state}

        # Think about how to improve htis...
        queued = _by_state(State.QUEUED)
        running = _by_state(State.RUNNING)
        sucessed = _by_state(State.SUCCESS)
        failed = _by_state(State.FAILED)

        for cmd in self._newly_finished:
            state = self._states[cmd]
            if state == State.SUCCESS:
                icon = "✓"
                color = "\033[92m"
            elif state == State.FAILED:
                icon = "🗙"
                color = "\033[31m"
            else:
                raise Exception("Invalid ProcessState")

            line = ""
            if color is not None:
                line += color
            line += f"{icon} \033[0m {cmd} \n"
            sys.stdout.write(line)

        self._newly_finished = []

        spinner = self._spinning_animation.current_frame()
        for cmd in running:
            icon = spinner
            color = None
            line = ""
            if color is not None:
                line += color
            line += f"{icon} \033[0m {cmd} \n"
            sys.stdout.write(line)

        line = f"{len(queued)} ⧖\033[0m, "
        line += f"{len(running)} {spinner}\033[0m, "
        line += f"\033[92m{len(sucessed)} ✓\033[0m, "
        line += f"\033[31m{len(failed)} 🗙\033[0m, "
        line += f"{len(self._states)} Total \n"
        sys.stdout.write(line)

        if overwrite:
            sys.stdout.write(f"\033[{len(running) + 1}A")

        sys.stdout.flush()

    def run(self) -> None:
        cursor.hide()

        while not self._stopevent.is_set():
            self._spinning_animation.next_frame()
            if self._print_status:
                self._print_states()

            time.sleep(self._update_interval)

        if self._print_status:
            self._print_states(overwrite=False)

        cursor.show()

    def join(self, timeout: Optional[float] = None) -> None:
        self._stopevent.set()
        return super().join(timeout=timeout)

    def states(self) -> Dict[Command, State]:
        return self._states
