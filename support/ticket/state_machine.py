from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Context:

    _state = None

    def __init__(self, state: State) -> None:
        self.transition_to(state)

    def transition_to(self, state: State):
        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

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
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context


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
    def change_state_to_InProgress(self) -> None:
        self.context.transition_to(StateInProgress())

    def change_state_to_Rejected(self) -> None:
        self.context.transition_to(StateRejected())

    def change_state_to_OnHold(self) -> None:
        self.context.transition_to(StateOnHold())


class StateInProgress(MixinGoToOpened, MixinGoToDone, MixinGoOnHold):
    def change_state_to_Opened(self) -> None:
        self.context.transition_to(StateOpened())

    def change_state_to_Done(self) -> None:
        self.context.transition_to(StateDone())

    def change_state_to_OnHold(self) -> None:
        self.context.transition_to(StateOnHold())


class StateDone(MixinGoToOpened):
    def change_state_to_Opened(self) -> None:
        self.context.transition_to(StateOpened())


class StateRejected(MixinGoToOpened):
    def change_state_to_Opened(self) -> None:
        self.context.transition_to(StateOpened())


class StateOnHold(MixinGoInProgress):
    def change_state_to_InProgress(self) -> None:
        self.context.transition_to(StateInProgress())


if __name__ == "__main__":
    context = Context(StateOpened())
    context.go_in_progress()
    context.go_done()
    context.go_opened()
    context.go_done()
    context.go_in_progress()
    context.go_rejected()
    context.go_opened()
    context.go_rejected()
