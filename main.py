from grammar.grammar import Grammar
from grammar.firstfollow import FirstFollow
from grammar.non_terminal import NonTerminal
from grammar.terminal import Terminal
from grammar.parser import ParsingTableBuilder

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
    print(parser.build())
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
      

