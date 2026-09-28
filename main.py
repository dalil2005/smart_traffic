"""Smart Traffic Light Intersection - run with:  python main.py"""
import sys
import pygame
from config import *
from simulation.simulation import Simulation
from simulation.comparison import compare_controllers
from ui.renderer import Renderer
from ui.dashboard import Dashboard, TMODES


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Smart Traffic Light Simulation")
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        self.clock = pygame.time.Clock()
        self.renderer, self.dashboard = Renderer(), Dashboard()
        self.density, self.controller, self.speed = DEFAULT_DENSITY, DEFAULT_CONTROLLER, 1
        self.tmode, self.running, self.accum, self.result = "AUTO", True, 0.0, None
        self.sim = self._new_sim()

    def _new_sim(self):
        return Simulation(self.controller, self.density,
                          forced_mode=None if self.tmode == "AUTO" else self.tmode)

    @property
    def state(self):
        return {"running": self.running, "controller": self.controller, "density": self.density,
                "speed": self.speed, "tmode": self.tmode}

    def dispatch(self, key):
        kind, _, val = key.partition(":")
        if kind == "start":
            self.running = True
        elif kind == "pause":
            self.running = False
        elif kind == "reset":
            print(self.sim.stats.report())
            self.sim, self.accum, self.result = self._new_sim(), 0.0, None
        elif kind == "emergency":
            self.sim.traffic.spawn_emergency()
        elif kind in ("fixed", "smart"):
            self.controller = kind.upper()
            self.sim.set_controller(self.controller)
        elif kind == "compare":
            self.run_compare()
        elif kind == "density":
            self.density = self.sim.traffic.density = val
        elif kind == "speed":
            self.speed = float(val) if "." in val else int(val)
        elif kind == "tmode":
            self.tmode = val
            self.sim.traffic.forced_mode = None if val == "AUTO" else val

    def run_compare(self):
        self.renderer.draw(self.screen, self.sim)
        msg = self.dashboard.big.render("Running Fixed vs Smart comparison...", True, (255, 255, 255))
        self.screen.blit(msg, msg.get_rect(center=(SIM_SIZE // 2, SIM_SIZE // 2)))
        pygame.display.flip()
        self.result = compare_controllers(self.density, self.sim.traffic.mode)
        print("Fixed vs Smart:", f"{self.result['wait_improvement']:.1f}% lower average wait")

    def handle(self, ev):
        if ev.type == pygame.QUIT:
            return False
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.result:
                self.result = None
            else:
                key = self.dashboard.click(ev.pos)
                key and self.dispatch(key)
        if ev.type == pygame.KEYDOWN:
            k = ev.key
            if k == pygame.K_ESCAPE:
                if self.result:
                    self.result = None
                else:
                    return False
            elif k == pygame.K_SPACE:
                self.running = not self.running
            elif k == pygame.K_r:
                self.dispatch("reset")
            elif k == pygame.K_f:
                self.dispatch("fixed")
            elif k == pygame.K_s:
                self.dispatch("smart")
            elif k == pygame.K_e:
                self.dispatch("emergency")
            elif k == pygame.K_c:
                self.dispatch("compare")
            elif k == pygame.K_t:
                self.dispatch("tmode:" + TMODES[(TMODES.index(self.tmode) + 1) % len(TMODES)])
            elif pygame.K_1 <= k <= pygame.K_4:
                self.dispatch("density:" + list(DENSITY)[k - pygame.K_1])
        return True

    def frame(self, dt):
        if self.running:
            self.accum += dt * self.speed
            n = 0
            while self.accum >= STEP and n < MAX_STEPS_PER_FRAME:
                self.sim.step(STEP)
                self.accum -= STEP
                n += 1
            if n == MAX_STEPS_PER_FRAME:
                self.accum = 0.0
        self.renderer.draw(self.screen, self.sim)
        self.dashboard.draw(self.screen, self.sim, self.state, pygame.mouse.get_pos())
        if self.result:
            self.dashboard.draw_compare(self.screen, self.result)
        pygame.display.flip()

    def run(self, max_frames=None):
        n, alive = 0, True
        while alive and (max_frames is None or n < max_frames):
            dt = self.clock.tick(FPS) / 1000
            for ev in pygame.event.get():
                alive = self.handle(ev) and alive
            self.frame(min(dt, 0.1))
            n += 1
        print(self.sim.stats.report())
        pygame.quit()


if __name__ == "__main__":
    App().run()
