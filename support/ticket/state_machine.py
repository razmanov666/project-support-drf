from __future__ import annotations
from abc import ABC, abstractmethod


class Context:
    """
    Контекст определяет интерфейс, представляющий интерес для клиентов. Он также
    хранит ссылку на экземпляр подкласса Состояния, который отображает текущее
    состояние Контекста.
    """

    _state = None
    """
    Ссылка на текущее состояние Контекста.
    """

    def __init__(self, state: State) -> None:
        self.transition_to(state)

    def transition_to(self, state: State):
        """
        Контекст позволяет изменять объект Состояния во время выполнения.
        """

        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    """
    Контекст делегирует часть своего поведения текущему объекту Состояния.
    """

    def go_opened(self):
        self._state.handle1()

    def go_in_progress(self):
        self._state.handle2()

    def go_done(self):
        self._state.handle3()
    
    def go_rejected(self):
        self._state.handle4()

    def go_on_hold(self):
        self._state.handle5()

    


class State(ABC):
    """
    Базовый класс Состояния объявляет методы, которые должны реализовать все
    Конкретные Состояния, a также предоставляет обратную ссылку на объект
    Контекст, связанный c Состоянием. Эта обратная ссылка может использоваться
    Состояниями для передачи Контекста другому Состоянию.
    """

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def handle1(self) -> None:
        pass

    @abstractmethod
    def handle2(self) -> None:
        pass

    @abstractmethod
    def handle3(self) -> None:
        pass

    @abstractmethod
    def handle4(self) -> None:
        pass

    @abstractmethod
    def handle5(self) -> None:
        pass


"""
Конкретные Состояния реализуют различные модели поведения, связанные с
состоянием Контекста.
"""


class StateOpened(State):
    def handle1(self) -> None:
        pass

    def handle2(self) -> None:
        self.context.transition_to(StateInProgress())

    def handle3(self) -> None:
        pass

    def handle4(self) -> None:
        self.context.transition_to(StateRejected())

    def handle5(self) -> None:
        self.context.transition_to(StateOnHold())


class StateInProgress(State):
    def handle1(self) -> None:
        self.context.transition_to(StateOpened())

    def handle2(self) -> None:
        pass

    def handle3(self) -> None:
        self.context.transition_to(StateDone())

    def handle4(self) -> None:
        pass

    def handle5(self) -> None:
        self.context.transition_to(StateOnHold())


class StateDone(State):
    def handle1(self) -> None:
        self.context.transition_to(StateOpened())
    
    def handle2(self) -> None:
        pass

    def handle3(self) -> None:
        pass

    def handle4(self) -> None:
        pass

    def handle5(self) -> None:
        pass


class StateRejected(State):
    def handle1(self) -> None:
        self.context.transition_to(StateOpened())
    
    def handle2(self) -> None:
        pass

    def handle3(self) -> None:
        pass

    def handle4(self) -> None:
        pass

    def handle5(self) -> None:
        pass


class StateOnHold(State):
    def handle1(self) -> None:
        pass

    def handle2(self) -> None:
        self.context.transition_to(StateInProgress())
        print(type(self))

    def handle3(self) -> None:
        pass

    def handle4(self) -> None:
        pass

    def handle5(self) -> None:
        pass


if __name__ == "__main__":
    # Клиентский код.

    context = Context(StateOpened())
    context.go_in_progress()
    context.go_done()
    context.go_opened()
    context.go_done()