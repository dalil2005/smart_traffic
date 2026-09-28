import random
from config import *
from simulation.car import Car, EmergencyVehicle
from simulation.statistics import Statistics


def mode_for_hour(h):
    for a, b, m in MODE_SCHEDULE:
        if a <= h < b:
            return m
    return "NORMAL"


class TrafficManager:
    """Spawns, moves and removes cars; exposes per-approach metrics."""

    def __init__(self, seed=None, density=DEFAULT_DENSITY):
        self.rng = random.Random(seed)
        self.density = density
        self.forced_mode = None
        self.emergency_prob = EMERGENCY_PROB
        self.clock = START_HOUR * 3600
        self.time = 0.0
        self.cars = {d: [] for d in DIRECTIONS}      # front car first
        self.backlog = {d: [] for d in DIRECTIONS}   # cars waiting to enter the map
        self.timers = {d: self._interval(d) for d in DIRECTIONS}
        self.stats = Statistics()
        self.metrics = {}
        self._next_metrics = 0.0
        self._refresh_metrics()

    @property
    def mode(self):
        return self.forced_mode or mode_for_hour(self.clock / 3600)

    def _interval(self, d):
        lo, hi = DENSITY[self.density]
        return self.rng.uniform(lo, hi) * MODE_INTERVAL_MULT[self.mode] / DIRECTION_WEIGHT[d]

    # spawning ---------------------------------------------------------
    def _create(self, d):
        cls = EmergencyVehicle if self.rng.random() < self.emergency_prob else Car
        self.backlog[d].append(cls(d, self.rng, self.time))
        self.stats.generated += 1

    def spawn_emergency(self, direction=None):
        d = direction or self.rng.choice(DIRECTIONS)
        self.backlog[d].insert(0, EmergencyVehicle(d, self.rng, self.time))
        self.stats.generated += 1

    def _admit(self, d):
        bl, lane = self.backlog[d], self.cars[d]
        if not bl:
            return
        last = lane[-1] if lane else None
        if last is None or last.rear >= MIN_GAP * 1.5:      # entry is clear
            car = bl.pop(0)
            car.waiting_time += self.time - car.created     # time queued off-map
            if last is not None:
                car.speed = min(car.speed, last.speed)
            lane.append(car)

    # update -----------------------------------------------------------
    def update(self, dt, lights):
        self.time += dt
        self.clock = (self.clock + dt * CLOCK_SPEED) % 86400
        for d in DIRECTIONS:
            self.timers[d] -= dt
            if self.timers[d] <= 0:
                self.timers[d] += self._interval(d)
                self._create(d)
            self._admit(d)
            lane, prev, state = self.cars[d], None, lights[d].state
            for car in lane:
                was = car.passed
                car.update(dt, prev, state)
                if car.passed and not was:
                    self.stats.on_pass(car)
                prev = car
            while lane and lane[0].rear > SIM_SIZE:
                lane.pop(0)
        if self.time >= self._next_metrics:
            self._next_metrics = self.time + 0.25
            self._refresh_metrics()
            self.stats.sample(sum(m["queue"] for m in self.metrics.values()), self.total_cars)

    # metrics ----------------------------------------------------------
    @property
    def total_cars(self):
        return sum(len(l) + len(b) for l, b in zip(self.cars.values(), self.backlog.values()))

    def _refresh_metrics(self):
        for d in DIRECTIONS:
            vis = [c for c in self.cars[d] if not c.passed]
            queued = [c for c in vis if c.speed < 8]
            bl = self.backlog[d]
            waits = [c.waiting_time for c in queued] + [self.time - c.created for c in bl]
            self.metrics[d] = {"cars": len(vis) + len(bl), "queue": len(queued) + len(bl),
                               "avg_wait": sum(waits) / len(waits) if waits else 0.0,
                               "max_wait": max(waits, default=0.0), "backlog": len(bl)}

    def emergency_axis(self):
        """Axis of the emergency vehicle closest to the stop line (or None)."""
        best, axis = -1e9, None
        for d in DIRECTIONS:
            for c in self.cars[d]:
                if c.emergency and not c.passed and c.d > best:
                    best, axis = c.d, AXIS_OF[d]
            if axis is None and any(c.emergency for c in self.backlog[d]):
                axis = AXIS_OF[d]
        return axis
