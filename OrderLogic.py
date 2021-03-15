import pickle

N = 0


class Order:
    def __init__(self, num, name=None, flag=False, cost=0, args=None):
        self.name = name
        self.num = num + 1
        self.flag = flag
        self.cost = cost
        self.orders = args
        self.count = 0

    def __repr__(self):
        return f'{self.num}, {self.name}, {self.cost}, {self.flag},{self.orders}'

    def separator(self):
        K = dict(name=self.name, cost=self.cost, order=self.orders, flag=self.flag, num=self.num)
        return K

    def changeflag(self):
        dbfile = open('order', 'rb')
        bd = pickle.load(dbfile)
        dbfile.close()
        bd[self - 1].flag = not bd[self - 1].flag
        updatedb(bd)

    def separateOrders(self):
        lBorder = rBorder = 0
        L = []
        dictoforders = {}
        self.orders = self.orders.replace(' ', '')

        for x in self.orders:
            rBorder += 1
            if x == ',':
                K = self.orders[lBorder:rBorder - 1]
                lBorder = rBorder
                try:
                    int(K)
                    dictoforders[f'{K}'] = 1
                except (ValueError):

                    a1 = a2 = 0
                    for i in K:
                        a2 += 1
                        if i == '*':
                            dictoforders[f'{K[a1:a2 - 1]}'] = int(K[a2:len(K)])
        return dictoforders


def adder(num, name=None, cost=0, args=None, flag=False):
    dbfile = open('order', 'rb')
    bd = pickle.load(dbfile)
    dbfile.close()
    num -= 1
    bd.append(Order(num, name, cost=cost, args=args, flag=flag))
    updatedb(bd)


def cleardb():
    dbfile = open('order', 'wb')
    pickle.dump([], dbfile)
    dbfile.close()


def updatedb(bd):
    dbfile = open('order', 'wb')
    pickle.dump(bd, dbfile)
    dbfile.close()


def loaddb(nameof, x):
    dbfile = open(f'{nameof}', 'rb')
    bd = pickle.load(dbfile)
    dbfile.close()
    x -= 1
    return bd[x]


def checkcount(nameof):
    dbfile = open(f'{nameof}', 'rb')
    bd = pickle.load(dbfile)
    dbfile.close()
    n = 0
    for x in bd:
        n += 1
    return n


if __name__ == '__main__':
    data = loaddb('order', 2)
    D = Order.separateOrders(data)
    print(D.keys())
