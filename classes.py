class House():
    def __init__(self, name, symbol_url, color, gif_url):
        self.name = name
        self.symbol_url = symbol_url
        self.color = color
        self.gif_url = gif_url

    def __str__(self):
        return self.name
