import time


class ThrottledGenerator(object):
    def __init__(self, delta=None, num=None, gen=None, **genargs):
        self.delta = delta or 0
        self.last = 0
        self.genargs = genargs
        self.gen = gen
        self.num = num
        self.count = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.num and self.count >= self.num:
            raise StopIteration

        t = time.time()
        if t - self.last > self.delta:
            self.last = t
            self.count += 1
            return self.gen(self.genargs) 
        else:
            return None


