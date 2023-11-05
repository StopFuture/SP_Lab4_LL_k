class Terminal():
    def __init__(self, text):
        self.text = text
        if self.is_empty():
            self.text = 'ε'

    def is_empty(self):
        return self.text in ('ε', 'epsilon', 'eps')
    
    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return self.text

    def __eq__(self, o: object) -> bool:
        #if isinstance(o, Terminal):
        return self.text == o.text
        #return False
    
    def __hash__(self) -> int:
        return hash(self.text)