from grammar.grammar import Grammar
from grammar.firstfollow import FirstFollow
from grammar.non_terminal import NonTerminal
from grammar.terminal import Terminal

class ParsingTableBuilder:
    def __init__(self, grammar, first_sets, follow_sets):
        self.grammar = grammar
        self.first_sets = first_sets
        self.follow_sets = follow_sets
        self.parsing_table = {}

    def build(self):
        for non_terminal, productions in self.grammar.rules.items():
            for production in productions:
                print(non_terminal)
                # For each terminal in FIRST(production)
                first_production = self._calculate_first_production(production)
                print(first_production)
                
                for terminal_tuple in first_production:
                    
                    terminal = terminal_tuple[0]
                    if terminal != Terminal('ε'):
                        self._add_to_parsing_table(non_terminal, terminal, production)
                
                # If ε is in FIRST(production), for each terminal in FOLLOW(non_terminal)
                if (Terminal('ε'), ) in first_production:
                    self._handle_epsilon(non_terminal, production)

        return self.parsing_table

    def _calculate_first_production(self, production):
        first_production = set()
        for t_symbol in production:
            symbol = Terminal(t_symbol) if Terminal(t_symbol) in self.grammar.terminals else NonTerminal(t_symbol)
            first_symbol = self.first_sets[symbol] if symbol in self.first_sets else {(symbol, )}
            if Terminal('ε') not in first_symbol:
                first_production.update(first_symbol)
            if 'ε' not in first_symbol:
                break
        else:
            first_production.add(Terminal('ε'))
        return first_production

    def _add_to_parsing_table(self, non_terminal, terminal, production):
        if (non_terminal, terminal) not in self.parsing_table:
            self.parsing_table[(non_terminal, terminal)] = production
        else:
            raise ValueError(f"Grammar is not LL(1): Conflict at ({non_terminal}, {terminal})")

    def _handle_epsilon(self, non_terminal, production):
        print('ok')
        for terminal in self.follow_sets[NonTerminal(non_terminal)]:
            print(terminal)
            if (non_terminal, terminal) not in self.parsing_table:
                print((non_terminal, terminal))
                self.parsing_table[(non_terminal, terminal[0])] = production
            else:
                raise ValueError(f"Grammar is not LL(1): Conflict at ({non_terminal}, {terminal})")
