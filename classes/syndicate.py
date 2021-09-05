from abc import ABCMeta, abstractmethod


class AbstractSyndicate(metaclass = ABCMeta):

    def __init__(self, id=None, value=None):
        self.taxe_his = []
        self.set_id(id)
        self.set_default_taxe(value)

    def __str__(self):
        return f'taxas de serviço:{self.taxe_his}, id:{self.id}, taxa:{self.default_taxe}'

    @abstractmethod
    def get_total(self):
        pass

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


class Syndicate(AbstractSyndicate):

    def get_total(self):
        return self.default_taxe + sum(self.taxe_his)

    def set_id(self, id):
        self.id = id

    def insert_taxe(self, value: float):
            self.taxe_his.append(value)
    
    def set_default_taxe(self, value: float):
        self.default_taxe = value

    def clear_his(self):
        self.taxe_his.clear()


class NoSyndicate(AbstractSyndicate):

    def get_total(self):
        return 0

    def set_id(self, id):
        self.id = None
    
    def insert_taxe(self, value: float):
        pass

    def set_default_taxe(self, value: float):
        self.default_taxe = 0

    def clear_his():
        pass

def new_syndicate(syndicate, id=None, value=0):
    return eval(syndicate)(id, value)