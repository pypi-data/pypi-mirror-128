class Symbol:
    def __init__(self, symbols, kind = 'phoneme', delimiter='/', **kwargs):
        self.symbols = ['_PAD_'] + symbols
        self.symbol_to_id = {v:k for k, v in enumerate(self.symbols)}
        assert(kind in ['phoneme', 'char'])
        self.kind = kind
        self.delimiter=delimiter

    def __len__(self):
        return len(self.symbols)
    
    def __call__(self, text):
        if self.kind == 'phoneme':
            return self.phoneme_to_index(text)
        elif self.kind == 'char':
            return self.text_to_index(text)

    def phoneme_to_index(self, text):
        text = text.split(self.delimiter)
        text = [self.symbol_to_id[i] for i in text if len(i) > 0]
        return text

    def text_to_index(self, text):
        text = [self.symbol_to_id[i] for i in text]
        return text
