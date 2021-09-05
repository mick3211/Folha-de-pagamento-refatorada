import PySimpleGUI as sg


def pay_schedule_layout(emplo_list: list, date):

    if len(emplo_list) == 0:
        return(
            [sg.Text('Não há funcionários para serem pagos hoje')],
            [sg.Button('Voltar')]
        )
    else:
        return(
            [sg.Text(f'Hoje: {date}', size=(20,6))],
            [sg.Multiline(f'{emplo.name}\n') for emplo in emplo_list],
        )