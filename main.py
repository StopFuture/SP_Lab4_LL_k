from grammar.grammar import Grammar
from grammar.firstfollow import FirstFollow
from grammar.non_terminal import NonTerminal
from grammar.terminal import Terminal
from grammar.parser import ParsingTableBuilder


def build_parsing_table(grammar, first_sets, follow_sets):
    """Build the LL(1) parsing table for a given grammar."""
    parsing_table = {}
    
    for i, (non_terminal, productions) in enumerate(grammar.rules.items()):
        for production in productions:
            # For each terminal in FIRST(production)
            first_production = set()
            #print(non_terminal)
            #print(production)
            for t_symbol in production:
                symbol = Terminal(t_symbol) if Terminal(t_symbol) in grammar.terminals else NonTerminal(t_symbol)
                first_symbol = first_sets[symbol] if symbol in first_sets else {(symbol, )}
                #print(first_symbol)
                if Terminal('ε') not in first_symbol:
                    #print(first_symbol)
                    first_production.update(first_symbol)
                if 'ε' not in first_symbol:
                    break
            else:
                first_production.add(Terminal('ε'))
            #print()
            #print(first_production)
            for terminall in first_production:
                #print(terminal)
                terminal = terminall[0]
                #print(terminal[0])
                #print(Terminal('ε'))
                if terminal != Terminal('ε'):
                    if (non_terminal, terminal) not in parsing_table:
                        parsing_table[(non_terminal, terminal)] = production
                    else:
                        raise ValueError(f"Grammar is not LL(1): Conflict at ({non_terminal}, {terminal})")

            # If ε is in FIRST(production), for each terminal in FOLLOW(non_terminal)
            if (Terminal('ε'), ) in first_production:
                #print('okdfdkflkdlfk')
                for terminal in follow_sets[NonTerminal(non_terminal)]:
                    if (non_terminal, terminal) not in parsing_table:
                        parsing_table[(non_terminal, terminal)] = (production, i)
                    else:
                        raise ValueError(f"Grammar is not LL(1): Conflict at ({non_terminal}, {terminal})")

    return parsing_table

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
      

