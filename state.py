class State:
    def __init__(self, id, pid, cbrd, gn, hn):
        self.id = id
        self.pid = pid
        self.cbrd = cbrd
        self.gn = gn
        self.hn = hn
        self.fn = gn + hn

    def __lt__(self, other):
        return self.id < other.id
