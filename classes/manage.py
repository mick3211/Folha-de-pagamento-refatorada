from abc import ABCMeta, abstractmethod
from person import Person


class AbstractState(metaclass = ABCMeta):

    @abstractmethod
    def execute():
        pass

class AddEmployeeState(AbstractState):

    def __init__(self, id):
        self.id = id

    def execute(self):
        print('Empregado Removido')
        return RemoveEmployeeState(Manager._employee_list.pop(self.id))


class RemoveEmployeeState(AbstractState):

    def __init__(self, employee):
        self.employee = employee

    def execute(self):
        Manager._employee_list.update({self.employee.cpf: self.employee})
        print('Empregado Readicionado')
        return AddEmployeeState(self.employee.cpf)


class State():

    _undo_stack = []
    _redo_stack = []

    @classmethod
    def stack(cls, state, arg):

        cls._undo_stack.append(eval(state)(arg))
        cls._redo_stack.clear()
        return cls._undo_stack[-1]

    @classmethod
    def undo(cls):
        try:
            act = cls._undo_stack.pop()
        except IndexError: return
        
        cls._redo_stack.append(act.execute())

    @classmethod
    def redo(cls):
        try:
            act = cls._redo_stack.pop()
        except IndexError: return

        cls._undo_stack.append(act.execute())


class Manager():

    __instance = None
    _state = State()
    _employee_list = {}

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def add_employee(cls, id, employee):
        cls._employee_list.update({id: employee})
        cls._state.stack('AddEmployeeState', id)

    @classmethod
    def del_employee(cls, id):
        employee = cls._employee_list.pop(id)
        cls._state.stack('RemoveEmployeeState', employee)


man = Manager()
p = Person('Mickael', '123', '20').create_employee('Commisioned', 4500, 'Bolto', 10)
p2 = Person('José', '456', '20').create_employee('Salaried', 4510, 'Boltonaro')
man.add_employee(p.cpf, p)
man.add_employee(p2.cpf, p2)