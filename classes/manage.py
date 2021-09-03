from abc import ABCMeta, abstractmethod


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

class UpdateEmployeeState(AbstractState):

    def __init__(self, employee):
        self.employee = employee

    def execute(self):
        employee = Manager._employee_list.pop(self.employee.cpf)
        Manager._employee_list.update({self.employee.cpf: self.employee})
        print('Informações restauradas')
        return UpdateEmployeeState(employee)


class State():

    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    # Empilha uma ação na pilha undo e limpa a redo
    def stack(self, state, arg):

        self._undo_stack.append(eval(state)(arg))
        self._redo_stack.clear()
        return self._undo_stack[-1]

    def undo(self):
        try:
            act = self._undo_stack.pop()
        except IndexError: return
        
        self._redo_stack.append(act.execute())

    def redo(self):
        try:
            act = self._redo_stack.pop()
        except IndexError: return

        self._undo_stack.append(act.execute())


class Manager():

    __instance = None
    _state = State()
    _employee_list = {}

    # Garante que apenas uma instância da classe será criada
    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def undo(cls):
        cls._state.undo()

    @classmethod
    def redo(cls):
        cls._state.redo()

    @classmethod
    def add_employee(cls, id, employee):
        cls._employee_list.update({id: employee})
        cls._state.stack('AddEmployeeState', id)
        
        print('--Empregado adicionado--', cls._employee_list, cls._employee_list[id])

    @classmethod
    def del_employee(cls, id):
        try:
            employee = cls._employee_list.pop(id)
        except IndexError:
            return False
        cls._state.stack('RemoveEmployeeState', employee)

        print ('--Empregado removido--', employee)
        return True

    @classmethod
    def update_employee(cls, id, updt_employee):
        employee = cls._employee_list.get(id)
        cls._state.stack('UpdateEmployeeState', employee)
        cls._employee_list.update({id: updt_employee})

        print('--empregado editado--', cls._employee_list, cls._employee_list[id])