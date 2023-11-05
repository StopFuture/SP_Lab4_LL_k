from grammar.non_terminal import NonTerminal
from grammar.terminal import Terminal
import re
import itertools


class Grammar:
    def __init__(self, rules):
        self.terminals = []
        self.non_terminals = []
        self.get_rules(rules)
        self.rules = rules
        self.epsilon_producers = self.find_epsilon_producing_non_terminals()

    def get_epsilon(self):
        return next((t for t in self.terminals if t.is_empty()))

    def get_epsilon(self):
        return next((t for t in self.terminals if t.is_empty()))

    @staticmethod
    def get_regex(text_set):
        return f"({'|'.join(sorted([re.escape(t.text) for t in text_set], key=lambda x: len(x), reverse=True))})"

    def get_rules(self, rules):
        self.non_terminals += [NonTerminal(n) for n in list(rules.keys())]
        N_regex = Grammar.get_regex(self.non_terminals)

        # get terminals
        terminals = set()
        for n in self.non_terminals:
            for nt_rule in rules[n.text]:
                g = nt_rule.split()
                t = [re.sub(N_regex, ' ', p).split() for p in g]
                terminals |= set(itertools.chain.from_iterable(t))
        self.terminals = [Terminal(term) for term in terminals]

        print(self.terminals, self.non_terminals)

        T_regex = Grammar.get_regex(self.terminals)

        regex = f"{N_regex}|{T_regex}"

        # get rules
        for n in self.non_terminals:
            for nt_rule in rules[n.text]:
                n.rules.append([])
                for m in re.finditer(regex, nt_rule):
                    if m.group(1):
                        n.rules[-1].append(next((nt for nt in self.non_terminals if nt.text == m.group(1))))
                    elif m.group(2):
                        n.rules[-1].append(next((t for t in self.terminals if t.text == m.group(2))))

    def find_epsilon_producing_non_terminals(self):
        epsilon_producers = set()
        # Finding non-terminals that have a direct epsilon production
        for nt in self.non_terminals:
            for production in nt.rules:
                if any(isinstance(symbol, Terminal) and symbol.is_empty() for symbol in production):
                    epsilon_producers.add(nt)
                    break

        # Recursive: finding non-terminals that can produce epsilon through other non-terminals
        added = True
        while added:
            added = False
            for nt in self.non_terminals:
                if nt in epsilon_producers:
                    continue
                for production in nt.rules:
                    # If all elements in the production are epsilon producers or empty terminals, this one is too
                    if all(symbol in epsilon_producers or (isinstance(symbol, Terminal) and symbol.is_empty()) for
                           symbol in production):
                        epsilon_producers.add(nt)
                        added = True
                        break

        return epsilon_producers

    @staticmethod
    def read_grammar_from_file(file_path):
        rules = {}

        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split('->')
                if len(parts) == 2:
                    left, right = parts
                    left = left.strip()

                    right_productions = right.strip().split("|")
                    if left not in rules:
                        rules[left] = right_productions
                    else:
                        rules[left].extend(right_productions)

        # Replace any occurrence of 'epsilon' with 'ε'
        for key in rules.keys():
            rules[key] = ['ε' if prod == 'epsilon' else prod for prod in rules[key]]

        return rules
