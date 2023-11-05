from grammar.non_terminal import NonTerminal
from grammar.terminal import Terminal
import re
import itertools

class Grammar:
    def __init__(self, rules):
        self.terminals = []
        self.non_terminals = []
        self.get_rules(rules)

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