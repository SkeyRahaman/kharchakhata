class test():
    a = 0
    b = ""

    def __init__(self, b="default"):
        self.b = b

    def printa(self):
        print(self.b)

    def printb(self):
        print("hi")


sa = test("sa")
ba = test("ba")
test.printa(sa)
test.printa(ba)
