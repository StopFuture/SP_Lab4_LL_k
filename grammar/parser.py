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
                # For each terminal in FIRST(production)
                first_production = self._calculate_first_production(production)

                for terminal_tuple in first_production:
                    terminal = terminal_tuple[0]
                    if terminal != Terminal('ε'):
                        self._add_to_parsing_table(non_terminal, terminal, production)

                # If ε is in FIRST(production), for each terminal in FOLLOW(non_terminal)
                if (Terminal('ε'),) in first_production:
                    self._handle_epsilon(non_terminal, non_terminal, production)

        return self.parsing_table

    def _calculate_first_production(self, production):
        first_production = set()

        production = [c.text for c in Grammar.get_tnt_string(self.grammar, production)]

        for t_symbol in production:
            symbol = Terminal(t_symbol) if Terminal(t_symbol) in self.grammar.terminals else NonTerminal(t_symbol)
            first_symbol = self.first_sets[symbol] if symbol in self.first_sets else {(symbol,)}

            if (Terminal('ε'),) not in first_symbol:
                first_production.update(first_symbol)
            if (Terminal('ε'),) not in first_symbol:
                break
        else:
            first_production.add((Terminal('ε'),))
        return first_production

    def _add_to_parsing_table(self, non_terminal, terminal, production):
        production = [c.text for c in Grammar.get_tnt_string(self.grammar, production)]
        if (non_terminal, terminal) not in self.parsing_table:
            self.parsing_table[(non_terminal, terminal)] = production
        else:
            raise ValueError(f"Grammar is not LL(1): Conflict at ({non_terminal}, {terminal})")

    def _handle_epsilon(self, non_terminal, nt, production):
        production = [c.text for c in Grammar.get_tnt_string(self.grammar, production)]

        # print('ok')
        for terminal in self.follow_sets[NonTerminal(non_terminal)]:
            if (non_terminal, terminal[0]) not in self.parsing_table:
                self.parsing_table[(non_terminal, terminal[0])] = production
            else:
                raise ValueError(f"Grammar is not LL(1): Conflict at ({non_terminal}, {terminal})")


class LL1Parser:
    def __init__(self, parsing_table, start_symbol, grammar):
        self.parsing_table = parsing_table
        self.grammar = grammar
        self.start_symbol = self.grammar.non_terminals[0]

    def str_to_symb(self, symb):
        if Terminal(symb) in self.grammar.terminals:
            return Terminal(symb)
        else:
            return NonTerminal(symb)

    def parse(self, tokens):
        tokens.append('$')  # Append end-of-input
        applied_rules = []
        stack = ['$', self.start_symbol]

        current_token_index = 0
        while len(stack) > 0:
            top = stack.pop()
            print(list(reversed(stack)))
            print(top)
            # print(current_token_index)
            print(tokens[current_token_index:])
            print('-' * 100)

            if isinstance(top, Terminal):
                if top == tokens[current_token_index]:
                    current_token_index += 1
                else:
                    raise SyntaxError(f"Unexpected token: Expected {top}, found {tokens[current_token_index]}")
            elif isinstance(top, NonTerminal):
                if isinstance(tokens[current_token_index], str) and tokens[current_token_index] == '$':
                    entry = self.parsing_table.get((str(top), Terminal('ε')))

                    if entry is not None:
                        applied_rules.append((str(top), Terminal('ε'), entry))
                        for symbol in reversed(entry):
                            if symbol == 'ε':
                                continue
                            stack.append(self.str_to_symb(symbol))
                        continue

                entry = self.parsing_table.get((str(top), tokens[current_token_index]))
                if entry is not None:
                    applied_rules.append((str(top), tokens[current_token_index], entry))
                    for symbol in reversed(entry):
                        if symbol == 'ε':
                            continue
                        stack.append(self.str_to_symb(symbol))
                else:
                    raise SyntaxError(f"No rule to parse: {top} with token {tokens[current_token_index]}")
            elif top == '$':  # End-of-input marker
                if tokens[current_token_index] == '$':  # If current token is also end-of-input
                    print("Parsing successful!")
                    # return  # Parsing is done

                else:
                    raise SyntaxError("Unexpected end of input")

            else:
                raise ValueError(f"Invalid symbol on stack: {top}")

        if current_token_index < len(tokens) - 1:
            raise SyntaxError("Input not fully parsed")

        ternimalized = []
        # print(applied_rules)
        for rule in applied_rules:
            func = lambda x: list(map(self.str_to_symb, x))
            ternimalized.append((func(rule[0]), rule[1], func(rule[2])))
        return ternimalized


def parse_grammar(grammar, string_to_parse):
    str_to_parse = string_to_parse
    # print(Grammar.get_regex(str_to_parse))
    first_follow = FirstFollow(grammar)
    first_k = first_follow.first_k(1)
    follow_k = first_follow.follow_k(1, first_k)
    parser = ParsingTableBuilder(grammar, first_k, follow_k)
    table = parser.build()
    print("Parser control table:")
    print(table)
    print("Analyzer process:")
    applied_rules = None
    try:
        analyzer = LL1Parser(table, " ", grammar)
        tokenized = grammar.get_tnt_string(str_to_parse)
        applied_rules = analyzer.parse(tokenized)
    except SyntaxError as se:
        print(f"Got an error: {str(se)}")
    except ValueError as ve:
        print(f"Got an error: {str(ve)}")
    except:
        print("Got an error")
    return applied_rules