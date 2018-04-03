class Symtable:

    def __init__(self):
        self.table={}
        self.temps=0
        self.labels=0

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

    def newlabel(self):
        self.labels = self.labels + 1
        name = "label"+str(self.labels)
        return name

    def elselabel(self):
        name = "elselabel"
        return name

    def afterlabel(self):
        name = "afterlabel"
        return name