import pygame
import math

# Initializing Pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Frame rate
FPS = 120
updates_per_frame = 20 # Esegui due aggiornamenti per ogni frame


class Ship:

    def __init__(self, x, y, mass, power, color, direction = 0, vx=0, vy=0):
        self.x = x
        self.y = y
        self.mass = mass
        self.power = power
        self.color = color
        self.direction = direction
        self.vx = vx  # Initial velocity x
        self.vy = vy  # Initial velocity y

    def draw(self, win):
        # Ensure coordinates are within the window boundaries
        if 0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT:
            center = (int(self.x), int(self.y))
            
            radius = 10
            ship = [
                (int(self.x + radius * math.cos(self.direction)), int(self.y + radius * math.sin(self.direction))),
                (int(self.x + radius * math.cos(self.direction + 2/3*math.pi)), int(self.y + radius * math.sin(self.direction + 2/3*math.pi))),
                (int(self.x + radius * math.cos(self.direction + 2*2/3*math.pi)), int(self.y + radius * math.sin(self.direction + 2*2/3*math.pi))),
                (int(self.x + radius * math.cos(self.direction)), int(self.y + radius * math.sin(self.direction))),
                (int(self.x + 2 * radius * math.cos(self.direction)), int(self.y + 2 * radius * math.sin(self.direction)))
            ]

            pygame.draw.lines(win, WHITE, False, ship)

        else:
            print(f"Body out of bounds: x={self.x}, y={self.y}")



    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        self.x = self.x % WIDTH
        self.y = self.y % HEIGHT
    
    def acceleration(self, dt):
        acc = self.power/self.mass
        ax = acc * math.cos(self.direction)
        ay = acc * math.sin(self.direction)
        self.vx += ax*dt
        self.vy += ay*dt
    
    def shoot(self):
        return Proiettile(self.x, self.y, self.direction, 300)

    
    def distance(self, other):
        return math.sqrt( (self.x-other.x)**2 + (self.y-other.y)**2 )
        

    def __str__(self):
        return f"Body at ({self.x:.3f}, {self.y:.3f}) with mass {self.mass:.3f}, direction {self.direction:.3f}, color {self.color}, velocity ({self.vx:.3f}, {self.vy:.3f})"


class Proiettile():

    def __init__(self, x, y, direction, velocity) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.vx = velocity * math.cos(direction)
        self.vy = velocity * math.sin(direction)

    def update_position(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        self.x = self.x % WIDTH
        self.y = self.y % HEIGHT
    
    def draw(self, win):
        # Ensure coordinates are within the window boundaries
        if 0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT:

            pygame.draw.line(win, WHITE, (int(self.x), int(self.y)), (int(self.x + self.vx/10), int(self.y + self.vy/10)))

        else:
            print(f"Body out of bounds: x={self.x}, y={self.y}")



def main():
    clear = 1
    run = True
    clock = pygame.time.Clock()

    # Creating celestial bodies
    bullets = []

    ships = Ship(WIDTH/2, HEIGHT/2, 10, 10000, WHITE, 0, 0, 0)
    
    while run:
        clock.tick(FPS)

        x, y = pygame.mouse.get_pos()

        ships.direction = math.atan2(y-ships.y, x-ships.x)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            """if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                bullets.append(ships.shoot())"""
            
        if pygame.mouse.get_pressed()[2]:
                bullets.append(ships.shoot())
        
        
        if pygame.mouse.get_pressed()[0]:
                ships.acceleration(1 / FPS)

        if pygame.mouse.get_pressed()[1]:
                clear = not clear
        
        if clear:
            WIN.fill(BLACK)

        ships.update_position(1 / FPS)
        #WIN.fill(BLACK)
        ships.draw(WIN)
        if bullets:
            for bullet in bullets:
                bullet.update_position(1 / FPS)
                bullet.draw(WIN)

        print(ships)


        #pygame.draw.line(WIN,WHITE, (bodies[0].x, bodies[0].y), (bodies[1].x, bodies[1].y))
        #print(bodies[0].distance(bodies[1]))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
