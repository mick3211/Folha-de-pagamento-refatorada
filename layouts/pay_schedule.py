import PySimpleGUI as sg


def pay_schedule_layout(emplo_list: list, date):

    pay_list = list()
    
    for emplo in emplo_list:
        pay_list.append(f'{emplo.name}//R${emplo.accumulated_payment()}//{emplo.paymethod}')

    if len(emplo_list) == 0:
        return(
            [sg.Text('Não há funcionários para serem pagos hoje')],
            [sg.Button('Voltar')]
        )
    else:
        return(
            [sg.Text(f'Hoje: {date}', font=('arial', 15))],
            [sg.Multiline('\n'.join(pay_list), size=(50, 15), disabled=True)],
            [sg.Button('Voltar'), sg.Button('Pagar', button_color='green')]
        )