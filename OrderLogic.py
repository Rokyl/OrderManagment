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
        return f'{self.num}, {self.name}, {self.cost}, {self.flag}'

    def separator(self):
        K = dict(name=self.name, cost=self.cost, order=self.orders, flag=self.flag, num=self.num)
        return K

    def changeflag(self):
        dbfile = open('order', 'rb')
        bd = pickle.load(dbfile)
        dbfile.close()
        bd[self - 1].flag = not bd[self - 1].flag
        updatedb(bd)


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
    pass
