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