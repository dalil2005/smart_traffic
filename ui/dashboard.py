import pygame
from config import *
from simulation.traffic_light import RED, YELLOW, GREEN

BG, CARD, TEXT, MUTED, ACCENT = (22, 25, 31), (33, 37, 46), (226, 231, 238), (140, 150, 165), (64, 156, 255)
STATE_COL = {RED: (255, 85, 85), YELLOW: (255, 196, 60), GREEN: (70, 224, 120)}
NAMES = {"N": "North", "S": "South", "E": "East", "W": "West"}
TMODES = ["AUTO", "NIGHT", "NORMAL", "MORNING_RUSH", "EVENING_RUSH"]
TMODE_LABEL = {"AUTO": "AUTO", "NIGHT": "NIGHT", "NORMAL": "NORMAL",
               "MORNING_RUSH": "AM RUSH", "EVENING_RUSH": "PM RUSH"}


class Button:
    def __init__(self, key, label, rect, active=None):
        self.key, self.label, self.rect, self.active = key, label, rect, active


class Dashboard:
    def __init__(self):
        f = lambda n, b=False: pygame.font.Font(None, n)
        self.h1, self.h2, self.body, self.small, self.big = f(20, True), f(14, True), f(13), f(12), f(26, True)
        self.buttons = self._build()

    def _build(self):
        x0, w, out = SIM_SIZE + 12, PANEL_W - 24, []

        def row(y, items, h=32):
            gap = 6
            bw = (w - gap * (len(items) - 1)) / len(items)
            for i, (k, l, a) in enumerate(items):
                out.append(Button(k, l, pygame.Rect(int(x0 + i * (bw + gap)), y, int(bw), h), a))

        row(500, [("start", "START", lambda s: s["running"]), ("pause", "PAUSE", lambda s: not s["running"]),
                  ("reset", "RESET", None), ("emergency", "EMERGENCY [E]", None)])
        row(542, [("fixed", "FIXED [F]", lambda s: s["controller"] == "FIXED"),
                  ("smart", "SMART [S]", lambda s: s["controller"] == "SMART"), ("compare", "COMPARE [C]", None)])
        row(604, [(f"density:{k}", k.replace("_", " "), (lambda s, k=k: s["density"] == k)) for k in DENSITY], 30)
        row(658, [(f"speed:{v}", f"{v}x", (lambda s, v=v: s["speed"] == v)) for v in SPEEDS], 30)
        row(712, [(f"tmode:{m}", TMODE_LABEL[m], (lambda s, m=m: s["tmode"] == m)) for m in TMODES], 30)
        return out

    def click(self, pos):
        for b in self.buttons:
            if b.rect.collidepoint(pos):
                return b.key
        return None

    def _text(self, screen, font, txt, pos, color=TEXT):
        screen.blit(font.render(txt, True, color), pos)

    def draw(self, screen, sim, state, mouse):
        x0 = SIM_SIZE
        pygame.draw.rect(screen, BG, (x0, 0, PANEL_W, WIN_H))
        tm, ctl = sim.traffic, sim.controller
        self._text(screen, self.h1, "SMART TRAFFIC CONTROL", (x0 + 12, 8))
        hh, mm = int(tm.clock // 3600), int(tm.clock // 60) % 60
        self._text(screen, self.body, f"Controller: {ctl.name}   |   Mode: {tm.mode.replace('_', ' ')}   |   {hh:02d}:{mm:02d}",
                   (x0 + 12, 36), MUTED)
        for i, d in enumerate(("N", "S", "E", "W")):
            r = pygame.Rect(x0 + 8 + (i % 2) * 238, 60 + (i // 2) * 116, 226, 110)
            pygame.draw.rect(screen, CARD, r, border_radius=8)
            m, st = tm.metrics[d], sim.intersection.lights[d].state
            pygame.draw.circle(screen, STATE_COL[st], (r.right - 16, r.y + 16), 7)
            self._text(screen, self.h2, NAMES[d], (r.x + 10, r.y + 7))
            rem = ctl.remaining(AXIS_OF[d])
            extra = f" (+{m['backlog']} off-map)" if m["backlog"] else ""
            lines = [(f"Cars: {m['cars']}{extra}", TEXT), (f"Queue: {m['queue']}", TEXT),
                     (f"Average Wait: {m['avg_wait']:.0f}s", TEXT), (f"Signal: {st}", STATE_COL[st]),
                     (f"Remaining: {int(rem + 0.99)}s" if rem is not None else "Remaining: --", MUTED)]
            for j, (t, c) in enumerate(lines):
                self._text(screen, self.body, t, (r.x + 10, r.y + 28 + j * 16), c)
        s = sim.summary()
        y = 300
        self._text(screen, self.h2, "STATISTICS", (x0 + 12, y))
        waiting = s["waiting"]
        left = [f"Cars Generated: {s['generated']}", f"Cars Passed: {s['passed']}",
                f"Cars Waiting: {waiting}", f"Total Cars: {tm.total_cars}",
                f"Average Wait: {s['avg_wait']:.1f}s", f"Maximum Wait: {s['max_wait']:.0f}s"]
        el = max(s["elapsed"], 1)
        right = [f"Average Queue: {s['avg_queue']:.1f}", f"Density (avg cars): {s['avg_cars']:.1f}",
                 f"Green NS/EW: {s['green_time']['NS']:.0f}/{s['green_time']['EW']:.0f}s",
                 f"Red NS/EW: {s['red_time']['NS']:.0f}/{s['red_time']['EW']:.0f}s",
                 f"Throughput: {s['passed'] / el * 60:.1f}/min", f"Sim time: {int(el // 60)}:{int(el % 60):02d}"]
        for j, (a, b) in enumerate(zip(left, right)):
            self._text(screen, self.body, a, (x0 + 14, y + 26 + j * 22))
            self._text(screen, self.body, b, (x0 + 250, y + 26 + j * 22))
        for b in self.buttons:
            on = bool(b.active and b.active(state))
            col = ACCENT if on else ((78, 86, 102) if b.rect.collidepoint(mouse) else (54, 60, 74))
            pygame.draw.rect(screen, col, b.rect, border_radius=6)
            t = self.small.render(b.label, True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=b.rect.center))
        for txt, yy in (("Traffic density", 586), ("Simulation speed", 640), ("Time of day  [T] / keys 1-4 = density", 694)):
            self._text(screen, self.small, txt, (x0 + 14, yy), MUTED)
        self._text(screen, self.small, "SPACE pause | R reset | E emergency | C compare | ESC quit",
                   (x0 + 14, 756), MUTED)

    def draw_compare(self, screen, r):
        box = pygame.Rect(0, 0, 560, 380)
        box.center = (SIM_SIZE // 2, SIM_SIZE // 2)
        pygame.draw.rect(screen, (18, 20, 26), box, border_radius=12)
        pygame.draw.rect(screen, ACCENT, box, 2, border_radius=12)
        self._text(screen, self.h1, "Fixed vs Smart - measured in simulation", (box.x + 20, box.y + 16))
        self._text(screen, self.small, f"Density {r['density']} | mode {r['mode']} | {r['duration']}s simulated | same random arrivals for both",
                   (box.x + 20, box.y + 46), MUTED)
        f, s = r["fixed"], r["smart"]
        rows = [("Cars generated", f["generated"], s["generated"], None),
                ("Cars passed", f["passed"], s["passed"], r["throughput_gain"]),
                ("Avg waiting time (s)", round(f["avg_wait"], 1), round(s["avg_wait"], 1), r["wait_improvement"]),
                ("Max waiting time (s)", round(f["max_wait"]), round(s["max_wait"]), None),
                ("Avg queue (cars)", round(f["avg_queue"], 1), round(s["avg_queue"], 1), None)]
        for x, h in ((box.x + 20, "Metric"), (box.x + 270, "Fixed"), (box.x + 360, "Smart"), (box.x + 450, "Change")):
            self._text(screen, self.h2, h, (x, box.y + 80), MUTED)
        for i, (n, a, b, ch) in enumerate(rows):
            yy = box.y + 110 + i * 30
            self._text(screen, self.body, n, (box.x + 20, yy))
            self._text(screen, self.body, str(a), (box.x + 270, yy))
            self._text(screen, self.body, str(b), (box.x + 360, yy))
            if ch is not None:
                self._text(screen, self.body, f"{ch:+.1f}%", (box.x + 450, yy), STATE_COL[GREEN] if ch > 0 else STATE_COL[RED])
        imp = r["wait_improvement"]
        self._text(screen, self.h2, "Improvement in average waiting time", (box.x + 20, box.y + 285))
        self._text(screen, self.big, f"{imp:.1f}%", (box.x + 20, box.y + 305), STATE_COL[GREEN] if imp > 0 else STATE_COL[RED])
        self._text(screen, self.small, "Click or press ESC to close", (box.x + 380, box.y + 350), MUTED)
