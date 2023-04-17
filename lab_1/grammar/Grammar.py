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
                print("start", combinations, 'end')
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
##------
    def eliminateLongProductions(self):
        new_grammar = self.clone()
        list_of_terminals_changed = []
        terminal_and_variable = {}
        for state in self.P:
            productions = self.P[state]
            for index, production in enumerate(productions):
                print(production, "production")
                print(len(production), "len")
                if len(production) == 2:
                    variables = list(production)
                    print(variables, "variables2")
                    print(len(variables), "len2")
                    if len(variables) == 2:
                        print("hi")
                        # check if the first variable is a terminal and the second is a variable
                        if production[0] in self.VT and production[1] in self.VN:
                            # check if the terminal has already been changed
                            if production[0] in list_of_terminals_changed:
                                print(production[0], "production[0]")
                                print(terminal_and_variable[production[0]], "terminal_and_variable[production[0]]")
                                new_grammar.P[state] = [(terminal_and_variable[production[0]], production[1])]
                                print(new_grammar.P[state])

                                productions[index] = (new_grammar.P[state])
                                print(production[index], "production[index]")
                                print(production)
                            # if the terminal has not been changed, change it
                            else:
                                print("hi2")
                                var1 = variables.pop(0)  # removes the first variable from the list
                                new_var = new_grammar.getNewVariable()
                                new_grammar.VN.add(new_var)
                                new_grammar.P[new_var] = [(var1)]
                                list_of_terminals_changed.append(var1)
                                terminal_and_variable[var1] = [new_var]
                                variables.insert(0, new_var)
                                print(variables, "variables3")
                                productions[index] = (tuple(variables))
                                print('hi3')
                        # check if the first variable is a variable and the second is a terminal
                        elif production[0] in self.VN and production[1] in self.VT:
                            # check if the terminal has already been changed
                            if production[1] in list_of_terminals_changed:
                                new_grammar.P[index] = [(production[0], terminal_and_variable[production[1]])]
                                productions[index] = (new_grammar.P[state])
                                print(production[index], "production[index]")
                            else:
                                var2 = variables.pop(1)  # removes the second variable from the list
                                new_var = new_grammar.getNewVariable()
                                new_grammar.VN.add(new_var)
                                new_grammar.P[new_var] = [var2]
                                list_of_terminals_changed.append(var2)
                                variables.insert(0, new_var)
                                productions[index] = (tuple(variables))
                        elif production[0] in self.VT and production[1] in self.VT:
                            if production[0] in list_of_terminals_changed and production[1] in list_of_terminals_changed: # -----------------------------------------
                                new_grammar.P[index] = [(terminal_and_variable[production[0]], terminal_and_variable[production[1]])]
                                productions[index] = (new_grammar.P[index])
                            elif production[0] in list_of_terminals_changed and production[1] not in list_of_terminals_changed:
                                var2 = variables.pop(1)
                                new_var = new_grammar.getNewVariable()
                                new_grammar.VN.add(new_var)
                                new_grammar.P[new_var] = [(var2)]
                                list_of_terminals_changed.append(var2)
                                variables.insert(0, new_var)
                                new_grammar.P[index] = [(terminal_and_variable[production[0]], production[1])]
                                productions[index] = (tuple(variables))
                            elif production[0] not in list_of_terminals_changed and production[1] in list_of_terminals_changed:
                                var1 = variables.pop(0)
                                new_var = new_grammar.getNewVariable()
                                new_grammar.VN.add(new_var)
                                new_grammar.P[new_var] = [(var1)]
                                list_of_terminals_changed.append(var1)
                                variables.insert(0, new_var)
                                new_grammar.P[index] = [(production[0], terminal_and_variable[production[1]])]
                                productions[index] = (tuple(variables))
                            else:
                                var1 = variables.pop(0)
                                var2 = variables.pop(0)  # removes the second variable from the list
                                new_var = new_grammar.getNewVariable()
                                new_grammar.VN.add(new_var)
                                new_grammar.P[new_var] = [(var1, var2)]
                                variables.insert(0, new_var)  # inserts the new variable at the beginning
                                # adds a new production that uses the current state and the remaining variables
                                productions[index] = (tuple(variables))

                        elif production[0] in self.VN and production[1] in self.VN:
                            break
                    else:
                        break
                elif len(production) > 2:
                    # Replace with new variables and productions
                    variables = list(production)
                    while len(variables) > 2:
                        print(variables,"variables")
                        print(len(variables), "len")
                        for i in range(len(variables)):
                            if production[i] in self.VT and production[i] not in list_of_terminals_changed:
                                var1 = variables.pop(i)
                                new_var = new_grammar.getNewVariable()
                                new_grammar.VN.add(new_var)
                                new_grammar.P[new_var] = [(var1)]
                                list_of_terminals_changed.append(var1)
                                terminal_and_variable[var1] = [new_var]
                                print(terminal_and_variable[var1], "terminal_and_variable")

                                variables.insert(0, new_var)
                                productions[index] = (tuple(variables))
                            elif production[i] in self.VT and production[i] in list_of_terminals_changed:
                                new_grammar.P[state] = [(terminal_and_variable[production[i]])]
                                productions[index] = (new_grammar.P[state])
                            # else:
                            #     new_grammar.P[index] = [(terminal_and_variable[production[0]], production[1])]
                        var1 = variables.pop(0)  # removes the first variable from the list
                        var2 = variables.pop(0)  # removes the second variable from the list
                        new_var = new_grammar.getNewVariable()
                        new_grammar.VN.add(new_var)
                        new_grammar.P[new_var] = [(var1, var2)]
                        variables.insert(0, new_var)  # inserts the new variable at the beginning
                    # adds a new production that uses the current state and the remaining variables
                    productions[index] = (tuple(variables))
                else:
                    productions[index] = production  # add the production as is
            new_grammar.P[state] = productions  # Update the grammar with the new productions
            print(variables, "variables")
        return new_grammar

    # def CNF(self):
    #     # Step 1: Find all epsilon production
    #     nullable_vars = set()
    #     for var in self.VN:
    #         if "" in self.P[var]:
    #             nullable_vars.add(var)
    #     print(nullable_vars)
    #
    #     # Step 2: Eliminate all epsilon productions
    #     new_productions = self.P.copy()
    #     for var in self.VN:
    #         new_rhs = []
    #         for symbol in self.P[var]:
    #             if symbol == "":
    #                 # Skip the empty string production
    #                 continue
    #             rhs_combinations = [[]]
    #             for rhs_symbol in symbol:
    #                 if rhs_symbol in nullable_vars:
    #                     # Add both possibilities: with and without the nullable symbol
    #                     new_rhs_combinations = []
    #                     for combination in rhs_combinations:
    #                         new_rhs_combinations.append(combination + [rhs_symbol])
    #                         new_rhs_combinations.append(combination)
    #                     rhs_combinations = new_rhs_combinations
    #                 else:
    #                     # Add the symbol to all existing combinations
    #                     for combination in rhs_combinations:
    #                         combination.append(rhs_symbol)
    #             for combination in rhs_combinations:
    #                 new_rhs.append("".join(combination))
    #         new_productions[var] = new_rhs
    #     print('new productions', new_productions)
    #     print(new_productions)
    #
    #     # Step 1: Find all unit productions
    #     unit_productions = {}
    #     for var in self.VN:
    #         for rhs in self.P[var]:
    #             if len(rhs) == 1 and rhs[0] in self.VN:
    #                 if var in unit_productions:
    #                     unit_productions[var].append(rhs[0])
    #                 else:
    #                     unit_productions[var] = [rhs[0]]
    #     print(unit_productions)
    #
    #     # Step 2: Generate new productions without unit productions
    #     # new_productions = (self.P.copy())
    #     for var in unit_productions:
    #         for rhs_var in unit_productions[var]:
    #             # Only consider non-unit productions for the rhs variable
    #             rhs = new_productions[rhs_var]
    #             while True:
    #                 new_rhs = []
    #                 for symbol in rhs:
    #                     if len(symbol) == 1 and symbol[0] in self.VN and symbol[0] != var:
    #                         # Expand unit productions for this symbol
    #                         new_rhs.extend(new_productions[symbol[0]])
    #                     else:
    #                         new_rhs.append(symbol)
    #                 if new_rhs == rhs:
    #                     break
    #                 rhs = new_rhs
    #             new_productions[var].extend(rhs)
    #     print('n', new_productions)
    #
    #     # Step 3: Remove unit productions
    #     for var in unit_productions:
    #         new_productions[var] = [rhs for rhs in new_productions[var] if
    #                                 len(rhs) != 1 or rhs[0] not in unit_productions]
    #     print(new_productions)
    #
    #     # Step 4: Eliminate inaccessible symbols
    #     reachable_vars = set([self.S])
    #     new_reachable_vars = set([self.S])
    #     while True:
    #         for var in new_reachable_vars:
    #             for rhs in new_productions[var]:
    #                 for symbol in rhs:
    #                     if symbol in self.VN:
    #                         reachable_vars.add(symbol)
    #         if new_reachable_vars == reachable_vars:
    #             break
    #         new_reachable_vars = reachable_vars.copy()
    #
    #     # Step 5: Create new grammar object and return it
    #     new_P = {var: new_productions[var] for var in reachable_vars}
    #     new_S = self.S if self.S not in nullable_vars else "NEW_START"
    #     new_P[new_S] = [self.S, ""] if self.S in nullable_vars else [self.S]
    #     print(new_P)
    #     return self.__class__(self.VT, list(reachable_vars) + ([new_S] if new_S != self.S else []), new_P, self.S)
    #
    # def convert_to_cnf(self):
    #     # Step 1: Eliminate epsilon productions
    #     new_productions = {}
    #     for non_terminal in self.P:
    #         new_productions[non_terminal] = []
    #         for production in self.P[non_terminal]:
    #             if production == '':
    #                 continue
    #             new_productions[non_terminal].append(production)
    #
    #     # Generate all possible combinations of productions that derive the empty string
    #     empty_combinations = {}
    #     for non_terminal in new_productions:
    #         empty_combinations[non_terminal] = set()
    #         if '' in new_productions[non_terminal]:
    #             empty_combinations[non_terminal].add('')
    #
    #     while True:
    #         updated = False
    #         for non_terminal in new_productions:
    #             for production in new_productions[non_terminal]:
    #                 for i, symbol in enumerate(production):
    #                     if symbol in empty_combinations:
    #                         for combination in empty_combinations[symbol]:
    #                             new_production = production[:i] + combination + production[i + 1:]
    #                             if new_production not in new_productions[non_terminal]:
    #                                 new_productions[non_terminal].append(new_production)
    #                                 updated = True
    #         if not updated:
    #             break
    #
    #     # Remove all epsilon productions
    #     for non_terminal in new_productions:
    #         new_productions[non_terminal] = [p for p in new_productions[non_terminal] if p != '']
    #