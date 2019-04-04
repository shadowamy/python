class name:
    __myname = 'abc'

    def setname(self, newname):
        self.__myname = newname

    def getname(self):
        print(self.__myname)

n = name()
n.setname("xiaohong")
n.getname()