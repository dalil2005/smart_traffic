"""Rule-based controllers. Swap SmartController for an ML/RL/vision
controller later by implementing the same small interface:
    green_time(axis), should_end_green(), choose_next_axis()."""
from config import *
from simulation.traffic_light import GREEN, YELLOW, ALL_RED
from ai.traffic_score import dynamic_green_time
from ai.priority_system import PrioritySystem


class TrafficController:
    name = "BASE"

    def __init__(self, intersection, traffic):
        self.intersection, self.traffic = intersection, traffic
        self.axis, self.phase, self.elapsed = "NS", GREEN, 0.0
        self.target = self.green_time(self.axis)
        self.apply()

    # --- decisions (override) ---
    def green_time(self, axis):
        return FIXED_GREEN

    def should_end_green(self):
        return self.elapsed >= self.target

    def choose_next_axis(self):
        return OPPOSITE_AXIS[self.axis]

    # --- state machine ---
    def adopt(self, other):
        self.axis, self.phase, self.elapsed = other.axis, other.phase, other.elapsed
        self.target = self.green_time(self.axis)
        self.apply()

    def apply(self):
        self.intersection.apply(self.axis, self.phase)

    def remaining(self, axis):
        if axis != self.axis:
            return None
        if self.phase == GREEN:
            return max(self.target - self.elapsed, 0.0)
        if self.phase == YELLOW:
            return max(YELLOW_TIME - self.elapsed, 0.0)
        return None

    def _to(self, phase):
        self.phase, self.elapsed = phase, 0.0

    def update(self, dt):
        self.elapsed += dt
        ea = self.traffic.emergency_axis()
        if self.phase == GREEN:
            if ea == self.axis:
                pass                                   # hold green for the ambulance
            elif ea and self.elapsed >= EMERGENCY_MIN_GREEN:
                self._to(YELLOW)                       # preempt: stop conflicting traffic
            elif self.should_end_green():
                self._to(YELLOW)
        elif self.phase == YELLOW:
            if self.elapsed >= YELLOW_TIME:
                self._to(ALL_RED)
        elif self.elapsed >= ALL_RED_TIME:
            self.axis = ea or self.choose_next_axis()
            self.target = self.green_time(self.axis)
            self._to(GREEN)
        self.apply()


class FixedController(TrafficController):
    name = "FIXED"


class SmartController(TrafficController):
    name = "SMART"

    def __init__(self, intersection, traffic):
        self.prio = PrioritySystem()
        super().__init__(intersection, traffic)

    def _m(self, axis):
        return self.prio.axis_metrics(self.traffic.metrics, axis)

    def green_time(self, axis):
        m = self._m(axis)
        return dynamic_green_time(m["cars"], m["avg_wait"])

    def should_end_green(self):
        e = self.elapsed
        own, other = self._m(self.axis), self._m(OPPOSITE_AXIS[self.axis])
        if other["cars"] == 0:
            return False                               # nobody waiting: rest on green
        if e >= MAX_GREEN:
            return True
        if own["cars"] == 0:
            return e >= MIN_SAFE_GREEN                 # empty road: leave early (not jittery)
        if e < MIN_GREEN:
            return False
        if self.prio.is_starving(other) or e >= self.target:
            return True
        return self.prio.priority(other) > SWITCH_RATIO * self.prio.priority(own)

    def choose_next_axis(self):
        other = OPPOSITE_AXIS[self.axis]
        if self._m(other)["cars"] == 0 and self._m(self.axis)["cars"] > 0:
            return self.axis
        return other


CONTROLLERS = {"FIXED": FixedController, "SMART": SmartController}
