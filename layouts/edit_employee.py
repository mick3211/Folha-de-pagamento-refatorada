import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Input

def edit_employee_layout(employee, agendas: list):

    TYPES = {'Salaried': 'Assalariado', 'Commisioned': 'Comissionado', 'Hourly': 'Horista'}
    info_list = employee.__dict__
    adress_list = employee.adress.__dict__
    agendas_list = ['Não alterar']
    agendas_list.extend(f'{e}.{i.to_string()}' for e, i in enumerate(agendas))

    return (
        [sg.Frame('Informações pessoais', [
            [sg.Text('Nome:')],
            [sg.Input(info_list['name'], key = 'name')],
        ], key='personal_info')],
        [sg.Frame('Definições do empregado', [
            [sg.Text('Tipo:')],
            [sg.Combo(['Horista', 'Assalariado', 'Comissionado'], key='type', default_value=TYPES[type(employee).__name__], enable_events=True, readonly=True)],
            [sg.Text('Salário:')],
            [sg.Input(f"R$ {info_list['salary']}", disabled=True, size=(10, 1))],
            [sg.Frame('',[
                [sg.Text('Porcentagem da comissão:', key='t1'), sg.Input(0, size=(3,1), key='comissao')]
            ], key='com', visible=False)],
            [sg.Text('Método de pagamento:')],
            [sg.Combo(['Cheque pelos Correios', 'Cheque em mãos', 'Depósito bancário'], key='paymethod', default_value=info_list['paymethod'], readonly=True)],
            [sg.Text('Agenda de pagamento (aplicado após o próximo pagamento)')],
            [sg.Combo(agendas_list, agendas_list[0], key='agenda', readonly=True, )],
            [sg.Text('Faz parte do sindicato?')],
            [sg.Radio('Sim', group_id='syn', key='syndicate', enable_events=True, default=False if type(employee.syndicate).__name__ == 'NoSyndicate' else True),
                sg.Radio('Não', group_id='syn', key='not_syndicate', enable_events=True, default=True if type(employee.syndicate).__name__ == 'NoSyndicate' else False)],
            [sg.Text('Valor da taxa sindical:', key='syn_text', visible=False if type(employee.syndicate).__name__ == 'NoSyndicate' else True)],
            [sg.Input(employee.syndicate.default_taxe, key='taxa', visible=False if type(employee.syndicate).__name__ == 'NoSyndicate' else True, size=(10,1))],
        ], key='employee_info')],
        [sg.Frame('Endereço', [
                [sg.Text('Rua:', pad=((5,265), (0,0))), sg.Text('N°:')],
                [sg.Input(adress_list['rua'], key='rua', size=(41,1)), sg.Input(adress_list['num'], key='numero', size=(3,1))],
                [sg.Text('CEP:', pad=((5,125), (0,0))), sg.Text('Bairro:')],
                [sg.Input(adress_list['cep'], key='cep', size=(22,1)), sg.Input(adress_list['bairro'], key='bairro', size=(22,1))],
                [sg.Text('Cidade:', pad=((5,115),(0,0))), sg.Text('Estado:')],
                [sg.Input(adress_list['cidade'], key='cidade', size=(22,1)), sg.Input(adress_list['estado'], key='estado', size=(22,1))]
            ], key='adress')
        ],
        [sg.Button('EXCLUIR EMPREGADO', button_color = 'red')],
        [sg.Button('Voltar'), sg.Button('Salvar')]
    )