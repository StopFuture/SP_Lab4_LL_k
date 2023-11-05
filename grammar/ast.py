from grammar.non_terminal import NonTerminal

class ASTNode:
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    @staticmethod
    def print_ast(node, prefix="", last=True):
        turn = '└── ' if last else '├── '
        print(prefix + turn + str(node.symbol))

        prefix += '    ' if last else '│   '

        child_count = len(node.children)
        for i, child in enumerate(node.children):
            is_last = i == (child_count - 1)
            ASTNode.print_ast(child, prefix, last=is_last)