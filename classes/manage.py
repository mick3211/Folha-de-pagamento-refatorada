from states import State
from person import Person

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
        cls._state.add_state('AddEmployeeState')


man = Manager()

p = Person('Mickael', '123', '20').create_employee('Commisioned', 4500, 'Bolto', 10)

man.add_employee(p.cpf, p)

print(man._employee_list)
print(man._employee_list['123'].__str__())