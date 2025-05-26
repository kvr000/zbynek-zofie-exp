#!/usr/bin/env python3

import random
import time
from typing import List, Tuple
import pgzrun  # pgzero runtime
from pgzero.screen import Screen
from pygame import Rect
import pygame

# Constants
WIDTH = 800
HEIGHT = 600
CELL_WIDTH = 10
CELL_HEIGHT = 10
COLS = WIDTH // CELL_WIDTH
ROWS = HEIGHT // CELL_HEIGHT
TRACK_WIDTH = 20

class RacingGame:
    start_speed: float = 20.0
    max_speed: float = 84.0
    acceleration: float = 0.02

    state: int # -1 crashed, 0 pause, 1 running
    track: List[Tuple[int, int]]
    track_offset: int
    offset_dir: int
    offset_counter: int
    kerb_offset: int

    player_pos: int
    player_dir: int

    next_update_time: float
    speed: float
    distance: int

    is_fullscreen: bool = False

    def __init__(self):
        self.initialize_game()

    def initialize_game(self) -> None:
        self.state = 0
        self.track = []
        self.track_offset = COLS // 2 - TRACK_WIDTH // 2
        self.offset_dir = 0
        self.offset_counter = 0
        self.kerb_offset = 0

        self.player_pos = COLS // 2
        self.player_dir = 0

        self.next_update_time = time.time()
        self.speed = self.start_speed
        self.distance = 0

        for _ in range(ROWS):
            self.track.append((self.track_offset, self.track_offset + TRACK_WIDTH))

    def update_track(self) -> None:
        if self.offset_counter == 0:
            self.offset_dir = random.choice([-1, 0, 1])
            self.offset_counter = random.randint(10, 40)

        new_offset = self.track_offset + self.offset_dir
        new_offset = max(1, min(COLS - TRACK_WIDTH - 1, new_offset))

        self.track.append((new_offset, new_offset + TRACK_WIDTH))
        if len(self.track) > ROWS:
            self.track.pop(0)
            self.kerb_offset = 1 - self.kerb_offset

        self.track_offset = new_offset
        self.offset_counter -= 1

    def update_car(self) -> bool:
        if self.player_pos < self.track[1][0] or self.player_pos >= self.track[1][1]:
            self.state = -1
            return False

        if self.player_dir < 0 and self.player_pos > 0:
            self.player_pos -= 1
        elif self.player_dir > 0 and self.player_pos < COLS - 1:
            self.player_pos += 1

        return True

    def update(self) -> None:
        now = time.time()
        while self.state == 1 and now >= self.next_update_time:
            if self.update_car():
                self.update_track()

                self.distance += 1

                self.speed = min(self.max_speed, self.speed + self.acceleration)

                self.next_update_time = self.next_update_time + 1 / self.speed

    def draw(self, screen: Screen) -> None:
        screen.clear()
        for y, (left_col, right_col) in enumerate(self.track):
            top = (ROWS - y - 1) * CELL_HEIGHT
            left = left_col * CELL_WIDTH
            right = right_col * CELL_WIDTH

            # Green grass
            screen.draw.filled_rect(Rect(0, top, left, CELL_HEIGHT), "lime green")
            screen.draw.filled_rect(Rect(right, top, COLS * CELL_WIDTH - right, CELL_HEIGHT), " lime green")

            # Kerbs
            screen.draw.filled_rect(
                Rect(left, top, CELL_WIDTH, CELL_HEIGHT),
                ("white", "cyan")[(y + self.kerb_offset) & 1]
            )
            screen.draw.filled_rect(
                Rect(right - CELL_WIDTH, top, CELL_WIDTH, CELL_HEIGHT),
                ("white", "cyan")[(y + self.kerb_offset + 1) & 1]
            )

            # Track surface
            screen.draw.filled_rect(
                Rect(left + CELL_WIDTH, top, right - left - 2 * CELL_WIDTH, CELL_HEIGHT),
                "gray"
            )

        # Draw car
        self.draw_car(screen.surface, Rect(self.player_pos * CELL_WIDTH, (ROWS - 2) * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

        # Statistics
        screen.draw.text(f"Speed: {self.speed * 3.6:.1f} km/h", (5, 0), fontsize=CELL_HEIGHT * 3, color="darkorange")
        screen.draw.text(f"Distance: {self.distance / 1000.0:.3f} km", topright=(WIDTH - 5, 0), fontsize=CELL_HEIGHT * 3, color="cyan")

        # Crash
        if self.state < 0:
            screen.draw.text("you crashed!", center=(WIDTH // 2, HEIGHT // 2), fontsize=CELL_HEIGHT * 10, color="cyan")

    def draw_car(self, surface: pygame.Surface, cell_rect: pygame.Rect, color = "orange") -> None:
        car_surface = pygame.Surface((CELL_WIDTH * 3, CELL_HEIGHT * 3), pygame.SRCALPHA)

        x, y, w, h = CELL_WIDTH, CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT
        cx, cy = x + w // 2, y + h // 2

        # Scaling factors based on cell size
        body_width = int(w * 0.6)
        body_height = int(h * 1.4)
        wing_width = int(w * 0.90)
        wing_height = max(1, h // 10)
        tire_radius = max(1, min(w, h) // 5)

        # Body
        body_rect = pygame.Rect(0, 0, body_width, body_height)
        body_rect.center = (cx, cy)
        pygame.draw.rect(car_surface, color, body_rect)

        # Front and rear wings
        pygame.draw.rect(car_surface, (0, 0, 0), (cx - wing_width // 2, y - wing_height, wing_width, wing_height))  # Front
        pygame.draw.rect(car_surface, (0, 0, 0), (cx - wing_width // 2, y + h, wing_width, wing_height))  # Rear

        # Cockpit
        pygame.draw.ellipse(car_surface,(50,50,50) , (cx - w // 8, cy - h // 12, w // 4, h // 6))

        # Tires
        tire_offsets = [
            (-w * 0.5, -h * 0.4),
            (w * 0.5, -h * 0.4),
            (-w * 0.5, h * 0.4),
            (w * 0.5, h * 0.4),
        ]
        for dx, dy in tire_offsets:
            pygame.draw.circle(car_surface,("limegreen"), (int(cx + dx), int(cy + dy)), tire_radius)

        rotated = pygame.transform.rotozoom(car_surface, (45, 0, -45)[self.player_dir + 1], 1)
        target_rect = rotated.get_rect(center=cell_rect.center)
        surface.blit(rotated, target_rect)

    def reinit_game(self):
        pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED if self.is_fullscreen else 0)
        pygame.display.set_caption("Zofie Racer Game")
        car_surface = pygame.Surface((CELL_WIDTH, CELL_HEIGHT), pygame.SRCALPHA)
        game.draw_car(car_surface, Rect(0, 0, CELL_WIDTH, CELL_HEIGHT))
        pygame.display.set_icon(car_surface)

    def on_key_down(self, key) -> None:
        if key.name == "SPACE":
            if self.state == -1:
                self.initialize_game()
                self.state = 0
            elif self.state == 1:
                self.state = 0
            return
        elif key.name == "Q":
            exit()
        elif key.name == "F":
            self.is_fullscreen = not self.is_fullscreen
            self.reinit_game()
            if self.state == 1:
                self.state = 0
        if self.state >= 0:
            if key.name == "LEFT":
                self.player_dir = -1
            elif key.name == "RIGHT":
                self.player_dir = 1
            elif key.name == "UP" or key.name == "DOWN":
                self.player_dir = 0
            else:
                return
            if self.state == 0:
                self.state = 1
                self.next_update_time = time.time()

# Create game instance
game = RacingGame()

# Pygame Zero callbacks
def draw():
    game.draw(screen)

def update():
    game.update()

def on_key_down(key):
    game.on_key_down(key)

pgzrun.go()
