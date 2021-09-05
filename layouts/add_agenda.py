import PySimpleGUI as sg


def add_agenda_layout():

    return (
        [sg.Text('Insira a agenda a ser criada:')],
        [sg.Input(key = 'agenda')],
        [sg.Button('Voltar'), sg.Button('Adicionar')]
    )