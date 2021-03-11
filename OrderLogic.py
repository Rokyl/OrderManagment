import pickle

N = 0


class Order:
    def __init__(self, num, name=None, flag=False, cost=0):
        self.name = name
        self.num = num
        self.flag = flag
        self.cost = cost
        # self.orders = args

    def __repr__(self):
        return f'{self.num}, {self.name}, {self.cost}'


def adder(num, name=None, flag=False, cost=0):
    dbfile = open('order', 'rb')
    bd = pickle.load(dbfile)
    dbfile.close()

    bd.append(Order(num, name, cost=cost))
    updatedb(bd)


def cleardb():
    dbfile = open('order', 'wb')
    pickle.dump([], dbfile)
    dbfile.close()


def updatedb(bd):
    dbfile = open('order', 'wb')
    pickle.dump(bd, dbfile)
    dbfile.close()

    # cleardb()


def loaddb(nameof,x):
    dbfile = open(f'{nameof}', 'rb')
    bd = pickle.load(dbfile)
    dbfile.close()
    return bd[x]


if __name__ == '__main__':
    adder(1, 'Bob', cost=1000)
    adder(2, 'Sue', cost=1000)

