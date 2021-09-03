class His():

    def __init__(self):
        self._values = []

    def __str__(self):
        return f'Histórico: {self._values}'

    def clear(self):
        self._values.clear()

    def pop(self):
        return self._values.pop()

    def append(self, value):
        self._values.append(value)


class SalesHis(His):

    def new_sale(self, time, value):
        self._values.append({time: value})


class ClockHis(His):

    def __init__(self):
        super().__init__()
        self.__time_set = []

    def isin(self):
        if len(self.__time_set) >= 1:
            return True
        return False

    def punch(self, time):
        self.__time_set.append(time)

        if len(self.__time_set) > 1:
            self._values.append(self.__time_set[:])
            self.__time_set.clear()
