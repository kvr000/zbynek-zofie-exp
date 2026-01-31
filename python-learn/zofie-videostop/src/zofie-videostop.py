#!/usr/bin/env python3

import pygame
import random
import sys


class VideostopGame:
    WIDTH = 600
    HEIGHT = 300
    ROLL_INTERVAL_MS = 300

    WHITE = (245, 245, 245)
    BLACK = (30, 30, 30)
    GREEN = (40, 160, 60)
    RED = (200, 60, 60)

    DIE_SIZE = 100
    DOT_RADIUS = 10

    DOT_POSITIONS = {
        1: [(0.5, 0.5)],
        2: [(0.25, 0.25), (0.75, 0.75)],
        3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
        4: [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)],
        5: [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75), (0.5, 0.5)],
        6: [(0.25, 0.25), (0.25, 0.5), (0.25, 0.75), (0.75, 0.25), (0.75, 0.5), (0.75, 0.75)]
    }

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Videostop")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 96)
        self.small_font = pygame.font.SysFont(None, 28)

        self.reset()

    def reset(self):
        self.dice = [1, 3, 5]
        self.rolling = True
        self.last_ticks = pygame.time.get_ticks()
        self.roll_interval = self.ROLL_INTERVAL_MS

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

                if event.key == pygame.K_SPACE and self.rolling:
                    self.rolling = False

                if event.key == pygame.K_r:
                    self.reset()

    def update(self):
        if not self.rolling:
            return

        now = pygame.time.get_ticks()

        while now - self.last_ticks >= self.roll_interval:
            self.last_ticks += self.roll_interval
            chosen = random.randrange(0, 3)
            self.dice[chosen] += 1
            if self.dice[chosen] > 6:
                self.dice[chosen] = 1

            # gradual acceleration
            self.roll_interval = max(4, self.roll_interval - 0.01)

    def draw_die(self, value, x, y):
        rect = pygame.Rect(x, y, self.DIE_SIZE, self.DIE_SIZE)
        pygame.draw.rect(self.screen, self.BLACK, rect, border_radius=12)
        for dx, dy in self.DOT_POSITIONS[value]:
            cx = x + dx * self.DIE_SIZE
            cy = y + dy * self.DIE_SIZE
            pygame.draw.circle(self.screen, self.WHITE, (int(cx), int(cy)), self.DOT_RADIUS)

    def draw(self):
        self.screen.fill(self.WHITE)

        spacing = 150
        start_x = 80
        y = 100
        for i, value in enumerate(self.dice):
            self.draw_die(value, start_x + i * spacing, y)

        if self.rolling:
            msg = "Press SPACE to stop"
            color = self.BLACK
        else:
            if self.dice[0] == self.dice[1] == self.dice[2]:
                msg = "VIDEOSTOP! YOU WIN"
                color = self.GREEN
            else:
                msg = "Not equal — press R"
                color = self.RED

        text = self.small_font.render(msg, True, color)
        self.screen.blit(text, text.get_rect(center=(self.WIDTH // 2, 40)))

        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

        return 0


if __name__ == "__main__":
    sys.exit(VideostopGame().run())
