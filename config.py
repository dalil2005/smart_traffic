"""Central configuration - every tunable of the simulation lives here."""

# ---------------- window / loop ----------------
SIM_SIZE = 800                    # square simulation area (px)
PANEL_W = 480                     # dashboard width
WIN_W, WIN_H = SIM_SIZE + PANEL_W, SIM_SIZE
FPS = 60
STEP = 1 / 30                     # fixed simulation step (s)
MAX_STEPS_PER_FRAME = 60
SPEEDS = [0.5, 1, 2, 5, 10]
COMPARE_STEP = 1 / 15             # step used by the headless Fixed-vs-Smart run
COMPARE_DURATION = 600            # simulated seconds per controller
COMPARE_SEED = 42

# ---------------- geometry ----------------
DIRECTIONS = ("N", "S", "E", "W")           # direction = side the car COMES FROM
AXIS_OF = {"N": "NS", "S": "NS", "E": "EW", "W": "EW"}
OPPOSITE_AXIS = {"NS": "EW", "EW": "NS"}
AXES = {"NS": ("N", "S"), "EW": ("E", "W")}
CX = CY = SIM_SIZE // 2
LANE_W = 44
HALF_ROAD = LANE_W                          # one lane per direction
LANE_OFFSET = LANE_W // 2
SIDEWALK_W = 16
STOP_LINE = CY - HALF_ROAD - 18             # front bumper must stop here
EXIT_LINE = CY + HALF_ROAD

# ---------------- cars ----------------
CAR_LEN, CAR_WID = 32, 18
MIN_GAP = 7
MAX_SPEED_RANGE = (125, 165)                # px/s
ACCEL_RANGE = (70, 110)                     # px/s^2
COMFORT_DECEL = 130
MAX_DECEL = 230

# ---------------- traffic density ----------------
# seconds between spawns PER DIRECTION (random in range)
DENSITY = {"LOW": (5.0, 10.0), "MEDIUM": (3.0, 6.0),
           "HIGH": (2.0, 3.6), "VERY_HIGH": (1.0, 2.2)}
DEFAULT_DENSITY = "MEDIUM"
DEFAULT_CONTROLLER = "FIXED"
# asymmetric traffic makes the smart controller matter (1.0 = neutral)
DIRECTION_WEIGHT = {"N": 1.3, "S": 1.1, "E": 0.8, "W": 0.7}

# ---------------- time of day ----------------
MODE_SCHEDULE = [(0, 6, "NIGHT"), (6, 9, "MORNING_RUSH"), (9, 16, "NORMAL"),
                 (16, 19, "EVENING_RUSH"), (19, 24, "NORMAL")]
MODE_INTERVAL_MULT = {"NIGHT": 2.2, "NORMAL": 1.0,
                      "MORNING_RUSH": 0.65, "EVENING_RUSH": 0.65}
START_HOUR = 12.0
CLOCK_SPEED = 30                            # clock seconds per simulated second

# ---------------- signal timing ----------------
MIN_GREEN = 15
MAX_GREEN = 90
YELLOW_TIME = 4
ALL_RED_TIME = 2
MAX_WAITING_TIME = 120
FIXED_GREEN = 30
MIN_SAFE_GREEN = 8                          # empty-road early termination

# ---------------- smart controller ----------------
BASE_GREEN = 15
CARS_FACTOR = 2.0                           # sec per car
WAIT_FACTOR = 0.2                           # sec per second of average wait
QUEUE_WEIGHT = 1.5
WAIT_WEIGHT = 0.2
WAIT_PRIORITY_WEIGHT = 0.3
STARVATION_BONUS = 1000
SWITCH_RATIO = 1.4                          # switch early if other priority > 1.4x own

# ---------------- emergency ----------------
EMERGENCY_PROB = 0.01                       # per spawned vehicle
EMERGENCY_MIN_GREEN = 4
