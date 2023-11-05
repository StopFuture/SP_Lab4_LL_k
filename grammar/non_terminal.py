class NonTerminal():
    def __init__(self, text):
        self.text = text
        self.rules = []

    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return self.text
    
    def __eq__(self, o: object) -> bool:
        #if isinstance(o, NonTerminal):
        return self.text == o.text
        #return False
    
    def __hash__(self) -> int:
        return hash(self.text)