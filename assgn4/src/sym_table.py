class Symtable:

    def __init__(self):
        self.table={}
        self.temps=0

    def lookup(self, var):
        if var in self.table.keys():
            return self.table[var]
        else:
            return None

    def insert(self, var):
        self.table[var] = {}
        self.table[var]["type"] = ""

    def newtemp(self):
        self.temps = self.temps + 1
        name = "temp"+str(self.temps)
        self.insert(name)
        return name