RED, YELLOW, GREEN = "RED", "YELLOW", "GREEN"
ALL_RED = "ALL_RED"          # controller phase (all lights red)


class TrafficLight:
    def __init__(self, direction):
        self.direction = direction
        self.state = RED

    def set(self, state):
        self.state = state
