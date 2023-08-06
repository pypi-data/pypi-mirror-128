class Color:
    def __init__(self, r, g, b, a = 255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def get_tuple(self):
        return (self.r, self.g, self.b, self.a)