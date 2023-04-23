import random as r
from lab_1.automaton.FiniteAutomaton import FiniteAutomaton


class Grammar(FiniteAutomaton):
    def __init__(self, VN, VT, P, S):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S
        self.string = self.S

    def generateWord(self):
        list_string = list(self.string)
        final = not any(x in list_string for x in self.VN)

        if final is False:
            for letter in self.string:
                if letter in self.VN:
                    self.string = self.string.replace(letter, self.P[letter][r.randint(0, len(self.P[letter]) - 1)])
                    return self.generateWord()
        else:
            return self.string

    def delete_string(self):
        self.string = self.S
        return self

    def toFiniteAutomaton(self):
        Q = set(self.VN + ['END'])
        Sigma = set(self.VT)
        delta = self.P_to_delta()
        q0 = 'S'
        F = {'END'}
        finite_automaton = FiniteAutomaton(Q=Q, Sigma=Sigma, delta=delta, q0=q0, F=F)
        return finite_automaton

    def P_to_delta(self):
        delta = {}

        for state, productions in self.P.items():
            transitions = {}
            for production in productions:
                if len(production) == 1:
                    transitions[production] = 'END'
                else:
                    transitions[production[0]] = production[1:]
            delta[state] = transitions
        delta['END'] = {'END': ''}
        return delta

    def classify_grammar(self):
        unrestricted = True
        context_sensitive = True
        context_free = True
        regular = True
        regular_left = True
        regular_right = True

        for state, productions in self.P.items():
            for production in productions:
                # check if the grammar exist
                for char in production:
                    if char not in self.VT + self.VN:
                        unrestricted, context_sensitive, context_free, regular, regular_left, regular_right = False
                        return f"The {char} does not belong to this grammar."

                for char in state:
                    if char not in self.VT + self.VN:
                        unrestricted, context_sensitive, context_free, regular, regular_left, regular_right = False
                        return f"The {char} is not in grammar"

                # check if type 1 or 0
                if (len(production) > 2 or len(state) > 1) and any([state_v in self.VN for state_v in state]):
                    context_free, regular, regular_left, regular_right = False

                # check type 1
                if any([ch in self.VN for ch in state]):
                    print("", end='')
                else:
                    context_sensitive, context_free, regular, regular_left, regular_right = False

                # type 2 or 3
                if len(production) <= 2 and len(state) == 1 and context_free:
                    if any([char_r in self.VN or len(char_r) == 0 for char_r in [production[1:]]]):
                        print("", end='')
                    else:
                        regular_right = False

                    if any([char_l in self.VN or len(char_l) == 0 for char_l in [production[0:1]]]):
                        print("", end='')
                    else:
                        regular_left = False

        if regular_left or regular_right:
            print(f"Regular(type 3)")
        elif context_free:
            print(f"Context-free(type 2)")
        elif context_sensitive:
            print(f"Context-sensitive(type 1)")
        elif unrestricted:
            print(f"Unrestricted(type 0)")

    def getNewVariable(self):
        n = 0
        while f'X{n + 1}' in self.VN:
            n += 1
        return f'X{n + 1}'

    def toChomskyNormalForm(self):
        self.eliminateEpsilonProductions()
        self.eliminateUnitProductions()
        self.eliminateInaccessibleSymbols()
        self.eliminateNonproductiveSymbols()
        self.eliminateLongProductions()

    def eliminateEpsilonProductions(self):
        # Find all nullable symbols
        nullable = set()
        for state in self.P:
            if 'epsilon' in self.P[state]:
                nullable.add(state)

        # Generate new productions without nullable symbols
        new_productions = {}
        for state in self.P:
            new_productions[state] = []
            for production in self.P[state]:
                if production == 'epsilon':
                    continue

                # Generate all combinations of production symbols
                combinations = [[]]
                for symbol in production:
                    if symbol in nullable:
                        # Add both possibilities (symbol present, symbol removed)
                        new_combinations = []
                        for comb in combinations:
                            new_combinations.append(comb + [symbol])
                            new_combinations.append(comb)
                        combinations = new_combinations
                    else:
                        # Add symbol to all combinations
                        for comb in combinations:
                            comb.append(symbol)
                # Add new productions to new_productions dict
                for comb in combinations:
                    if comb:
                        new_production = ''.join(comb)
                        if new_production not in new_productions[state]:
                            new_productions[state].append(new_production)

        # Add new productions generated by nullable symbols
        for state in self.P:
            for production in self.P[state]:
                for symbol in nullable:
                    if symbol in production and len(production) != 1:
                        new_production = production.replace(symbol, '')
                        if new_production not in new_productions[state]:
                            new_productions[state].append(new_production)

        # Update grammar with new productions
        self.P = new_productions

    def eliminateUnitProductions(self):
        new_productions = {}
        for state, productions in self.P.items():
            new_productions[state] = productions
        # Eliminate all unit productions except loops
        for state in self.P.keys():
            productions = new_productions[state]
            for production in productions:
                if len(production) == 1 and production.isupper():
                    # A unit production
                    unit_state = production
                    for unit_production in new_productions[unit_state]:
                        if unit_production != state and unit_production not in new_productions[state]:
                            new_productions[state].append(unit_production)
        # Eliminate loops
        for state in self.P.keys():
            productions = new_productions[state]
            if state in productions:
                new_productions[state].remove(state)
                for unit_production in new_productions[state]:
                    if unit_production != state and unit_production not in new_productions[state]:
                        new_productions[state].append(unit_production)
        # Remove all unit productions
        for state, productions in new_productions.items():
            new_productions[state] = [production for production in productions if
                                      len(production) > 1 or not production.isupper()]
        self.P = new_productions

    def eliminateInaccessibleSymbols(self):
        reachable = set()
        # Add the start symbol to the set of reachable symbols
        reachable.add(self.S)

        # Iterate through the productions and add any symbols that can be reached
        # from the start symbol
        while True:
            old_size = len(reachable)

            for state, productions in self.P.items():
                if state in reachable:
                    for production in productions:
                        for symbol in production:
                            if symbol in self.VN:
                                reachable.add(symbol)

            # Check if there are any new symbols that were added to the set of reachable symbols
            if len(reachable) == old_size:
                break

        # Find the set of inaccessible symbols
        inaccessible = set(self.VN) - reachable

        # Remove the productions involving inaccessible symbols
        new_productions = {}
        for state, productions in self.P.items():
            if state not in inaccessible:
                new_productions[state] = []
                for production in productions:
                    if not any(symbol in inaccessible for symbol in production):
                        new_productions[state].append(production)

        # Update the grammar with the new set of productions and non-terminals
        self.P = new_productions
        self.VN = reachable

        return Grammar(self.VN, self.VT, self.P, self.S)

    def eliminateNonproductiveSymbols(self):
        productive = {self.S}
        changed = True
        while changed:
            changed = False
            for state, productions in self.P.items():
                for production in productions:
                    if all(s in productive for s in production):
                        if state not in productive:
                            productive.add(state)
                            changed = True
        nonproductive = set(self.VN) - productive
        new_productions = {}
        for state, productions in self.P.items():
            new_productions[state] = [p for p in productions if all(s not in nonproductive for s in p)]
        # Check if 'S' has an empty string production and remove it if it does
        if '' in new_productions[self.S]:
            new_productions[self.S].remove('')
        return Grammar(list(productive), self.VT, new_productions, self.S)

    def clone(self):
        return Grammar(self.VN, self.VT, self.P, self.S)

    def eliminateLongProductions(self):
        for state in self.P:
            self.P[state].sort(key=len)
        new_P = self.P.copy()
        new_VN = self.VN.copy()
        new_VT = self.VT.copy()
        new_S = self.S
        new_grammar = Grammar(new_VN, new_VT, new_P, new_S)
        list_of_terminals_changed = []
        terminal_and_variable = {}
        for state in self.P:
            productions = self.P[state]
            productions_copy = self.P[state]
            for index, production in enumerate(productions):
                if len(production) == 1:
                    productions_copy[index] = production
                elif len(production) == 2:
                    variables = list(production)
                    if len(variables) == 2:
                        # check if the first variable is a terminal and the second is a variable
                        if production[0] in self.VT and production[1] in self.VN:
                            # check if the terminal has already been changed
                            if production[0] in list_of_terminals_changed:
                                productions_copy[index] = (terminal_and_variable[production[0]], production[1])
                            # if the terminal has not been changed, change it
                            else:
                                var1 = variables.pop(0)  # removes the first variable from the list
                                new_var = new_grammar.getNewVariable()
                                new_grammar.VN.add(new_var)
                                new_grammar.P[new_var] = var1
                                list_of_terminals_changed.append(var1)
                                terminal_and_variable[var1] = new_var
                                variables.insert(0, new_var)
                                productions_copy[index] = (tuple(variables))
                        # check if the first variable is a variable and the second is a terminal
                        elif production[0] in self.VN and production[1] in self.VT:
                            # check if the terminal has already been changed
                            if production[1] in list_of_terminals_changed:
                                productions[index] = (production[0], terminal_and_variable[production[1]])
                            else:
                                var2 = variables.pop(1)  # removes the second variable from the list
                                new_var = new_grammar.getNewVariable()
                                new_grammar.VN.add(new_var)
                                new_grammar.P[new_var] = var2
                                list_of_terminals_changed.append(var2)
                                variables.insert(0, new_var)
                                productions_copy[index] = (tuple(variables))
                        elif production[0] in self.VT and production[1] in self.VT:
                            if production[0] in list_of_terminals_changed and production[1] in \
                                    list_of_terminals_changed:
                                new_grammar.P[index] = [
                                    (terminal_and_variable[production[0]], terminal_and_variable[production[1]])]
                                productions_copy[index] = (new_grammar.P[index])
                            elif production[0] in list_of_terminals_changed and production[1] not in \
                                    list_of_terminals_changed:
                                var2 = variables.pop(1)
                                new_var = new_grammar.getNewVariable()
                                new_grammar.VN.add(new_var)
                                new_grammar.P[new_var] = var2
                                list_of_terminals_changed.append(var2)
                                variables.insert(0, new_var)
                                new_grammar.P[index] = [(terminal_and_variable[production[0]], production[1])]
                                productions_copy[index] = (tuple(variables))
                            elif production[0] not in list_of_terminals_changed and production[1] in \
                                    list_of_terminals_changed:
                                var1 = variables.pop(0)
                                new_var = new_grammar.getNewVariable()
                                new_grammar.VN.add(new_var)
                                new_grammar.P[new_var] = var1
                                list_of_terminals_changed.append(var1)
                                variables.insert(0, new_var)
                                new_grammar.P[index] = [(production[0], terminal_and_variable[production[1]])]
                                productions_copy[index] = (tuple(variables))
                            else:
                                var1 = variables.pop(0)
                                var2 = variables.pop(0)  # removes the second variable from the list
                                new_var = new_grammar.getNewVariable()
                                new_grammar.VN.add(new_var)
                                new_grammar.P[new_var] = [(var1, var2)]
                                variables.insert(0, new_var)  # inserts the new variable at the beginning
                                # adds a new production that uses the current state and the remaining variables
                                productions_copy[index] = (tuple(variables))

                        elif production[0] in self.VN and production[1] in self.VN:
                            productions_copy[index] = (production)
                    else:
                        break
                elif len(production) > 2:
                    # Replace with new variables and productions
                    variables = list(production)
                    while len(variables) > 2:
                        var1 = variables.pop(0)  # removes the first variable from the list
                        var2 = variables.pop(0)  # removes the second variable from the list
                        # if var1 is terminal
                        if var1 in new_grammar.VT:
                            # if var1 is a terminal and in list of terminals changed
                            if var1 in list_of_terminals_changed:
                                gata = False
                                # for var1 terminal in list and var2 variable
                                if var2 in new_grammar.VN:
                                    for i in range(len(new_grammar.P)):
                                        if gata == False:
                                            keys = [k for k, v in new_grammar.P.items() if
                                                    v == [terminal_and_variable[var1], var2]]
                                            if keys != []:
                                                key = ''.join(keys)
                                                variables.insert(0, key)
                                                productions_copy[index] = key
                                                gata = True
                                            # if [terminal_and_variable[var1], var2] != list(new_grammar.P)[i]:
                                            else:
                                                new_var = new_grammar.getNewVariable()
                                                new_grammar.VN.add(new_var)
                                                new_grammar.P[new_var] = [terminal_and_variable[var1], var2]
                                                variables.insert(0, new_var)
                                                productions_copy[index] = (tuple(variables))
                                                gata = True
                                # for var1 terminal in list and var2 terminal
                                elif var2 in new_grammar.VT:
                                    if var2 in list_of_terminals_changed:
                                        gata = False
                                        for i in range(len(new_grammar.P)):
                                            if gata == False:
                                                keys = [k for k, v in new_grammar.P.items() if
                                                        v == [terminal_and_variable[var1], terminal_and_variable[var2]]]
                                                if keys != []:
                                                    key = ''.join(keys)
                                                    variables.insert(0, key)
                                                    productions_copy[index] = key
                                                    gata = True

                                                else:
                                                    new_var = new_grammar.getNewVariable()
                                                    new_grammar.VN.add(new_var)
                                                    new_grammar.P[new_var] = [terminal_and_variable[var1],
                                                                              terminal_and_variable[var2]]
                                                    variables.insert(0, new_var)
                                                    productions_copy[index] = (tuple(variables))
                                                    gata = True
                                    elif var2 not in list_of_terminals_changed:
                                        # change var2 with new variable
                                        new_var2 = new_grammar.getNewVariable()
                                        new_grammar.VN.add(new_var2)
                                        new_grammar.P[new_var2] = var2
                                        list_of_terminals_changed.append(var2)
                                        terminal_and_variable[var2] = new_var2
                                        variables.insert(0, new_var2)
                                        productions_copy[index] = (tuple(variables))
                                        # add new production of var1 and new var2
                                        new_var = new_grammar.getNewVariable()
                                        new_grammar.VN.add(new_var)
                                        new_grammar.P[new_var] = [terminal_and_variable[var1],
                                                                  terminal_and_variable[var2]]
                                        variables.insert(0, new_var)
                                        productions_copy[index] = (tuple(variables))
                                        gata = True
                            #
                            # for var1 terminal not in list
                            elif var1 not in list_of_terminals_changed:
                                new_var = new_grammar.getNewVariable()
                                new_grammar.VN.add(new_var)
                                new_grammar.P[new_var] = var1
                                list_of_terminals_changed.append(var1)
                                terminal_and_variable[var1] = new_var
                                variables.insert(0, new_var)
                                productions_copy[index] = (tuple(variables))
                                gata = False
                                # for var1 terminal not in list and var2 variable
                                if var2 in new_grammar.VN:
                                    for i in range(len(new_grammar.P)):
                                        if gata == False:
                                            # if var1 was not changed then there was no combination of var1 and var2
                                            new_var = new_grammar.getNewVariable()
                                            new_grammar.VN.add(new_var)
                                            new_grammar.P[new_var] = [terminal_and_variable[var1], var2]
                                            variables.insert(0, new_var)
                                            productions_copy[index] = (tuple(variables))
                                            gata = True
                                # for var1 terminal not in list and var2 terminal
                                elif var2 in new_grammar.VT:
                                    # var2 was changed
                                    if var2 in list_of_terminals_changed:
                                        gata = False
                                        for i in range(len(new_grammar.P)):
                                            if gata == False:
                                                keys = [k for k, v in new_grammar.P.items() if
                                                        v == [terminal_and_variable[var1], terminal_and_variable[var2]]]
                                                if keys != []:
                                                    key = ''.join(keys)
                                                    variables.insert(0, key)
                                                    productions_copy[index] = key
                                                    gata = True

                                                else:
                                                    new_var = new_grammar.getNewVariable()
                                                    new_grammar.VN.add(new_var)
                                                    new_grammar.P[new_var] = [terminal_and_variable[var1],
                                                                              terminal_and_variable[var2]]
                                                    variables.insert(0, new_var)
                                                    productions_copy[index] = (tuple(variables))
                                                    gata = True
                                    elif var2 not in list_of_terminals_changed:
                                        # change var2 with new variable
                                        new_var2 = new_grammar.getNewVariable()
                                        new_grammar.VN.add(new_var2)
                                        new_grammar.P[new_var2] = var2
                                        list_of_terminals_changed.append(var2)
                                        terminal_and_variable[var2] = new_var2
                                        variables.insert(0, new_var2)
                                        productions_copy[index] = (tuple(variables))
                                        # add new production of var1 and new var2
                                        new_var = new_grammar.getNewVariable()
                                        new_grammar.VN.add(new_var)
                                        new_grammar.P[new_var] = [terminal_and_variable[var1],
                                                                  terminal_and_variable[var2]]
                                        variables.insert(0, new_var)
                                        productions_copy[index] = (tuple(variables))
                                        gata = True

                        if var1 in new_grammar.VN: # for var1 variable
                            gata = False
                            # for var1 variable and var2 variable
                            if var2 in new_grammar.VN:
                                for i in range(len(new_grammar.P)):
                                    if gata == False:
                                        keys = [k for k, v in new_grammar.P.items() if
                                                v == [var1, var2]]
                                        if keys != []:
                                            key = ''.join(keys)
                                            variables.insert(0, key)
                                            productions_copy[index] = key
                                            gata = True

                                        else:
                                            new_var = new_grammar.getNewVariable()
                                            new_grammar.VN.add(new_var)
                                            new_grammar.P[new_var] = [var1, var2]
                                            variables.insert(0, new_var)
                                            productions_copy[index] = (tuple(variables))
                                            gata = True
                            if var2 in new_grammar.VT:
                                if var2 in list_of_terminals_changed:
                                    gata = False
                                    for i in range(len(new_grammar.P)):
                                        if gata == False:
                                            keys = [k for k, v in new_grammar.P.items() if v == [var1, terminal_and_variable[var2]]]
                                            if keys != []:
                                                key = ''.join(keys)
                                                variables.insert(0, key)
                                                productions_copy[index] = key
                                                gata = True
                                            else:
                                                if gata == False:
                                                    new_var = new_grammar.getNewVariable()
                                                    new_grammar.VN.add(new_var)
                                                    new_grammar.P[new_var] = [var1, terminal_and_variable[var2]]
                                                    variables.insert(0, new_var)
                                                    productions_copy[index] = (tuple(variables))
                                                    gata = True
                                elif var2 not in list_of_terminals_changed:
                                    # change var2 with new variable
                                    new_var2 = new_grammar.getNewVariable()
                                    new_grammar.VN.add(new_var2)
                                    new_grammar.P[new_var2] = var2
                                    list_of_terminals_changed.append(var2)
                                    terminal_and_variable[var2] = new_var2
                                    variables.insert(0, new_var2)
                                    productions_copy[index] = (tuple(variables))
                                    # add new production of var1 and new var2
                                    new_var = new_grammar.getNewVariable()
                                    new_grammar.VN.add(new_var)
                                    new_grammar.P[new_var] = [var1, new_var2]
                                    variables.insert(0, new_var)
                                    productions_copy[index] = (tuple(variables))
                                    gata = True

                    # adds a new production that uses the current state and the remaining variables
                    productions_copy[index] = (tuple(variables))
                else:
                    productions_copy[index] = production  # add the production as is
            new_grammar.P[state] = productions_copy  # Update the grammar with the new productions
        return new_grammar
