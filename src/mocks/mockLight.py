class mockLight:

    def __init__(self):
        self.color = None
        self.curR = None
        self.curG = None
        self.curB = None

    def testInput(self, r, g, b, colorName):
        if isinstance(r, int) & isinstance(g, int) & isinstance(b, int) & isinstance(colorName, str):
            if 0 <= r <= 255 & 0 <= g <= 255 & 0 <= b <= 255:
                self.color = colorName
                self.curR = r
                self.curG = g
                self.curB = b
                return "The light was changed to the color, " + colorName
            else:
                return("Invalid numbers")
        else:
            return("Invalid RGB types")

    # Returns class variables in order of colorName, R value, G value, and B value of color
    def getInfo(self):
        current_info = [self.color, self.curR, self.curG, self.curB]
        return current_info
