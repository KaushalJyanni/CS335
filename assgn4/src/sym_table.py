class Symtable:

    def __init__(self):
        self.table={}
        self.parent=None

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
