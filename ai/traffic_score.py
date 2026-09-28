from config import *


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def traffic_score(cars, queue, avg_wait):
    """cars + queue*1.5 + avg_wait*0.2"""
    return cars + QUEUE_WEIGHT * queue + WAIT_WEIGHT * avg_wait


def dynamic_green_time(cars, avg_wait):
    """Base + 2s*cars + 0.2*avg_wait, clamped to [MIN_GREEN, MAX_GREEN]."""
    return clamp(BASE_GREEN + CARS_FACTOR * cars + WAIT_FACTOR * avg_wait, MIN_GREEN, MAX_GREEN)
