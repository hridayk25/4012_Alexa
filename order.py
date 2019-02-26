class order:
    def __init__(self):
        self.dict = {
            "chicken sandwhich":0,
            "lemonade" : 0,
            "milkshake": 0
        }

    def addItem(self, item):
        self.dict[item] = self.dict[item] + 1

    def printOrder(self):
        string = ""

        for item in self.dict:
            if self.dict[item] != 0:
                string = string + " " + str(self.dict[item]) + " " + item + " and"
        return string
