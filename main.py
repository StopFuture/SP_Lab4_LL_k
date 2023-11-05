from grammar.grammar import Grammar
from grammar.firstfollow import FirstFollow
from grammar.non_terminal import NonTerminal
from grammar.terminal import Terminal
from grammar.parser import ParsingTableBuilder

class LL1Parser:
    def __init__(self, parsing_table, start_symbol, grammar):
        self.parsing_table = parsing_table
        #for key, v in self.parsing_table:
        #    parsing_table[(key[0], str(key[1])]
        self.start_symbol = start_symbol
        self.grammar = grammar
        
    def str_to_symb(self, symb):
        if Terminal(symb) in self.grammar.terminals:
            return Terminal(symb)
        else:
            return NonTerminal(symb)
            
    def parse(self, tokens):
        #tokens  = list(reversed(tokens))
        tokens.append('$')  # Append end-of-input marker
        stack = ['$', self.start_symbol]  # Initialize stack with start symbol and end-of-input marker

        current_token_index = 0
        while len(stack) > 0:
            top = stack.pop() 
            print(list(reversed(stack)))
            print(top)
            #print(current_token_index)
            print(tokens[current_token_index:])
             # Get the top of the stack
            print('-'*100)
            
            #elif self.parsing_table.get((str(top), tokens[current_token_index]))
            if isinstance(top, Terminal):  # If the top is a Terminal
                if top == tokens[current_token_index]:  # Match terminal with current token
                    current_token_index += 1  # Consume the token
                else:
                    raise SyntaxError(f"Unexpected token: Expected {top}, found {tokens[current_token_index]}")
            elif isinstance(top, NonTerminal):  # If the top is a NonTerminal
                # Look up the parsing table entry
                if isinstance(tokens[current_token_index], str) and tokens[current_token_index] == '$':
                    #print('dfjjdfok')
                    entry = self.parsing_table.get((str(top), Terminal('ε')))
                    if entry is not None:
                        for symbol in reversed(entry):
                            if symbol == 'ε':
                                continue
                            stack.append(self.str_to_symb(symbol))
                        continue
                        
                    
                entry = self.parsing_table.get((str(top), tokens[current_token_index]))
                if entry is not None:
                    # Push the production onto the stack in reverse order
                    for symbol in reversed(entry):
                        if symbol == 'ε':
                            continue
                        stack.append(self.str_to_symb(symbol))
                else:
                    raise SyntaxError(f"No rule to parse: {top} with token {tokens[current_token_index]}")
            elif top == '$':  # End-of-input marker
                if tokens[current_token_index] == '$':  # If current token is also end-of-input
                    print("Parsing successful!")
                    return  # Parsing is done

                else:
                    raise SyntaxError("Unexpected end of input")

            else:  # If it's not a terminal, non-terminal or end-of-input marker
                raise ValueError(f"Invalid symbol on stack: {top}")

        if current_token_index < len(tokens) - 1:  # If there are still tokens left to parse
            raise SyntaxError("Input not fully parsed")

# Example usage:
# parser = LL1Parser(parsing_table, start_symbol)
# parser.parse(list_of_tokens)


if __name__ == "__main__":
    test_grammar = Grammar({
        'S': ['BA'],
        'A': ['+BA', 'ε'],
        'B': ['DC'],
        'C': ['*DC', 'ε'],
        'D': ['(S)', 'a']
    })

    test_grammar_1 = Grammar({
        'E': ['id + D', '(E * R)', 'epsilon'],
        'D': ['V * E', 'L ! E'],
        'R': ['V ! E', 'L * E'],
        'V': ['Z', 'num'],
        'L': ['Z', '(E)'],
        'Z': ['epsilon'],
    })


    test_grammar_conflict = Grammar({
        'S': ['E', 'E a'],
        'E': ['b', 'epsilon']
    })

    # print(test_grammar.non_terminals)
    first_follow = FirstFollow(test_grammar)
    first_k = first_follow.first_k(1)
    follow_k = first_follow.follow_k(1, first_k)
    #print(first_follow.tuples_to_strings(follow_k))
    parser = ParsingTableBuilder(test_grammar, first_k, follow_k)
    table = parser.build()
    print(table)
    parser = LL1Parser(table, NonTerminal('S'), test_grammar)
    str_to_parse = '(a+a)*a'
    parser.parse(list(map(lambda x: Terminal(x), str_to_parse)))
    print('-' * 100)
    # print(first_follow.tuples_to_strings(first_follow.first_k(2)))
    #print(first_follow.tuples_to_strings(follow_k))
    # print(f)

    # print(first_follow.concat_k(1, {(Terminal('ε'),)}, {(Terminal('ε'),), (Terminal('+'),)}))


    test_grammar_2 = Grammar({
        'E': ['id + D', '( E * R )', 'ε'],
        'D': ['V * E', 'L ! E'],
        'R': ['V ! E'],
        'V': ['Z', 'num'],
        'L': ['Z', '( E )'],
        'Z': ['ε']
    })

    #test_grammar_3 = Grammar(Grammar.read_grammar_from_file("inputs/input_1.txt"))
    # print(test_grammar.non_terminals)

    print(test_grammar.epsilon_producers)
    print(test_grammar_2.epsilon_producers)
    #print(test_grammar_3.epsilon_producers)
      

