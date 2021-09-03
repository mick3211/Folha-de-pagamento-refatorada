import PySimpleGUI as sg


def reg_info_layout(employee):

    layout = []

    if type(employee.syndicate).__name__ == 'Syndicate':
        layout.append([[sg.Frame('Lançar taxa de serviço', [
                    [sg.Input(key='serv_taxe'), sg.Button('Lançar')],
                    ])]
                ]
        )

    if type(employee).__name__ == 'Hourly':
         layout.append(
            [sg.Frame('Registrar ponto', [
                [sg.Button('Registrar entrada' if employee.his.isin() else 'Registrar saída', key='ponto')]
            ])]
        )

    elif type(employee).__name__ == 'Commisioned':
        layout.append(
            [sg.Frame('Lançar venda',[
                [sg.Input(key='sale_value'), sg.Button('Lançar', key='venda')]
            ])]
        )

    if layout == []:
        layout.append(
                [sg.Text('Não há informações a serem registradas para o funcionário selecionado')],
                [sg.Button('Voltar')]
            )
    return layout