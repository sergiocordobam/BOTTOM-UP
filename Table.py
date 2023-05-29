from Grammar import Grammar


class Table:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.table = {}

    def generar_tabla_parsing(self, producciones):
        producciones = self.grammar.producciones
        produccion_inicial = producciones[0]
        simbolo_inicial = produccion_inicial.split('->')[0]
        estados, transiciones = self.grammar.generar_LR0(producciones)
        terminals = list(self.grammar.terminals) + ['$']
        no_terminales = list(self.grammar.Nterminals)
        funcion_de_action = {}
        funcion_de_goto = {}

        for i, estado in enumerate(estados):
            funcion_de_action[i] = {}
            funcion_de_goto[i] = {}

            for item in estado:
                left, right = item.split('->')
                punto_del_item = right.index('.')
                
                if punto_del_item + 1 == len(right):
                    siguiente_simbolo = None
                else:
                    siguiente_simbolo = right[punto_del_item + 1]

                if siguiente_simbolo is None:
                    if left == f"{simbolo_inicial}'":
                        funcion_de_action[i]['$'] = ('accept', '')
                    else:
                        production_index = producciones.index(f'{left}->{right[:-1]}')
                        for terminal in terminals:
                            funcion_de_action[i][terminal] = (f'r{production_index}', f'reduce {left}->{right[:-1]}')
                elif siguiente_simbolo in terminals:
                    estado_siguiente = self.grammar.goto(estado, siguiente_simbolo, producciones)
                    indice_estado_siguiente = estados.index(estado_siguiente)
                    funcion_de_action[i][siguiente_simbolo] = (f's{indice_estado_siguiente}', f'shift {indice_estado_siguiente}')
                elif siguiente_simbolo in no_terminales:
                    estado_siguiente = self.grammar.goto(estado, siguiente_simbolo, producciones)
                    indice_estado_siguiente = estados.index(estado_siguiente)
                    funcion_de_goto[i][siguiente_simbolo] = indice_estado_siguiente

        return {'action': funcion_de_action, 'goto': funcion_de_goto}
    
    def print_table(self):
        print("\nTabla:")
        parsing_table = self.generar_tabla_parsing(self.grammar.producciones)
        action_table = parsing_table['action']
        goto_table = parsing_table['goto']

        for estado in sorted(action_table.keys()):
            print(f' Estado {estado}:')
            for simbolo, accion in action_table[estado].items():
                print(f'  action[{estado}][{simbolo}] = {accion}')

            for simbolo, siguiente_estado in goto_table[estado].items():
                print(f'  goto[{estado}][{simbolo}] = {siguiente_estado}')