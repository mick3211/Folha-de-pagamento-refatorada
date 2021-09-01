from states import State


class Manager():

    __instance = None
    _state = State()
    _employee_list = {}

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def add_employee(cls, id, employee):
        cls._employee_list.update({id: employee})
        cls._state = State.select_state('AddEmployeeState')


man = Manager()

man.add_employee('Mickael', '123', '45', 'Salaried', 4500, 'Depósito Bancário')

print(man._employee_list)
print(man._employee_list['123'].__str__())