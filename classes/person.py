from abc import ABCMeta, abstractmethod
import time
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
        self.agenda = self.new_agenda
        print('Agenda atualizada', self.agenda)

    def clear_his(self):
        self.his.clear()

    def pay(self):
        payment = self.accumulated_payment()
        self.clear_his()
        self.update_agenda()
        self.agenda.set_payday()
        self.syndicate.clear_his()
        print('Funcionário pago',payment)

    @abstractmethod
    def set_comissao(self, value):
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
    
    def insert_his(self, value=None):
        self.his.punch(time.time())
        
    def accumulated_payment(self):

        syn_total = self.syndicate.get_total()
        total_h = 0
        total_extra = 0

        for each in self.his._values:
            sec = (each[1] - each[0])

            if sec > 28800:
                total_extra += (sec - 28800)
                total_h += 28800
            else: total_h += sec

        total_h /= 3600
        total_extra /= 3600

        return (self.salary*total_h + self.salary*total_extra*1.5) - syn_total

class Salaried(AbstractEmployee):

    def __init__(self, salary, paymethod, comissao, person: Person):
        self.agenda = create_agenda('Mensal', 30)
        super().__init__(salary, paymethod, comissao, person)

    def set_comissao(self, value):
        return super().set_comissao(value)

    @staticmethod
    def clear_his():
        pass

    def insert_his(self, value=None):
        print('Assalariado não possui historico')

    def accumulated_payment(self):
        syn_total = self.syndicate.get_total()
        salary = self.salary/4
        return salary*self.agenda.work_weeks() - syn_total


class Commisioned(AbstractEmployee):

    def __init__(self, salary, paymethod, comissao, person: Person):
        self.agenda = create_agenda('Semanal', 2, 4)
        super().__init__(salary, paymethod, comissao, person)
        self.his = SalesHis()

    def set_comissao(self, value):
        self.comissao = value

    def insert_his(self, value):
        self.his.new_sale(value)

    def accumulated_payment(self):
        syn_total = self.syndicate.get_total()
        com_total = self.his.get_total()
        salary = self.salary/2
        return salary*self.agenda.work_weeks() - syn_total + com_total*self.comissao