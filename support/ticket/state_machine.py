from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class ManagerOfState:

    _state = None

    def __init__(self, state: State) -> None:
        self.transition_to(const_dict_of_states.get(state))

    def transition_to(self, state: State):
        if self._state == None:
            print(f"ManagerOfState: Current status {type(state).__name__}")
        else:
            print(f"ManagerOfState: Transition to {type(state).__name__}")
        self._state = state
        self._state.ManagerOfState = self

    def go_opened(self):
        try:
            self._state.change_state_to_Opened()
        except AttributeError:
            print(f"{type(self._state).__name__} can't do 'go_opened'")

    def go_in_progress(self):
        try:
            self._state.change_state_to_InProgress()
        except AttributeError:
            print(f"{type(self._state).__name__} can't do 'go_in_progress'")

    def go_done(self):
        try:
            self._state.change_state_to_Done()
        except AttributeError:
            print(f"{type(self._state).__name__} can't do 'go_done'")

    def go_rejected(self):
        try:
            self._state.change_state_to_Rejected()
        except AttributeError:
            print(f"{type(self._state).__name__} can't do 'go_rejected'")

    def go_on_hold(self):
        try:
            self._state.change_state_to_OnHold()
        except AttributeError:
            print(f"{type(self._state).__name__} can't do 'go_on_hold'")


class State(ABC):
    @property
    def ManagerOfState(self) -> ManagerOfState:
        return self._ManagerOfState

    @ManagerOfState.setter
    def ManagerOfState(self, ManagerOfState: ManagerOfState) -> None:
        self._ManagerOfState = ManagerOfState


class MixinGoToOpened(State):
    @abstractmethod
    def change_state_to_Opened(self) -> None:
        pass


class MixinGoInProgress(State):
    @abstractmethod
    def change_state_to_InProgress(self) -> None:
        pass


class MixinGoToDone(State):
    @abstractmethod
    def change_state_to_Done(self) -> None:
        pass


class MixinGoToRejected(State):
    @abstractmethod
    def change_state_to_Rejected(self) -> None:
        pass


class MixinGoOnHold(State):
    @abstractmethod
    def change_state_to_OnHold(self) -> None:
        pass


class StateOpened(MixinGoInProgress, MixinGoToRejected, MixinGoOnHold):
    name_status = "OP"

    def change_state_to_InProgress(self) -> None:
        self.ManagerOfState.transition_to(StateInProgress())

    def change_state_to_Rejected(self) -> None:
        self.ManagerOfState.transition_to(StateRejected())

    def change_state_to_OnHold(self) -> None:
        self.ManagerOfState.transition_to(StateOnHold())


class StateInProgress(MixinGoToOpened, MixinGoToDone, MixinGoOnHold):
    name_status = "IP"

    def change_state_to_Opened(self) -> None:
        self.ManagerOfState.transition_to(StateOpened())

    def change_state_to_Done(self) -> None:
        self.ManagerOfState.transition_to(StateDone())

    def change_state_to_OnHold(self) -> None:
        self.ManagerOfState.transition_to(StateOnHold())


class StateDone(MixinGoToOpened):
    name_status = "DN"

    def change_state_to_Opened(self) -> None:
        self.ManagerOfState.transition_to(StateOpened())


class StateRejected(MixinGoToOpened):
    name_status = "RJ"

    def change_state_to_Opened(self) -> None:
        self.ManagerOfState.transition_to(StateOpened())


class StateOnHold(MixinGoInProgress):
    name_status = "OH"

    def change_state_to_InProgress(self) -> None:
        self.ManagerOfState.transition_to(StateInProgress())


const_dict_of_states = {"OP": StateOpened(),
                        "IP": StateInProgress(),
                        "DN": StateDone(),
                        "RJ": StateRejected(),
                        "OH": StateOnHold()}

if __name__ == "__main__":
    ManagerOfState = ManagerOfState("IP")
    ManagerOfState.go_opened()
    ManagerOfState.go_done()
    ManagerOfState.go_opened()
    ManagerOfState.go_done()
    ManagerOfState.go_in_progress()
    ManagerOfState.go_rejected()
    ManagerOfState.go_opened()
    ManagerOfState.go_rejected()
