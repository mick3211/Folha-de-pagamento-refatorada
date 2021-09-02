import PySimpleGUI as sg
from layouts.add_employee import add_employee_layout
from classes.person import Person
from classes.manage import Manager


TYPES = {'Assalariado': 'Salaried', 'Comissionado': 'Commisioned', 'Horista': 'Hourly'}


class Menu():

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

                try: emplo_class = TYPES[values['type']]
                except KeyError: sg.popup('TIPO INVÁLIDO', title='ERRO')
                else:
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
                                    employee.adress.set_all(*adress)
                                    Manager.add_employee(cpf, employee)
                                    sg.popup('Empregado adicionado')
                                    break

        window.close(); del window