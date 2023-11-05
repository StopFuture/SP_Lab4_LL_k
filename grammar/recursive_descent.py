from grammar.non_terminal import NonTerminal
from grammar.terminal import Terminal


class RecursiveDescentParser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.tokens = []
        self.index = 0

    def parse(self, input_str):
        self.tokens = [c.text for c in self.grammar.get_tnt_string(input_str)]
        self.index = 0
        start_symbol = self.grammar.non_terminals[0]
        return self.parse_non_terminal(start_symbol) and self.index == len(self.tokens)

    def parse_non_terminal(self, non_terminal):
        save_index = self.index
        for rule in non_terminal.rules:
            self.index = save_index  # backtrack to the start of this rule
            if all(self.parse_symbol(symbol) for symbol in rule):
                return True  # successfully parsed this rule
        self.index = save_index  # backtrack to the start of this non-terminal
        return False

    def parse_symbol(self, symbol):
        if isinstance(symbol, Terminal):
            if symbol.is_empty():
                return True  # epsilon transition
            return self.match(symbol.text)
        elif isinstance(symbol, NonTerminal):
            return self.parse_non_terminal(symbol)
        return False

    def match(self, terminal):
        if self.index < len(self.tokens) and self.tokens[self.index] == terminal:
            self.index += 1
            return True
        return False