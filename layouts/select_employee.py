import PySimpleGUI as sg

def select_employee_layout(employee_list):

    i = list(employee_list.keys())

    return (
        [sg.Text('Selecione o empregado:')],
        [sg.Combo(i, key='selected_employee', default_value=i[0], readonly=True)],
        [sg.Button('Selecionar')],
    )
