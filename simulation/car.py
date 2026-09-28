import itertools
import math
from config import *
from simulation.traffic_light import RED, YELLOW

_ids = itertools.count(1)
CAR_COLORS = [(214, 48, 49), (9, 132, 227), (0, 184, 148), (253, 203, 110),
              (108, 92, 231), (232, 67, 147), (225, 112, 85), (99, 110, 114),
              (236, 240, 241), (45, 52, 54), (0, 206, 201), (250, 177, 160)]


def safe_speed(gap, lead_speed=0.0):
    """Highest speed from which the car can still stop within `gap`."""
    return math.sqrt(lead_speed ** 2 + 2 * COMFORT_DECEL * max(gap, 0.0))


class Car:
    kind = "car"
    emergency = False
    length = CAR_LEN

    def __init__(self, direction, rng, created=0.0):
        self.id = next(_ids)
        self.direction = direction          # side it comes from
        self.lane = 0
        self.d = -self.length / 2           # centre distance travelled along its axis
        self.max_speed = rng.uniform(*MAX_SPEED_RANGE)
        self.acceleration = rng.uniform(*ACCEL_RANGE)
        self.speed = self.max_speed * 0.7
        self.waiting_time = 0.0
        self.stopped = False
        self.braking = False
        self.color = rng.choice(CAR_COLORS)
        self.passed = False                 # front bumper crossed the stop line
        self.committed = False              # chose to run the yellow
        self.created = created

    # geometry ---------------------------------------------------------
    @property
    def front(self):
        return self.d + self.length / 2

    @property
    def rear(self):
        return self.d - self.length / 2

    @property
    def x(self):
        return {"N": CX - LANE_OFFSET, "S": CX + LANE_OFFSET,
                "W": self.d, "E": SIM_SIZE - self.d}[self.direction]

    @property
    def y(self):
        return {"W": CY + LANE_OFFSET, "E": CY - LANE_OFFSET,
                "N": self.d, "S": SIM_SIZE - self.d}[self.direction]

    # behaviour --------------------------------------------------------
    def update(self, dt, leader, light_state):
        front = self.front
        target = self.max_speed
        limit = float("inf")                # max distance we may move this step

        if leader is not None:              # car following
            gap = leader.rear - front - MIN_GAP
            limit = max(gap, 0.0)
            target = min(target, safe_speed(gap, leader.speed))

        if not self.passed:                 # traffic light
            dist = max(STOP_LINE - front, 0.0)
            stop = False
            if light_state == RED and not self.committed:
                stop = True
            elif light_state == YELLOW and not self.committed:
                if self.speed ** 2 / (2 * MAX_DECEL) > dist:
                    self.committed = True   # too close to stop safely: go
                else:
                    stop = True
            if stop:
                limit = min(limit, dist)
                target = min(target, safe_speed(dist) if dist > 1.0 else 0.0)

        old = self.speed
        if target > old:
            self.speed = min(target, old + self.acceleration * dt)
        else:
            self.speed = max(target, old - MAX_DECEL * dt)
        move = self.speed * dt
        if move > limit:
            move = limit
            self.speed = move / dt
        self.d += move

        self.stopped = self.speed < 3
        self.braking = self.speed < old - 0.5 or self.stopped
        if not self.passed:
            if self.front > STOP_LINE + 0.01:
                self.passed = True
            elif self.speed < 5:
                self.waiting_time += dt


class EmergencyVehicle(Car):
    emergency = True
    length = 38
    COLORS = {"ambulance": (245, 245, 245), "firetruck": (200, 30, 30),
              "police": (30, 60, 150)}

    def __init__(self, direction, rng, created=0.0, kind=None):
        super().__init__(direction, rng, created)
        self.kind = kind or rng.choice(tuple(self.COLORS))
        self.color = self.COLORS[self.kind]
        self.max_speed = rng.uniform(170, 200)
        self.acceleration = 130
        self.speed = self.max_speed * 0.6
