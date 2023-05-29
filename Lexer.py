from Table import Table

class Lexer:
    def __init__(self, table: Table):
        self.table = table
        self.stack = []

    def analizador_de_cadenas(self, cadena, tabla_parsing):
        tabla_action = tabla_parsing['action']
        tabla_goto = tabla_parsing['goto']
        pila = [0]
        cadena += '$'
        i = 0
        while True:
            estado = pila[-1]
            simbolo = cadena[i]

            if simbolo not in tabla_action[estado]:
                return False
            
            action, value = tabla_action[estado][simbolo]
            if value.startswith('shift'):
                pila.append(simbolo)
                estado_siguiente = int(value.split(' ')[1])
                pila.append(estado_siguiente)
                i += 1
            elif value.startswith('reduce'):
                head, body = value.split(' ')[1].split('->')
                for a in range(len(body) * 2):
                    pila.pop()
                estado = pila[-1]
                pila.append(head)
                pila.append(tabla_goto[estado][head])
            elif action == 'accept':
                return True
            else:
                return False
        
    def verificar_entrada(self):
        tabla_de_parsing = self.table.generar_tabla_parsing(self.table.grammar.producciones)
        while True:
            cadena_por_analizar = input("Ingrese la cadena: ")
            if cadena_por_analizar == "":
                break
            resultado_analizador = self.analizador_de_cadenas(cadena_por_analizar, tabla_de_parsing)
            if resultado_analizador:
                print('Si')
            else:
                print('No')



        
        

    
