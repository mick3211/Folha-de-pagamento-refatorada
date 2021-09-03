from abc import ABCMeta, abstractmethod
from syndicate import new_syndicate
from adress import Adress
from hist import SalesHis, ClockHis


class Person():

    def __init__(self, name, cpf):
        self.name = name
        self.cpf = cpf

    def create_employee(self, emplo_class, salary, paymethod, comissao=None):
        try:
            return eval(emplo_class)(salary, paymethod, comissao, self)
        except TypeError:
            return emplo_class(salary, paymethod, comissao, self)


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

    def __str__(self):
        return (f'//{type(self).__name__}, salário:{self.salary}, paymethod:{self.paymethod}, '
        f'syndicate:{type(self.syndicate).__name__}, name:{self.name}, cpf:{self.cpf} '
        f'endereço: {self.adress}, sindicato:{self.syndicate}')

    def set_syndicate(self, syndicate, id=None, value=0):
        self.syndicate = new_syndicate(syndicate, id, value)

    def get_attr():
        pass

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
    def reg():
        pass


class Hourly(AbstractEmployee):

    def __init__(self, salary, paymethod, comissao, person: Person):
        super().__init__(salary, paymethod, comissao, person)
        self.his = ClockHis()

    def set_comissao(self, value):
        return super().set_comissao(value)

    def accumulated_payment(self):
        print('Pagamento acumulado de horista')

    def clear_his(self):
        print('Limpando historico do horista')
    
    def reg(self):
        print('Registrando ponto')
        

class Salaried(AbstractEmployee):

    def set_comissao(self, value):
        return super().set_comissao(value)

    def accumulated_payment(self):
        print('Salário acumulado do assalariado')

    def clear_his(self):
        print('Limpando histórico do assalariado')

    def reg(self):
        print('Assalariado não possui historico')


class Commisioned(AbstractEmployee):

    def __init__(self, salary, paymethod, comissao, person: Person):
        super().__init__(salary, paymethod, comissao, person)
        self.his = SalesHis()

    def set_comissao(self, value):
        self.comissao = value

    def accumulated_payment(self):
        print('Salário acumulado do comissionado')

    def clear_his(self):
        print('Limpando histórico do comissionado')

    def reg(self):
        print('Adicionando venda')

#p = Person('Mickael', '123').create_employee(Hourly, 4500, "Deposito")
#p2 = Person('José', '123').create_employee(Commisioned, 4500, "Deposito")