

class VHResult():

    def __init__(self, deltaH, deltaS, xs, ys, m, b):
        self.deltaH = deltaH
        self.deltaS = deltaS
        self.xs = xs
        self.ys = ys
        self.m = m
        self.b = b

    def to_dict(self):
        return {
            "deltaH": self.deltaH,
            "deltaS": self.deltaS,
            "m": self.m,
            "b": self.b,
            "xs": self.xs,
            "ys": self.ys,
        }