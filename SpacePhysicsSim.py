import pygame
import math

# Initializing Pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Frame rate
FPS = 120
updates_per_frame = 600 # Esegui due aggiornamenti per ogni frame

class Body:
    G = 6.67430e-11  # Gravitational constant

    def __init__(self, x, y, mass, radius, color, vx=0, vy=0):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.vx = vx  # Initial velocity x
        self.vy = vy  # Initial velocity y
        self.ax = 0  # Initial acceleration x
        self.ay = 0  # Initial acceleration y
    
    @classmethod
    def from_initial_velocity(cls, x, y, mass, radius, color, initial_vx, initial_vy):
        return cls(x, y, mass, radius, color, initial_vx, initial_vy)
    
    @classmethod
    def stationary_body(cls, x, y, mass, radius, color):
        return cls(x, y, mass, radius, color, 0, 0)

    def draw(self, win):
        # Ensure coordinates are within the window boundaries
        if 0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT:
            center = (int(self.x), int(self.y))
            pygame.draw.circle(win, self.color, center, self.radius)
        else:
            print(f"Body out of bounds: x={self.x}, y={self.y}")

    def update_position(self, dt):
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        if self.x < 0 or self.x > WIDTH:
            self.vx = 0
            self.x = max(min(self.x, WIDTH), 0)
        if self.y < 0 or self.y > HEIGHT:
            self.vy = 0
            self.y = max(min(self.y, HEIGHT), 0)

    def apply_gravity(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > (self.radius + other.radius):  # Avoid collision
            force = self.G * self.mass * other.mass / distance**2
            angle = math.atan2(dy, dx)
        else:
            force = 200 ** ((self.radius + other.radius) - distance)
            angle = math.atan2(-dy, -dx)

        fx = math.cos(angle) * force
        fy = math.sin(angle) * force
        self.ax += fx / self.mass
        self.ay += fy / self.mass

    
    def distance(self, other):
        return math.sqrt( (self.x-other.x)**2 + (self.y-other.y)**2 )
        

    def __str__(self):
        return f"Body at ({self.x}, {self.y}) with mass {self.mass}, radius {self.radius}, color {self.color}, velocity ({self.vx}, {self.vy})"


def main():
    run = True
    clock = pygame.time.Clock()

    # Creating celestial bodies
    bodies = [

        Body.from_initial_velocity(WIDTH/2 + 100, HEIGHT/2, -10**11, 10, WHITE, 0, 0.1),
        Body.from_initial_velocity(WIDTH/2 - 100, HEIGHT/2, 10**11, 10, WHITE, 0, -0.1),
        Body.from_initial_velocity(WIDTH/2, HEIGHT/2+100, -10**11, 10, WHITE, -0.1, 0),
        Body.from_initial_velocity(WIDTH/2, HEIGHT/2-100, 10**11, 10, WHITE, +0.1, 0),
        Body.stationary_body(WIDTH/2, HEIGHT/2, 10**10, 10, WHITE),  # Moon

        # Body.stationary_body(WIDTH/2 - 50, HEIGHT/2, 1000000000000000, 20, WHITE),  # Earth
        # Body.stationary_body(WIDTH/2 + 50, HEIGHT/2, 10000000000, 10, WHITE),  # Moon
        # Body.from_initial_velocity(WIDTH/2 + 25, HEIGHT/2, 10000000000, 10, WHITE, 0, 30)
    ]
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for _ in range(updates_per_frame):
            for body in bodies:
                body.ax = body.ay = 0  # Reset accelerations before applying gravity
                for other in bodies:
                    if body != other:
                        body.apply_gravity(other)

            for body in bodies:
                body.update_position(1 / FPS)

        WIN.fill(BLACK)
        for body in bodies:
            body.draw(WIN)

        pygame.draw.line(WIN,WHITE, (bodies[0].x, bodies[0].y), (bodies[1].x, bodies[1].y))
        print(bodies[0].distance(bodies[1]))
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
