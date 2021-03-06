from core.components import Component
from core.blackboard import Blackboard
from simpy import Interrupt
from core.log import Loggable


class Behaviour(Loggable):
    def __init__(self, nname):
        super().__init__(nname)
        self.onrun = True
        self.infinite = Blackboard().get('stoptime')
        self.process = self.env.process(self.run())

    def do(self):
        pass

    def boot(self):
        pass

    def run(self):
        self.boot()
        while True:
            try:
                if (self.onrun == True):
                    yield self.env.process(self.do())
                else:
                    yield self.env.timeout(self.infinite)
            except Interrupt as i:
                self.onrun = not self.onrun

class SimpleBehaviour(Behaviour):
    def __init__(self, nname, dettime):
        super().__init__(nname)
        self.deltatime = dettime

    def do(self):
        yield self.env.timeout(self.deltatime)
        if (self.onrun == True):
            self.log('is cii_replpackage;;',2)


class Performing(Component):
    def __init__(self, nname, bbehaviour, mmtbf=0, mmttr=0):
        super().__init__(nname, mmtbf, mmttr)
        self.behaviour = bbehaviour

    def faultPropagation(self):
        super().faultPropagation()
        self.behaviour.process.interrupt()

    def repairPropagation(self):
        super().repairPropagation()
        self.behaviour.process.interrupt()