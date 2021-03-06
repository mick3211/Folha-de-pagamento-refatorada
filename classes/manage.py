from abc import ABCMeta, abstractmethod
from datetime import date
from classes.states import State
from classes.agenda import Semanal, Mensal


class Manager():

    __instance = None
    _state = State()
    _employee_list = {}
    _agendas = [Semanal(1, 4), Semanal(2, 4), Mensal(30)]

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
        cls._state.stack('AddEmployeeState', id, cls)
        
        print('--Empregado adicionado--', cls._employee_list, cls._employee_list[id])

    @classmethod
    def del_employee(cls, id):
        try:
            employee = cls._employee_list.pop(id)
        except IndexError:
            return False
        cls._state.stack('RemoveEmployeeState', employee, cls)

        print ('--Empregado removido--', employee)
        return True

    @classmethod
    def update_employee(cls, id, updt_employee):
        employee = cls._employee_list.get(id)
        cls._state.stack('UpdateEmployeeState', employee, cls)
        cls._employee_list.update({id: updt_employee})

        print('--empregado editado--', cls._employee_list, cls._employee_list[id])

    @classmethod
    def insert_his(cls, employee, value=None):
        employee.insert_his(value)

        if len(employee.his._values) > 0:
            cls._state.stack('InsertHisState', (employee.his))
            print('--Valor registrado--', employee.his)

    @classmethod
    def insert_service_taxe(cls, employee, value):
        employee.syndicate.insert_taxe(value)
        cls._state.stack('InsertHisState', (employee.syndicate.taxe_his))

        print('--Valor registrado--', employee.syndicate)

    @classmethod
    def add_agenda(cls, agenda):
        cls._agendas.append(agenda)
        print('--Agenda adicionada--', cls._agendas[-1])

    @classmethod
    def pending_pays(cls, time=date.today()):

        pending = list()

        for emplo in cls._employee_list.values():
            if emplo.agenda.payday == time:
                pending.append(emplo)
        return pending