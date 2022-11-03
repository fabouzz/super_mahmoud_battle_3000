"""Super Mahmoud Battle 3000."""
import numpy as np
import pygame
from pygame.locals import K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, KEYDOWN, QUIT

# Initialize Pygame and game clock
pygame.init()
clock = pygame.time.Clock()

SIZE = WIDTH, HEIGHT = 1080, 720
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
global G
G = 9.81


class Projectile:
    """Default class for a projectile with parabolic motion."""

    def __init__(self, x0, y0, v0):
        """Construct of the Projectile class."""
        self.v: list[float] = v0
        self.coords: list[float] = [x0, y0]
        self.mass = 10
        self.radius = 7

    def is_onscreen(self):
        """Check if the projectile is on screen or above."""
        x, y = self.coords
        if x > 0 and x < WIDTH and y < HEIGHT:
            return True
        return False

    def update(self):
        """Update the coordiates of the projectile."""
        dt = clock.get_time() * 1e-3
        self.v[1] += self.mass * G * dt
        self.coords[0] += self.v[0]
        self.coords[1] += self.v[1]

    def draw(self, surface):
        """Draw the projectile on screen."""
        pygame.draw.circle(surface, RED, self.coords, self.radius)


class Tank:
    """Player controlled tank.

    Methods : update, draw
    """

    def __init__(self, coords=(100, 500), shape=(30, 15)):
        """Construct Tank class."""
        # Coords of the top left corner of the tank chassis
        self.coords = coords
        self.shape = shape
        self.chassis = pygame.Rect(*self.coords, *self.shape)
        self.speed = 3  # Speed of the tank

        # Init tank cannon which is represented by a line between two points.
        self.angle = np.deg2rad(90)  # Default angle of the cannon
        self.cannon_length = 30
        self.dx = self.cannon_length * np.cos(self.angle)
        self.dy = -self.cannon_length * np.sin(self.angle)
        self.start_pos = [
            self.chassis.left + self.shape[0] // 2, self.chassis.top
        ]
        self.end_pos = [
            self.start_pos[0] + self.dx, self.start_pos[1] + self.dy
        ]

    def get_cannon(self):
        """Return coords of the tip of the cannon and its angle."""
        return self.end_pos, self.angle

    def update(self):
        """Update tank state when pressing keys."""
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT] and self.chassis.left > 0:  # Left translation
            self.chassis.move_ip(-self.speed, 0)
            self.start_pos[0] -= self.speed
            self.end_pos[0] -= self.speed

        if pressed_keys[
                K_RIGHT] and self.chassis.left < WIDTH:  # Right translation
            self.chassis.move_ip(self.speed, 0)
            self.start_pos[0] += self.speed
            self.end_pos[0] += self.speed
        if pressed_keys[K_UP] and (self.angle >= 0 and self.angle <=
                                   np.deg2rad(180)):  # Increasing cannon angle
            self.angle += np.deg2rad(1)
            if self.angle > np.deg2rad(180):
                self.angle = np.deg2rad(180)

        if pressed_keys[K_DOWN] and (
                self.angle >= 0
                and self.angle <= np.deg2rad(180)):  # Decreasing cannon angle
            self.angle -= np.deg2rad(1)
            if self.angle < 0:
                self.angle = 0

        self.dx = self.cannon_length * np.cos(self.angle)
        self.dy = -self.cannon_length * np.sin(self.angle)
        self.end_pos = [
            self.start_pos[0] + self.dx, self.start_pos[1] + self.dy
        ]

    def draw(self, surface):
        """Draw tank on surface."""
        pygame.draw.rect(surface, WHITE, self.chassis)
        pygame.draw.line(surface, WHITE, self.start_pos, self.end_pos, width=5)


def main():
    """Call the main function of the program."""
    screen = pygame.display.set_mode(SIZE)

    player = Tank()
    projectiles_list = []
    # Main loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    coords, angle = player.get_cannon()
                    v0 = [50 * np.cos(angle), 50 * -np.sin(angle)]
                    projectile = Projectile(*coords, v0)
                    projectiles_list.append(projectile)
        player.update()
        # Update display
        screen.fill(BLACK)
        player.draw(screen)
        for p in projectiles_list:
            p.draw(screen)
            p.update()
            if not p.is_onscreen():
                projectiles_list.remove(p)

        pygame.display.flip()
        clock.tick(25)


if __name__ == "__main__":
    main()
