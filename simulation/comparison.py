"""Headless Fixed-vs-Smart run: identical seed => identical arrivals, so the
difference measured is purely due to the controller (nothing is hard-coded)."""
from config import *
from simulation.simulation import Simulation


def run_headless(controller, density, mode, duration=COMPARE_DURATION,
                 seed=COMPARE_SEED, step=COMPARE_STEP):
    sim = Simulation(controller, density, seed=seed, forced_mode=mode)
    sim.traffic.emergency_prob = 0.0
    for _ in range(int(duration / step)):
        sim.step(step)
    return sim.summary()


def pct(old, new, lower_is_better=True):
    if old == 0:
        return 0.0
    return (old - new) / old * 100 if lower_is_better else (new - old) / old * 100


def compare_controllers(density, mode, duration=COMPARE_DURATION):
    fixed = run_headless("FIXED", density, mode, duration)
    smart = run_headless("SMART", density, mode, duration)
    return {"fixed": fixed, "smart": smart, "density": density, "mode": mode,
            "duration": duration,
            "wait_improvement": pct(fixed["avg_wait"], smart["avg_wait"]),
            "throughput_gain": pct(fixed["passed"], smart["passed"], False)}
