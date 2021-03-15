import pickle

N = 0


class Order:
    def __init__(self, num, name=None, flag=False, cost=0, args=None):
        self.name = name
        self.num = num + 1
        self.flag = flag
        self.cost = cost
        self.orders = args

    def __repr__(self):
        return f'{self.num}, {self.name}, {self.cost}, {self.flag},{self.orders}'

    def separator(self):
        K = dict(name=self.name, cost=self.cost, order=self.orders, flag=self.flag, num=self.num)
        return K

    def changeflag(self,path):
        dbfile = open(path, 'rb')
        bd = pickle.load(dbfile)
        dbfile.close()
        bd[self.num - 1].flag = not bd[self.num - 1].flag
        updatedb(path,bd)

    def separateOrders(self):
        lBorder = rBorder = 0
        dictoforders = {}
        self.orders = self.orders.replace(' ', '')
        commacount = 0
        for x in self.orders:
            if x == ',':
                commacount += 1
        for x in self.orders:
            rBorder += 1
            if x == ',' or commacount == 0:
                K = self.orders[lBorder:rBorder - 1]
                lBorder = rBorder
                commacount -= 1
                if commacount == 0:
                    rBorder = len(self.orders)
                try:
                    int(K)
                    dictoforders[f'{K}'] = 1
                except ValueError:
                    a1 = a2 = 0
                    for i in K:
                        a2 += 1
                        if i == '*':
                            dictoforders[f'{K[a1:a2 - 1]}'] = int(K[a2:len(K)])
        return dictoforders


def adder(path, num, name=None, cost=0, args=None, flag=False):
    dbfile = open(path, 'rb')
    bd = pickle.load(dbfile)
    dbfile.close()
    num -= 1
    bd.append(Order(num, name, cost=cost, args=args, flag=flag))
    updatedb(path, bd)
    savefile(path,)

def cleardb():
    dbfile = open('order', 'wb')
    pickle.dump([], dbfile)
    dbfile.close()
def loadfile(path):
    dbfile = open(path, 'rb')
    bd = pickle.load(dbfile)
    dbfile.close()
    dbfile = open('order', 'wb')
    pickle.dump(bd, dbfile)
    dbfile.close()

def savefile(path):
    dbfile = open('order', 'rb')
    bd = pickle.load(dbfile)
    dbfile.close()
    dbfile = open(path, 'wb')
    pickle.dump(bd, dbfile)
    dbfile.close()


def updatedb(path, bd):
    dbfile = open(path, 'wb')
    pickle.dump(bd, dbfile)
    dbfile.close()


def loaddb(path, x):
    dbfile = open(path, 'rb')
    bd = pickle.load(dbfile)
    dbfile.close()
    x -= 1
    return bd[x]


def checkcount(path):
    dbfile = open(path, 'rb')
    bd = pickle.load(dbfile)
    dbfile.close()
    n = 0
    for x in bd:
        n += 1
    return n


if __name__ == '__main__':
    path='order'
   # adder(path,1, args='1,2,4,5,6')
    cleardb()
    data = loaddb(path, 4)
    D = Order.separateOrders(data)
    print(D.keys())
