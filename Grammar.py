import re

class Grammar:
    def __init__(self):
        self.rules = {}
        self.terminals = {}
        self.Nterminals = {}
        self.first = {}
        self.follow = {}
        self.start = None
        self.producciones = []
    
    def add_rule(self, left, right):
        if left not in self.rules:
            self.rules[left] = []
        self.rules[left] += right

    def add_terminals(self, right):
        for element in right:
            if element == "epsilon":
                continue
            caracter = re.findall("[a-z0-9\+\/\*\-\%\=\(\)]", element)
            for token in caracter:
                self.terminals[token] = token

    def add_Nterminals(self, left):
        self.Nterminals[left] = left

    def add_productions(self, production):
        left, right = production.split("->")
        right = right.split("|")
        for element in right:
            self.producciones.append(f"{left}->{element}")

    def closure(self, I, productions):
        J = I.copy()
        añadido = True
        while añadido:
            añadido = False
            for item in J:
                left, right = item.split("->")
                punto_del_item = right.index(".")
                if punto_del_item + 1 < len(right) and right[punto_del_item + 1] in self.Nterminals:
                    next_Nterminal = right[punto_del_item + 1]
                    for production in productions:
                        if production.startswith(next_Nterminal):
                            new_item = production.replace("->", "->.")
                            if new_item not in J:
                                J.append(new_item)
                                añadido = True
            if not añadido:
                break
        return J

    def goto(self, I, X, productions):
        items_nuevos = []
        for item in I:
            left, right = item.split("->")
            punto_en_item = right.index(".")
            if punto_en_item < len(right) - 1 and right[punto_en_item + 1] == X:
                nuevo_item = left + "->" + right[:punto_en_item] + X + "." + right[punto_en_item + 2:]
                items_nuevos.append(nuevo_item)
        return self.closure(items_nuevos, productions)

    def conjunto_item(self, productions):
        conjunto_de_itemes = []
        produccion_inicial = productions[0]
        simbolo_inicial = produccion_inicial.split("->")[0]
        conjunto_item_inicial = self.closure([f"{simbolo_inicial}'->.{simbolo_inicial}"], productions)
        conjunto_de_itemes.append(conjunto_item_inicial)

        symbols = [simbolo_inicial]
        for production in productions:
            left, right = production.split("->")
            for symbol in right:
                if symbol != "." and symbol not in symbols:
                    symbols.append(symbol)

        while True:
            añadido = False
            for item_set in conjunto_de_itemes:
                for symbol in symbols:
                    new_item_set = self.goto(item_set, symbol, productions)
                    if new_item_set and new_item_set not in conjunto_de_itemes:
                        conjunto_de_itemes.append(new_item_set)
                        añadido = True
            if not añadido:
                break
        return conjunto_de_itemes

    def generar_LR0(self, productions):
        produccion_inicial = productions[0]
        simbolo_inicial = produccion_inicial.split("->")[0]
        estado_inicial = self.closure([f"{simbolo_inicial}'->.{simbolo_inicial}"], productions)
        estados = [estado_inicial]
        transiciones = []

        symbols = [simbolo_inicial]
        for production in productions:
            left, right = production.split("->")
            for symbol in right:
                if symbol != "." and symbol not in symbols:
                    symbols.append(symbol)

        while True:
            añadido = False
            for state in estados:
                for symbol in symbols:
                    nuevo_estado = self.goto(state, symbol, productions)
                    if nuevo_estado:
                        if nuevo_estado not in estados:
                            estados.append(nuevo_estado)
                            añadido = True
                        transition = (estados.index(state), symbol, estados.index(nuevo_estado))
                        transiciones.append(transition)
            if not añadido:
                break
        return estados, transiciones


