import core.utils
from core.metaclasses import Singleton


class Recorder(metaclass=Singleton):
    def __init__(self):
        self.reset()

    def reset(self):
        self.sample = dict()

    def add(self,tag,value):
        if not tag in self.sample.keys():
            self.sample[tag] = list()
        self.sample[tag].append(value)

    def addMC(self,tag,channel,value):
        if not tag in self.sample.keys():
            self.sample[tag] = dict()
        if not channel in self.sample[tag].keys():
            self.sample[tag][channel] = list()
        self.sample[tag][channel].append(value)

    def generateRecord(self):
        retval = dict(self.sample)
        for k in retval.keys():
            temp = retval[k]
            if type(temp) == dict:
                summ = 0
                for ch in temp.keys():
                    summ += sum(temp[ch])
                retval[k] = summ/len(temp.keys())
            else:
                retval[k] = sum(temp)
        return retval


class Analyser():
    def __init__(self):
        self.record = dict()

    def add(self,rrec):
        for k in rrec:
            if not k in self.record.keys():
                self.record[k] = list()
            self.record[k].append(rrec[k])

    def mean(self):
        return self.swissknife(core.utils.mean)

    def std(self):
        return self.swissknife(core.utils.std)

    def confidence95(self):
        return self.swissknife(core.utils.confidence95)

    def confidence99(self):
        return self.swissknife(core.utils.confidence99)

    def swissknife(self,func):
        retval = dict()
        for k in self.record.keys():
            retval[k] = func(self.record[k])
        return retval

    def getAll(self):
        return self.mean(), self.std(), self.confidence95(), self.confidence99()
