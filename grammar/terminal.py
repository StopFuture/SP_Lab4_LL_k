class Terminal():
    def __init__(self, text):
        self.text = text

    def is_empty(self):
        return self.text in ('ε', 'epsilon')
    
    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return self.text