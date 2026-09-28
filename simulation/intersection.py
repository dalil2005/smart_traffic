from config import DIRECTIONS, AXIS_OF
from simulation.traffic_light import TrafficLight, RED, YELLOW, GREEN, ALL_RED


class Intersection:
    """Four approaches (N/S/E/W), one traffic light each."""

    def __init__(self):
        self.lights = {d: TrafficLight(d) for d in DIRECTIONS}

    def apply(self, axis, phase):
        for d in DIRECTIONS:
            if phase == ALL_RED or AXIS_OF[d] != axis:
                state = RED
            else:
                state = GREEN if phase == GREEN else YELLOW
            self.lights[d].set(state)
