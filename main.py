from Grammar import Grammar
from Table import Table
from Lexer import Lexer


def procesar_gramatica():
    print("Ingrese la gramatica")
    grammar = Grammar()
    linea = input().split(" ")
    string = ""
    linea = string.join(linea)
    while linea:
        grammar.add_productions(linea)
        left, right = linea.split("->")
        right = right.split("|")
        if grammar.start is None:
            grammar.start = left
        grammar.add_rule(left, right)
        grammar.add_terminals(right)
        grammar.add_Nterminals(left)
        linea = input().split(" ")
        string = ""
        linea = string.join(linea)

    print("Producciones: ", grammar.producciones)

    conjuntos_item = grammar.conjunto_item(grammar.producciones)
    for i, conjunto_de_item in enumerate(conjuntos_item):
        print(f"Item set {i}:")
        for item in conjunto_de_item:
            print(f" {item}")

    estado, transiciones = grammar.generar_LR0(grammar.producciones)
    for i, state in enumerate(estado):
        print(f'Estados {i}:')
        for item in state:
            print(f' {item}')
    print('Transiciones:')
    for transicion in transiciones:
        print(f' {transicion}')
    
    table = Table(grammar)
    table.print_table()

    lexer = Lexer(table)
    lexer.verificar_entrada()

if __name__ == "__main__":
    procesar_gramatica()