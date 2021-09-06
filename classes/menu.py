import PySimpleGUI as sg
from datetime import date
from layouts.add_employee import add_employee_layout
from layouts.edit_employee import edit_employee_layout
from layouts.select_employee import select_employee_layout
from layouts.reg_info import reg_info_layout
from layouts.add_agenda import add_agenda_layout
from layouts.pay_schedule import pay_schedule_layout
from classes.person import Person
from classes.manage import Manager
from classes.agenda import create_agenda


TYPES = {'Assalariado': 'Salaried', 'Comissionado': 'Commisioned', 'Horista': 'Hourly'}
DAYS = {'segunda': 0, 'terça': 1, 'quarta': 2, 'quinta': 3, 'sexta': 4, 'sábado': 5, 'domingo': 6}


class Menu():

    def select_employee():

        employee_list = Manager()._employee_list

        if len(employee_list) == 0:
            sg.popup('SEM FUNCIONÁRIOS CADASTRADOS!', title='ERRO')
            return False

        else:
            window = sg.Window('Selecionar empregado', select_employee_layout(employee_list))

            while True:
                event, values = window.read()

                if event == sg.WIN_CLOSED or event == "Voltar":
                    window.close(); del window
                    return False
                if event == 'Selecionar':
                    window.close(); del window
                    return employee_list[values['selected_employee']]

    def add_employee():
        window = sg.Window('Adicionar empregado', add_employee_layout())

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Voltar": break

            if event == 'syndicate':
                window['syn_text'].update(visible=True)
                window['taxa'].update(visible=True)

            if event == 'not_syndicate':
                window['syn_text'].update(visible=False)
                window['taxa'].update(visible=False)

            if values['type'] == 'Horista':
                window['t2'].update('Valor do salário hora:')
            else: window['t2'].update('Valor do salário mês:')

            if values['type'] == 'Comissionado':
                window['com'].update(visible=True)
            else:
                window['com'].update(visible=False)

            if event == 'Adicionar':
                name = values['name']
                cpf = values['cpf']
                syndicate = 'Syndicate' if values['syndicate'] else 'NoSyndicate'
                paymethod = values['paymethod']
                adress = (values['cep'], values['rua'], values['numero'], values['bairro'], values['cidade'], values['estado'])
                emplo_class = TYPES[values['type']]

                try: taxa = float(values['taxa']) if values['syndicate'] else None
                except ValueError: sg.popup('VALOR DA TAXA SINDICAL INVÁLIDO', title='ERRO')
                else:
                    try: salary = float(values['salary'])
                    except ValueError: sg.popup('VALOR DO SALÁRIO INVÁLIDO')
                    else:
                        try: comissao = float(values['comissao'])/100 if values['type'] == 'Comissionado' else None
                        except ValueError: sg.popup('VALOR DA COMISSÃO INVÁLIDO')
                        else:
                            if cpf == '' or cpf in Manager._employee_list.keys(): sg.popup('CPF JÁ CADASTRADO!', title='ERRO')
                            elif name == '': sg.popup('INSIRA UM NOME VÁLIDO', title='ERRO')
                            else:
                                employee = Person(name, cpf).create_employee(emplo_class, salary, paymethod, comissao)
                                employee.set_syndicate(syndicate, cpf, taxa)
                                employee.set_comissao(comissao)
                                employee.adress.set_all(*adress)
                                Manager.add_employee(cpf, employee)
                                sg.popup('Empregado adicionado')
                                break

        window.close(); del window

    def edit_employee(employee):

        manager = Manager()
        window = sg.Window('Editar empregado', edit_employee_layout(employee, manager._agendas), enable_close_attempted_event=True)

        while True:
            event, values = window.read()
            
            if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Voltar') and sg.popup_yes_no('Sair sem salvar?') == 'Yes':
                break

            if event == 'EXCLUIR EMPREGADO' and sg.popup_yes_no('Tem certeza que quer deletar o funcionário?') == 'Yes':
                if manager.del_employee(employee.cpf):
                    sg.popup('Funcionário removido')
                    break
                else: sg.popup('Não foi possível remover o funionário')

            if values['syndicate']:
                window['syn_text'].update(visible=True)
                window['taxa'].update(visible=True)
            else:
                window['syn_text'].update(visible=False)
                window['taxa'].update(visible=False)

            if values['type'] == 'Comissionado':
                window['com'].update(visible=True)
            else:
                window['com'].update(visible=False)

            if event == 'Salvar':
                name = values['name']
                emplo_class = TYPES[values['type']]
                paymethod = values['paymethod']
                syndicate = 'NoSyndicate' if not values['syndicate'] else 'Syndicate'
                adress = (values['cep'], values['rua'], values['numero'], values['bairro'], values['cidade'], values['estado'])
                taxa = None
                try:
                    comissao = float(values['comissao'])/100
                except ValueError:
                    sg.popup('VALOR DA COMISSÃO INVÁLIDO', title='ERRO')
                else:
                    if values['taxa'] != '':
                        try:
                            taxa = float(values['taxa'])
                        except ValueError:
                            sg.popup('VALOR DA TAXA SINDICAL INVÁLIDO', title='ERRO')
                        else:
                            new_employee = Person(name, employee.cpf).create_employee(emplo_class, employee.salary, paymethod, comissao)
                            new_employee.set_syndicate(syndicate, employee.cpf, taxa)
                            new_employee.adress.set_all(*adress)
                            new_employee.agenda = employee.agenda

                            if values['agenda'] != 'Não alterar':
                                agenda = values['agenda'].split('.')
                                agenda = int(agenda[0])
                                new_employee.set_agenda(manager._agendas[agenda])

                            manager.update_employee(employee.cpf, new_employee)
                            sg.popup('Alterações Salvas', title = 'Confirmação')
                            break

        window.close(); del window

    def undo():
        Manager.undo()

    def redo():
        Manager.redo()

    def reg_info(employee):

        window = sg.Window('Registrar informações', layout=reg_info_layout(employee), use_default_focus=False)
        manager = Manager()

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Voltar': break

            if event == 'ponto':
                manager.insert_his(employee)
                sg.popup('Ponto registrado', title='Ponto')
                break

            if event == 'venda':
                try:
                    sale = float(values['sale_value'])
                except:
                    sg.popup('VALOR DA VENDA INVÁLIDO', title='ERRO')
                else:
                    manager.insert_his(employee, sale)
                    sg.popup(f'Venda no valor de R${sale} registrada', title='Venda registrada')

            if event == 'Lançar':
                try:
                    serv_taxe = float(values['serv_taxe'])
                except:
                    sg.popup('VALOR DA TAXA INVÁLIDO', title='ERRO')
                else:
                    manager.insert_service_taxe(employee, serv_taxe)
                    sg.popup(f'Taxa de serviço no valor de R${serv_taxe} registrada', title='Taxa registrada')

        window.close(); del window

    def add_agenda():

        manager = Manager()
        window = sg.Window('Adicionar agenda', add_agenda_layout())

        while True:
            event, values = window.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Voltar': break

            if event == 'Adicionar':
                agenda = str(values['agenda'])

                name, *args = agenda.split(' ')

                name = name.capitalize()

                if name not in ['Semanal', 'Mensal']:
                    sg.popup('TIPO DE AGENDA INVÁLIDO', title='ERRO')
                else:
                    if name == 'Mensal':
                        if len(args) != 1:
                            sg.popup('INSIRA O DIA DO MÊS', title='ERRO')
                        else:
                            try:
                                args[0] = int(args[0])
                                if args[0] > 30 or args[0] < 1: raise ValueError
                            except ValueError:
                                sg.popup('DIA DO MÊS INVÁLIDO', title='ERRO')
                            else:
                                manager.add_agenda(create_agenda(name, *args))
                    else:
                        if len(args) != 2:
                            sg.popup('INSIRA A FREQUÊNCIA E O DIA DA SEMANA', title='ERRO')
                        else:
                            try:
                                args[0] = int(args[0])
                            except ValueError:
                                sg.popup('FREQUÊNCIA INVÁLIDA', title='ERRO')
                            else:
                                if args[1].lower() not in DAYS.keys():
                                    sg.popup('DIA DA SEMANA INVÁLIDO', title='ERRO')                       
                                else:
                                    args[1] = DAYS[args[1]]
                                    manager.add_agenda(create_agenda(name, *args))

        window.close(); del window

    def pay_schedule():

        manager = Manager()
        pending = manager.pending_pays()
        window = sg.Window('Folha de pagamento', pay_schedule_layout(pending, date.today().strftime("%d/%m/%Y")))

        while True:
            event, values = window.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Voltar': break

            if event == 'Pagar':

                for emplo in pending:
                    emplo.pay()
                sg.popup('Funcionários pagos')

        window.close(); del window