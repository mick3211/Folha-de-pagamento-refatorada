from abc import ABCMeta, abstractmethod


class Person():

    def __init__(self, name, cpf):
        self.name = name
        self.cpf = cpf

    def create_employee(self, emplo_class, salary, paymethod, comissao=None):
        try:
            return eval(emplo_class)(salary, paymethod, comissao, self)
        except TypeError:
            return emplo_class(salary, paymethod, comissao, self)


class Adress():

    def __init__(self, cep='', rua='', num='', bairro='', cidade='', estado=''):
        self.cep = cep
        self.rua = rua
        self.num = num
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado

    def __str__(self):
        return (f'cep: {self.cep}, rua:{self.rua}, num:{self.num}, '
        f'bairro:{self.bairro}, cidade:{self.cidade}, estado:{self.estado}')

    def set_all(self, cep, rua, num, bairro, cidade, estado):
        self.cep = cep
        self.rua = rua
        self.num = num
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado


class AbstractSyndicate(metaclass = ABCMeta):

    def __init__(self, id=None, value=None):
        self.taxe_his = []
        self.set_id(id)
        self.set_default_taxe(value)

    def __str__(self):
        return f'taxas de serviço:{self.taxe_his}, id:{self.id}, taxa:{self.default_taxe}'

    @abstractmethod
    def set_id(self, id):
        pass

    @abstractmethod
    def insert_taxe(self, value: float):
        pass

    @abstractmethod
    def set_default_taxe(self, value: float):
        pass

    @abstractmethod
    def clear_his():
        pass


class AbstractEmployee(metaclass = ABCMeta):

    def __init__(self, salary, paymethod, comissao, person: Person):
        self.salary = salary
        self.paymethod = paymethod
        self.syndicate = NoSyndicate()
        self.adress = Adress()
        self.name = person.name
        self.cpf = person.cpf
        self.set_comissao(comissao)

    def __str__(self):
        return (f'//{type(self).__name__}, salário:{self.salary}, paymethod:{self.paymethod}, '
        f'syndicate:{type(self.syndicate).__name__}, name:{self.name}, cpf:{self.cpf} '
        f'endereço: {self.adress.__str__()}, sindicato:{self.syndicate.__str__()}')

    def set_syndicate(self, syndicate, id=None, value=None):
        self.syndicate = eval(syndicate)(id, value)

    def remove_syndicate(self):
        self.syndicate = NoSyndicate()

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


class Syndicate(AbstractSyndicate):

    def set_id(self, id):
        self.id = id

    def insert_taxe(self, value: float):
            self.taxe_his.append(value)
    
    def set_default_taxe(self, value: float):
        self.default_taxe = value

    def clear_his(self):
        self.taxe_his.clear()


class NoSyndicate(AbstractSyndicate):

    def set_id(self, id):
        self.id = None
    
    def insert_taxe(self, value: float):
        pass

    def set_default_taxe(self, value: float):
        self.default_taxe = 0

    def clear_his():
        pass


class Hourly(AbstractEmployee):

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

    def set_comissao(self, value):
        self.comissao = value

    def accumulated_payment(self):
        print('Salário acumulado do comissionado')

    def clear_his(self):
        print('Limpando histórico do comissionado')

    def reg(self):
        print('Limpando histórico do comissionado')

#p = Person('Mickael', '123').create_employee(Hourly, 4500, "Deposito")