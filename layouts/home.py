import PySimpleGUI as sg


def home_layout():
    return (
        [sg.Menu([['Opções',('Desfazer', 'Refazer')]])],
        [sg.Button('Adicionar empregado', size=(30,2))],
        [sg.Button('Editar empregado', size=(30,2))],
        [sg.Button('Lançar ponto / taxa / venda', size=(30,2))],
        [sg.Button('Adicionar agenda de pagamento', size=(30,2), key='agenda')],
        [sg.Button('Rodar folha de pagamento', size=(30,2), key='pay')],
        [sg.Button('Sair', button_color = 'red', size=(30,2))]
    )