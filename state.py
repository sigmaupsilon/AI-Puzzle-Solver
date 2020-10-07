class State:
    def __init__(self, id: str, pid: str, cbrd: list, gn: int, hn: int):
        self.id = id
        self.pid = pid
        self.cbrd = cbrd
        self.gn = gn
        self.hn = hn
        self.fn = gn + hn

    def __lt__(self, other):
        return self.id < other.id
