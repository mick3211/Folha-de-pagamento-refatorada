# Folha-de-pagamento-refatorada
Disciplina projeto de software UFAL 2020.2

Code smells:

1. Long method na classe Person, métodos get_adres, get_info, set_adress, set_info
2. Feature envy na classe Person, métodos get e set adress
3. Primitive obsession para definir agendas
4. Duplicated code na classes filhas de Person, método clear_his
5. Long method na classe Sys, método undo
6. Long method na classe Person, método set_next_payday
7. Primitive obsession para definir sindicato

Refatorações:

1. métodos removidos
2. Métodos movidos para a classe Adress (move method)
3. Replace array with object para agenda
4. Histórico transformado em objeto (extract class)
5. Padrão State utilizado
6. Padrão Strategy utilizado
7. Sindicato tranformado em objeto (Replace data value with object) e classe NoSyndicate criada (Introduce Null Object)
