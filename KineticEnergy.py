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
updates_per_frame = 20 # Esegui due aggiornamenti per ogni frame


class Body:

    def __init__(self, x, y, mass, radius, color, vx=0, vy=0):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.vx = vx  # Initial velocity x
        self.vy = vy  # Initial velocity y
        self.vxn = vx  # Next velocity x
        self.vyn = vx  # Next velocity y

    def draw(self, win):
        # Ensure coordinates are within the window boundaries
        if 0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT:
            center = (int(self.x), int(self.y))
            pygame.draw.circle(win, self.color, center, self.radius)
        else:
            print(f"Body out of bounds: x={self.x}, y={self.y}")

    def urto_elastico(self, other):
        m1 = self.mass
        m2 = other.mass
        v1x = self.vx
        v1y = self.vy
        v2x = other.vx
        v2y = other.vy

        v1fx = ((m1 - m2) * v1x + 2 * m2 * v2x) / (m1 + m2)
        v1fy = ((m1 - m2) * v1y + 2 * m2 * v2y) / (m1 + m2)
    
        return v1fx, v1fy

    def update_position(self, dt):
        self.vx = self.vxn
        self.vy = self.vyn

        self.x += self.vx * dt
        self.y += self.vy * dt
        
        self.x = self.x % WIDTH
        self.y = self.y % HEIGHT


    def chek_collision(self, other):

        self.vxn = self.vx
        self.vyn = self.vy
        
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < (self.radius + other.radius):  # Collision
            self.vxn, self.vyn = self.urto_elastico(other)

    
    def distance(self, other):
        return math.sqrt( (self.x-other.x)**2 + (self.y-other.y)**2 )
        

    def __str__(self):
        return f"Body at ({self.x}, {self.y}) with mass {self.mass}, radius {self.radius}, color {self.color}, velocity ({self.vx}, {self.vy})"




def main():
    run = True
    clock = pygame.time.Clock()

    # Creating celestial bodies
    bodies = [

        Body(WIDTH/2-86, HEIGHT/2+60, 2, 13, WHITE, 1, -8),
        Body(WIDTH/2-20, HEIGHT/2+150, 7, 15, WHITE, -2, 9),
        Body(WIDTH/2, HEIGHT/2+30, 6, 10, WHITE, 3, 18),
        Body(WIDTH/2+30, HEIGHT/2-40, 5, 5, WHITE, 4, -4),
        Body(WIDTH/2-37, HEIGHT/2-100, 12, 17, WHITE, 5, -6),
        Body(WIDTH/2+60, HEIGHT/2+40, 10, 20, WHITE, -6, 7)
    ]
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for _ in range(updates_per_frame):
            for body in bodies:
                for other in bodies:
                    if body != other:
                        body.chek_collision(other)

            for body in bodies:
                body.update_position(1 / FPS)

        WIN.fill(BLACK)
        for body in bodies:
            body.draw(WIN)

        #pygame.draw.line(WIN,WHITE, (bodies[0].x, bodies[0].y), (bodies[1].x, bodies[1].y))
        #print(bodies[0].distance(bodies[1]))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
