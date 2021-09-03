from abc import ABCMeta, abstractmethod


class AbstractState(metaclass = ABCMeta):

    @abstractmethod
    def execute():
        pass

class AddEmployeeState(AbstractState):

    def __init__(self, id, manager):
        self.id = id
        self.manager = manager

    def execute(self):
        print('Empregado Removido')
        return RemoveEmployeeState(self.manager._employee_list.pop(self.id), self.manager)


class RemoveEmployeeState(AbstractState):

    def __init__(self, employee, manager):
        self.employee = employee
        self.manager = manager

    def execute(self):
        self.manager._employee_list.update({self.employee.cpf: self.employee})
        print('Empregado Readicionado')
        return AddEmployeeState(self.employee.cpf, self.manager)

class UpdateEmployeeState(AbstractState):

    def __init__(self, employee, manager):
        self.employee = employee
        self.manager = manager

    def execute(self):
        employee = self.manager._employee_list.pop(self.employee.cpf)
        self.manager._employee_list.update({self.employee.cpf: self.employee})
        print('Informações restauradas')
        return UpdateEmployeeState(employee, self.manager)


class InsertHisState(AbstractState):

    def __init__(self, his:list, manager=None):
        self.his = his

    def execute(self):
        try:
            value = self.his.pop()
        except IndexError:
            return super()

        print('Ultima entrada do historico desfeita', self.his)
        return PopHisState(self.his, value)


class PopHisState(AbstractState):

    def __init__(self, his:list, item, manager=None):
        self.his = his
        self.item = item

    def execute(self):
        self.his.append(self.item)
        print('Ultima entrada do historico Refeita', self.his)
        return InsertHisState(self.his)
        

class State():

    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    # Empilha uma ação na pilha undo e limpa a redo
    def stack(self, state, arg, manager=None):

        self._undo_stack.append(eval(state)(arg, manager))
        self._redo_stack.clear()
        return self._undo_stack[-1]

    #Desmpilha da pilha undo e execulta a ação, após empilha a ação na pilha de redo
    def undo(self):
        try:
            act = self._undo_stack.pop()
        except IndexError: return
        
        self._redo_stack.append(act.execute())

    #Desempilha da pilha de redo e execulta a ação, após empilha a ação na pilha de undo
    def redo(self):
        try:
            act = self._redo_stack.pop()
        except IndexError: return

        self._undo_stack.append(act.execute())