from config import *
from simulation.intersection import Intersection
from simulation.traffic_manager import TrafficManager
from ai.traffic_controller import CONTROLLERS


class Simulation:
    def __init__(self, controller=DEFAULT_CONTROLLER, density=DEFAULT_DENSITY,
                 seed=None, forced_mode=None):
        self.intersection = Intersection()
        self.traffic = TrafficManager(seed, density)
        self.traffic.forced_mode = forced_mode
        self.controller_name = controller
        self.controller = CONTROLLERS[controller](self.intersection, self.traffic)

    def set_controller(self, name):
        if name == self.controller_name:
            return
        new = CONTROLLERS[name](self.intersection, self.traffic)
        new.adopt(self.controller)               # keep the current phase: no glitch
        self.controller, self.controller_name = new, name

    def step(self, dt):
        self.controller.update(dt)
        self.traffic.update(dt, self.intersection.lights)
        self.traffic.stats.tick(dt, self.controller.axis, self.controller.phase)

    @property
    def stats(self):
        return self.traffic.stats

    def summary(self):
        s = self.stats.summary()
        s["waiting"] = sum(m["queue"] for m in self.traffic.metrics.values())
        return s
