from config import *
from ai.traffic_score import traffic_score


class PrioritySystem:
    """Aggregates the two approaches of an axis and ranks axes by need."""

    def axis_metrics(self, metrics, axis):
        ms = [metrics[d] for d in AXES[axis]]
        cars = sum(m["cars"] for m in ms)
        queue = sum(m["queue"] for m in ms)
        aw = sum(m["avg_wait"] * m["queue"] for m in ms) / queue if queue else 0.0
        return {"cars": cars, "queue": queue, "avg_wait": aw,
                "max_wait": max(m["max_wait"] for m in ms),
                "score": traffic_score(cars, queue, aw)}

    def is_starving(self, m):
        return m["max_wait"] >= MAX_WAITING_TIME

    def priority(self, m):
        p = m["score"] + WAIT_PRIORITY_WEIGHT * m["max_wait"]
        return p + (STARVATION_BONUS if self.is_starving(m) else 0)
