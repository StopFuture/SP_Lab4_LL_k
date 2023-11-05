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