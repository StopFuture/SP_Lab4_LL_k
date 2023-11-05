class NonTerminal():
    def __init__(self, text):
        self.text = text
        self.rules = []

    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return self.text