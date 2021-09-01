from abc import ABCMeta, abstractmethod

class AbstractState(metaclass = ABCMeta):

    @abstractmethod
    def undo():
        pass

    @abstractmethod
    def redo():
        pass


class AddEmployeeState(AbstractState):

    def undo():
        pass

    def redo():
        pass


class RemoveEmployeeState(AbstractState):

    def undo():
        pass

    def redo():
        pass


class State():

    _stack = []

    @classmethod
    def add_state(cls, state):

        cls._stack.append(eval(state)())
        return cls._stack[-1]

    def undo():
        pass

    def redo():
        pass