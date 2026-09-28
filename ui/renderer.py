import random
import pygame
from config import *
from simulation.traffic_light import RED, YELLOW, GREEN

GRASS = (52, 128, 68)
SIDEWALK = (176, 174, 168)
ROAD = (56, 59, 65)
LIGHT_COL = {RED: (255, 62, 62), YELLOW: (255, 190, 40), GREEN: (50, 232, 112)}
ROOFS = [(160, 84, 70), (110, 120, 135), (190, 160, 110), (95, 110, 90), (150, 140, 160)]
# (cx, cy, orientation) of each traffic-light housing
LIGHT_POS = {"N": (CX - HALF_ROAD - 8, STOP_LINE - 34, "v"),
             "S": (CX + HALF_ROAD + 8, SIM_SIZE - STOP_LINE + 34, "v"),
             "W": (STOP_LINE - 34, CY + HALF_ROAD + 8, "h"),
             "E": (SIM_SIZE - STOP_LINE + 34, CY - HALF_ROAD - 8, "h")}
# stop-line rectangle per approach (drawn in the light's colour)
STOP_RECT = {"N": (CX - HALF_ROAD, STOP_LINE, HALF_ROAD, 4),
             "S": (CX, SIM_SIZE - STOP_LINE - 4, HALF_ROAD, 4),
             "W": (STOP_LINE, CY, 4, HALF_ROAD),
             "E": (SIM_SIZE - STOP_LINE - 4, CY - HALF_ROAD, 4, HALF_ROAD)}
ANGLE = {"W": 0, "E": 180, "N": -90, "S": 90}


class Renderer:
    def __init__(self):
        self.bg = self._build_background()
        self.cache, self.glows = {}, {}
        self.font = pygame.font.SysFont("Arial", 12, bold=True)
        self.night = pygame.Surface((SIM_SIZE, SIM_SIZE), pygame.SRCALPHA)
        self.night.fill((0, 0, 35, 115))

    # ------------------------------------------------------------ background
    def _build_background(self):
        rng = random.Random(11)
        s = pygame.Surface((SIM_SIZE, SIM_SIZE))
        s.fill(GRASS)
        for _ in range(900):
            g = rng.randint(-10, 10)
            pygame.draw.circle(s, (52 + g, 128 + g, 68 + g),
                               (rng.randrange(SIM_SIZE), rng.randrange(SIM_SIZE)), rng.randint(1, 3))
        lo, hi = CX - HALF_ROAD - SIDEWALK_W, CX + HALF_ROAD + SIDEWALK_W
        for x0, y0 in ((0, 0), (hi, 0), (0, hi), (hi, hi)):           # city blocks
            for gx in range(2):
                for gy in range(2):
                    cell = pygame.Rect(x0 + gx * 170 + 14, y0 + gy * 170 + 14, 142, 142)
                    if rng.random() < 0.65:
                        w, h = rng.randint(80, 130), rng.randint(80, 130)
                        r = pygame.Rect(0, 0, w, h)
                        r.center = cell.center
                        pygame.draw.rect(s, (30, 70, 40), r.move(6, 6), border_radius=4)
                        roof = rng.choice(ROOFS)
                        pygame.draw.rect(s, roof, r, border_radius=4)
                        pygame.draw.rect(s, tuple(c - 35 for c in roof), r, 3, border_radius=4)
                        pygame.draw.rect(s, tuple(min(255, c + 30) for c in roof), r.inflate(-w // 2, -h // 2))
                    else:
                        for _ in range(6):
                            p = (rng.randint(cell.left + 14, cell.right - 14), rng.randint(cell.top + 14, cell.bottom - 14))
                            rad = rng.randint(12, 17)
                            pygame.draw.circle(s, (24, 92, 46), (p[0] + 3, p[1] + 3), rad)
                            pygame.draw.circle(s, (38, 122, 62), p, rad)
                            pygame.draw.circle(s, (70, 160, 88), (p[0] - 4, p[1] - 4), rad // 2)
        sw = SIDEWALK_W
        pygame.draw.rect(s, SIDEWALK, (lo, 0, hi - lo, SIM_SIZE))
        pygame.draw.rect(s, SIDEWALK, (0, lo, SIM_SIZE, hi - lo))
        pygame.draw.rect(s, ROAD, (CX - HALF_ROAD, 0, 2 * HALF_ROAD, SIM_SIZE))
        pygame.draw.rect(s, ROAD, (0, CY - HALF_ROAD, SIM_SIZE, 2 * HALF_ROAD))
        yellow, white = (240, 200, 60), (235, 235, 235)
        far = SIM_SIZE - STOP_LINE
        for a in range(0, STOP_LINE - 10, 26):                       # dashed centre lines
            pygame.draw.rect(s, yellow, (CX - 1, a, 3, 14))
            pygame.draw.rect(s, yellow, (a, CY - 1, 14, 3))
        for a in range(far + 10, SIM_SIZE, 26):
            pygame.draw.rect(s, yellow, (CX - 1, a, 3, 14))
            pygame.draw.rect(s, yellow, (a, CY - 1, 14, 3))
        for a, b in ((CX - HALF_ROAD, CX + HALF_ROAD - 2), ):        # road edge lines
            pygame.draw.rect(s, white, (a, 0, 2, CY - HALF_ROAD - 14))
            pygame.draw.rect(s, white, (b, 0, 2, CY - HALF_ROAD - 14))
            pygame.draw.rect(s, white, (a, CY + HALF_ROAD + 14, 2, SIM_SIZE))
            pygame.draw.rect(s, white, (b, CY + HALF_ROAD + 14, 2, SIM_SIZE))
            pygame.draw.rect(s, white, (0, CY - HALF_ROAD, CX - HALF_ROAD - 14, 2))
            pygame.draw.rect(s, white, (0, CY + HALF_ROAD - 2, CX - HALF_ROAD - 14, 2))
            pygame.draw.rect(s, white, (CX + HALF_ROAD + 14, CY - HALF_ROAD, SIM_SIZE, 2))
            pygame.draw.rect(s, white, (CX + HALF_ROAD + 14, CY + HALF_ROAD - 2, SIM_SIZE, 2))
        for a in range(CX - HALF_ROAD + 4, CX + HALF_ROAD - 4, 12):  # zebra crossings
            pygame.draw.rect(s, white, (a, CY - HALF_ROAD - 14, 6, 11))
            pygame.draw.rect(s, white, (a, CY + HALF_ROAD + 3, 6, 11))
            pygame.draw.rect(s, white, (CX - HALF_ROAD - 14, a, 11, 6))
            pygame.draw.rect(s, white, (CX + HALF_ROAD + 3, a, 11, 6))
        return s

    # ------------------------------------------------------------ cars
    def _sprite(self, car, phase):
        key = (car.kind, car.color, car.direction, car.braking, phase)
        spr = self.cache.get(key)
        if spr:
            return spr
        L, W = int(car.length), CAR_WID
        surf = pygame.Surface((L, W), pygame.SRCALPHA)
        body = car.color
        dark = tuple(max(0, c - 70) for c in body)
        pygame.draw.rect(surf, body, (0, 0, L, W), border_radius=5)
        pygame.draw.rect(surf, dark, (0, 0, L, W), 1, border_radius=5)
        glass = (110, 160, 195)
        if car.kind == "police":
            pygame.draw.rect(surf, (240, 240, 240), (int(L * .3), 0, int(L * .22), W))
        elif car.kind == "firetruck":
            pygame.draw.rect(surf, (200, 200, 205), (3, W // 2 - 2, int(L * .5), 4))
        pygame.draw.rect(surf, glass, (int(L * .60), 2, int(L * .17), W - 4), border_radius=2)
        pygame.draw.rect(surf, glass, (int(L * .10), 3, int(L * .10), W - 6), border_radius=2)
        if not car.emergency:
            roof = tuple(min(255, c + 22) for c in body)
            pygame.draw.rect(surf, roof, (int(L * .28), 3, int(L * .30), W - 6), border_radius=3)
        else:
            a, b = ((255, 40, 40), (40, 90, 255)) if phase == 0 else ((40, 90, 255), (255, 40, 40))
            bx = int(L * .40)
            pygame.draw.rect(surf, a, (bx, 3, 5, W // 2 - 3))
            pygame.draw.rect(surf, b, (bx, W // 2, 5, W // 2 - 3))
            if car.kind == "ambulance":
                pygame.draw.rect(surf, (220, 30, 30), (int(L * .2), W // 2 - 1, 10, 3))
        pygame.draw.rect(surf, (255, 250, 205), (L - 3, 2, 3, 4))
        pygame.draw.rect(surf, (255, 250, 205), (L - 3, W - 6, 3, 4))
        tail = (255, 35, 35) if car.braking else (125, 20, 20)
        pygame.draw.rect(surf, tail, (0, 2, 2, 4))
        pygame.draw.rect(surf, tail, (0, W - 6, 2, 4))
        spr = pygame.transform.rotate(surf, ANGLE[car.direction])
        self.cache[key] = spr
        return spr

    # ------------------------------------------------------------ lights
    def _glow(self, color):
        g = self.glows.get(color)
        if g is None:
            g = pygame.Surface((44, 44), pygame.SRCALPHA)
            for r, a in ((21, 22), (17, 40), (13, 70)):
                pygame.draw.circle(g, (*color, a), (22, 22), r)
            self.glows[color] = g
        return g

    def _draw_lights(self, screen, sim):
        for d in DIRECTIONS:
            state = sim.intersection.lights[d].state
            sr = pygame.Rect(STOP_RECT[d])
            pygame.draw.rect(screen, LIGHT_COL[state], sr)                # stop line shows the state
            cx, cy, o = LIGHT_POS[d]
            hw, hh = (16, 44) if o == "v" else (44, 16)
            pygame.draw.rect(screen, (18, 18, 22), (cx - hw // 2, cy - hh // 2, hw, hh), border_radius=5)
            pygame.draw.rect(screen, (90, 90, 100), (cx - hw // 2, cy - hh // 2, hw, hh), 1, border_radius=5)
            for i, st in enumerate((RED, YELLOW, GREEN)):
                off = (i - 1) * 14
                p = (cx, cy + off) if o == "v" else (cx + off, cy)
                col = LIGHT_COL[st]
                if st == state:
                    screen.blit(self._glow(col), self._glow(col).get_rect(center=p))
                    pygame.draw.circle(screen, col, p, 5)
                    pygame.draw.circle(screen, (255, 255, 255), (p[0] - 1, p[1] - 1), 2)
                else:
                    pygame.draw.circle(screen, tuple(c // 5 for c in col), p, 5)
            rem = sim.controller.remaining(AXIS_OF[d]) if state in (GREEN, YELLOW) else None
            if rem is not None:
                t = self.font.render(str(int(rem + 0.99)), True, LIGHT_COL[state])
                off = {"N": (0, -34), "S": (0, 34), "W": (-38, 0), "E": (38, 0)}[d]
                screen.blit(t, t.get_rect(center=(cx + off[0], cy + off[1])))

    # ------------------------------------------------------------ frame
    def draw(self, screen, sim):
        screen.set_clip(pygame.Rect(0, 0, SIM_SIZE, SIM_SIZE))
        screen.blit(self.bg, (0, 0))
        t = sim.traffic.time
        phase = int(t * 4) % 2
        for d in DIRECTIONS:
            for car in sim.traffic.cars[d]:
                spr = self._sprite(car, phase if car.emergency else 0)
                screen.blit(spr, spr.get_rect(center=(int(car.x), int(car.y))))
        if sim.traffic.mode == "NIGHT":
            screen.blit(self.night, (0, 0))
        self._draw_lights(screen, sim)
        screen.set_clip(None)
