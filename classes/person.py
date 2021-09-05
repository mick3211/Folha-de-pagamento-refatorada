from abc import ABCMeta, abstractmethod
from datetime import time
from classes.syndicate import new_syndicate
from classes.adress import Adress
from classes.hist import SalesHis, ClockHis
from classes.agenda import create_agenda


class Person():

    def __init__(self, name, cpf):
        self.name = name
        self.cpf = cpf

    def create_employee(self, emplo_class, salary, paymethod, comissao=None):
        try:
            return emplo_class(salary, paymethod, comissao, self)
        except TypeError:
            return eval(emplo_class)(salary, paymethod, comissao, self)


class AbstractEmployee(metaclass = ABCMeta):

    def __init__(self, salary, paymethod, comissao, person: Person):
        self.salary = salary
        self.paymethod = paymethod
        self.adress = Adress()
        self.name = person.name
        self.cpf = person.cpf
        self.his = None
        self.set_syndicate('NoSyndicate')
        self.set_comissao(comissao)
        self.set_agenda(self.agenda)

    def __str__(self):
        return (f'//{type(self).__name__}, salário:{self.salary}, paymethod:{self.paymethod}, '
        f'syndicate:{type(self.syndicate).__name__}, name:{self.name}, cpf:{self.cpf}, '
        f'endereço: {self.adress}, sindicato:{self.syndicate}, agenda:{self.agenda}, {self.new_agenda}')

    def set_syndicate(self, syndicate, id=None, value=0):
        self.syndicate = new_syndicate(syndicate, id, value)
        
    def set_agenda(self, agenda):
        self.new_agenda = agenda

    def update_agenda(self):
        self.agenda = self.new_agenda[:]

    @abstractmethod
    def set_comissao(self, value):
        pass

    @abstractmethod
    def clear_his():
        pass

    @abstractmethod
    def accumulated_payment():
        pass

    @abstractmethod
    def insert_his():
        pass


class Hourly(AbstractEmployee):

    def __init__(self, salary, paymethod, comissao, person: Person):
        self.agenda = create_agenda('Semanal', 1, 4)
        super().__init__(salary, paymethod, comissao, person)
        self.his = ClockHis()

    def set_comissao(self, value):
        return super().set_comissao(value)

    def accumulated_payment(self):
        print('Pagamento acumulado de horista')

    def clear_his(self):
        print('Limpando historico do horista')
    
    def insert_his(self, value=None):
        self.his.punch(time.time())
        

class Salaried(AbstractEmployee):

    def __init__(self, salary, paymethod, comissao, person: Person):
        self.agenda = create_agenda('Mensal', 30)
        super().__init__(salary, paymethod, comissao, person)

    def set_comissao(self, value):
        return super().set_comissao(value)

    def accumulated_payment(self):
        print('Salário acumulado do assalariado')

    def clear_his(self):
        print('Limpando histórico do assalariado')

    def insert_his(self, value=None):
        print('Assalariado não possui historico')


class Commisioned(AbstractEmployee):

    def __init__(self, salary, paymethod, comissao, person: Person):
        self.agenda = create_agenda('Semanal', 2, 4)
        super().__init__(salary, paymethod, comissao, person)
        self.his = SalesHis()

    def set_comissao(self, value):
        self.comissao = value

    def accumulated_payment(self):
        print('Salário acumulado do comissionado')

    def clear_his(self):
        print('Limpando histórico do comissionado')

    def insert_his(self, value):
        self.his.new_sale(time.time(), value)