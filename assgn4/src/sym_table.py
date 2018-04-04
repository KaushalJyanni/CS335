class Symtable:

    def __init__(self):
        self.table={}
        self.temps=0
        self.labels=0
        self.elabels=0
        self.alabels=0

    def lookup(self, var):
        if var in self.table.keys():
            return self.table[var]
        else:
            return None

    def gettype(self,var):
        if(self.lookup(var)):
            return self.table[var]["type"]
        else:
            return None

    def insert(self, var, typeof):
        print "************************8888",typeof
        self.table[var] = {}
        self.table[var]["type"] = str(typeof)
        # print "yolooooooooooooooo", self.table['a']["type"]

    def newtemp(self, typeof):
        self.temps = self.temps + 1
        name = "temp"+str(self.temps)
        self.insert(name, typeof)
        return name

    def newlabel(self):
        self.labels = self.labels + 1
        name = "label"+str(self.labels)
        return name

    def elselabel(self):
        self.elabels = self.elabels + 1
        name = "elselabel"+str(self.elabels)
        return name

    def afterlabel(self):
        self.alabels = self.alabels + 1
        name = "afterlabel"+str(self.alabels)
        return name

    def getelabel(self):
        name = "elselabel"+str(self.elabels)
        return name

    def getalabel(self):
        name = "afterlabel"+str(self.alabels)
        return name
