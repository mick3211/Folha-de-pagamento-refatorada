import PySimpleGUI as sg


def add_employee_layout():
    return (
        [sg.Frame('Informações pessoais', [
            [sg.Text('Nome:')],
            [sg.Input(key = 'name')],
            [sg.Text('CPF:')],
            [sg.Input(key = 'cpf')],
        ], key='personal_info')],
        [sg.Frame('Definições do empregado', [
            [sg.Text('Tipo:')],
            [sg.Combo(['Horista', 'Assalariado', 'Comissionado'], key='type', default_value='Horista', enable_events=True)],
            [sg.Text('Valor do salário hora:', key='t2'), sg.Input(size=(7,1), key='salary')],
            [sg.Frame('',[
                [sg.Text('Porcentagem da comissão:', key='t1'), sg.Input(size=(3,1), key='comissao')]
            ], visible=False, key='com')],
            [sg.Text('Método de pagamento:')],
            [sg.Combo(['Cheque pelos Correios', 'Cheque em mãos', 'Depósito bancário'], key='paymethod', default_value='Cheque em mãos')],
            [sg.Text('Faz parte do sindicato?')],
            [sg.Radio('Sim', group_id='syn', key='syndicate', enable_events=True), sg.Radio('Não', group_id='syn', key='not_syndicate', default=True, enable_events=True)],
            [sg.Text('Valor da taxa sindical:', key='syn_text', visible=False)],
            [sg.Input(0, key='taxa', visible=False, size=(10,1))],
        ], key='employee_info')],
        [sg.Frame('Endereço', [
                [sg.Text('Rua:', pad=((5,265), (0,0))), sg.Text('N°:')],
                [sg.Input(key='rua', size=(41,1)), sg.Input(key='numero', size=(3,1))],
                [sg.Text('CEP:', pad=((5,125), (0,0))), sg.Text('Bairro:')],
                [sg.Input(key='cep', size=(22,1)), sg.Input(key='bairro', size=(22,1))],
                [sg.Text('Cidade:', pad=((5,115),(0,0))), sg.Text('Estado:')],
                [sg.Input(key='cidade', size=(22,1)), sg.Input(key='estado', size=(22,1))]
            ], key='adress')
        ],
        [sg.Button('Voltar'), sg.Button('Adicionar')]
    )