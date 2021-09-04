from abc import ABCMeta, abstractmethod
from datetime import date, timedelta


class AbstractAgenda(metaclass = ABCMeta):

    def __init__(self):
        self.payday = date.today()

    def __str__(self):
        return f'agenda: {type(self).__name__}, payday: {self.payday}'

    def set_new_agenda(self, agenda):
        self.new_agenda = agenda

    def update_agenda(self):
        if self.new_agenda:
            self.new_agenda = self.new_agenda[:]

    @abstractmethod
    def set_payday():
        pass


class Semanal(AbstractAgenda):

    def __init__(self, week: int, wday: int):
        super().__init__()
        self.wday = wday
        self.week = week
        self.set_payday()

    def set_payday(self, init=date.today()):
        self.payday = init + timedelta(7)*self.week

        while self.payday.weekday() > self.wday:
            self.payday = self.payday - timedelta(1)

        while self.payday.weekday() < self.wday:
            self.payday = self.payday + timedelta(1)


class Mensal(AbstractAgenda):

    def __init__(self, day):
        super().__init__()
        self.day = day
        self.set_payday()

    def set_payday(self, init=date.today()):
        self.payday = init + timedelta(30)
        self.payday.replace(day=self.day)


def create_agenda(type, *args):
    
    try:
        return type(*args)
    except TypeError:
        return eval(type)(*args)