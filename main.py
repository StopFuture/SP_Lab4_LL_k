from grammar.grammar import Grammar
from grammar.firstfollow import FirstFollow
from grammar.ast import ASTNode
from grammar.parser import ParsingTableBuilder, LL1Parser, parse_grammar
from grammar.recursive_descent import RecursiveDescentParser


def parse_and_display(grammar, str_to_parse):
    first_follow = FirstFollow(grammar)
    first_k = first_follow.first_k(1)
    follow_k = first_follow.follow_k(1, first_k)
    print("Terminals: ", grammar.terminals)
    print("Non-Terminals: ", grammar.non_terminals)
    print("Epsilon-Producers: ", grammar.epsilon_producers)
    print("First_k", first_k)
    print("Follow_k", follow_k)

    recursive_parser = RecursiveDescentParser(grammar)
    print(f'Recursive Descent Parsing "{str_to_parse}": {recursive_parser.parse(str_to_parse)}')
    sequence = parse_grammar(grammar, str_to_parse)
    print('-' * 100)
    if sequence:
        print("Applied Rules:")
        for i, rule in enumerate(sequence):
            print(f"{rule[0]} -> {rule[2]}")

        print('-' * 100)
        print("Abstract Syntax Tree:")
        root = grammar.build_ast(sequence)
        ASTNode.print_ast(root)
        print('-' * 100)
    else:
        print("AST cannot be built")


if __name__ == "__main__":
    print("TEST 1:")
    test_grammar = Grammar({
        'S': ['BA'],
        'A': ['+BA', 'ε'],
        'B': ['DC'],
        'C': ['*DC', 'ε'],
        'D': ['(S)', 'a']
    })
    str_to_parse = '(a+a)*a'

    parse_and_display(test_grammar, str_to_parse)

    print("TEST 2: \n")
    test_grammar_1 = Grammar(Grammar.read_grammar_from_file("inputs/input_1.txt"))

    str_to_parse_1 = 'id + ! id + !'
    str_to_parse_2 = '( * ! !)'

    parse_and_display(test_grammar_1, str_to_parse_1)





