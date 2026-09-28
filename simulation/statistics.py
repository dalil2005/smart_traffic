from config import AXES


class Statistics:
    def __init__(self):
        self.generated = 0
        self.passed = 0
        self.wait_sum = 0.0
        self.wait_max = 0.0
        self.q_sum = 0.0
        self.cars_sum = 0.0
        self.samples = 0
        self.green_time = {a: 0.0 for a in AXES}
        self.red_time = {a: 0.0 for a in AXES}
        self.elapsed = 0.0

    def on_pass(self, car):
        self.passed += 1
        self.wait_sum += car.waiting_time
        self.wait_max = max(self.wait_max, car.waiting_time)

    def sample(self, queue, cars):
        self.samples += 1
        self.q_sum += queue
        self.cars_sum += cars

    def tick(self, dt, axis, phase):
        self.elapsed += dt
        for a in AXES:
            if a == axis and phase == "GREEN":
                self.green_time[a] += dt
            else:
                self.red_time[a] += dt

    @property
    def avg_wait(self):
        return self.wait_sum / self.passed if self.passed else 0.0

    @property
    def avg_queue(self):
        return self.q_sum / self.samples if self.samples else 0.0

    @property
    def avg_cars(self):
        return self.cars_sum / self.samples if self.samples else 0.0

    def summary(self):
        return {"generated": self.generated, "passed": self.passed,
                "avg_wait": self.avg_wait, "max_wait": self.wait_max,
                "avg_queue": self.avg_queue, "avg_cars": self.avg_cars,
                "green_time": dict(self.green_time), "red_time": dict(self.red_time),
                "elapsed": self.elapsed}

    def report(self):
        s = self.summary()
        return ("Simulation Results\n"
                f"  Cars Generated: {s['generated']}\n  Cars Passed: {s['passed']}\n"
                f"  Average Waiting Time: {s['avg_wait']:.1f} sec\n"
                f"  Maximum Waiting Time: {s['max_wait']:.0f} sec\n"
                f"  Average Queue: {s['avg_queue']:.1f} cars")
