from grammar.grammar import Grammar

if __name__ == "__main__":
    test_grammar = Grammar({
        'S': ['BA'], 
        'A': ['+BA', 'ε'],
        'B': ['DC'],
        'C': ['*DC', 'ε'],
        'D': ['(S)', 'a']
    })

    # print(test_grammar.non_terminals)