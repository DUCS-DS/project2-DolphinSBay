import random, math, pygame

def radians(degrees):
    """Convert degrees to radians."""
    return math.pi / 180 * degrees

def blue(scale=0.8):
    """Return the RGB of a shade of blue."""
    assert 0 <= scale <= 1, f"Scale must be between 0 and 1 inclusive, not {scale}"
    num = int(scale * 255)
    return (num // 2, 2 * num // 3, num)

class Node:
    def __init__(self, x, y, speed, angle):
        """Create a node."""
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.dx = math.sin(self.angle) * self.speed
        self.dy = math.cos(self.angle) * self.speed

    def move(self):
        """Move the node."""
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        """Draw the node to the screen."""
        pygame.draw.circle(screen, blue(), (int(self.x), int(self.y)), node_radius)

    def reflect(self):
        """Reflect off the screen boundaries."""
        if self.x > winwidth - node_radius or self.x < node_radius:
            self.dx = -self.dx
            self.x = max(node_radius, min(self.x, winwidth - node_radius))
        if self.y > winheight - node_radius or self.y < node_radius:
            self.dy = -self.dy
            self.y = max(node_radius, min(self.y, winheight - node_radius))

winwidth, winheight = 800, 600
background = (5, 5, 5)
num_nodes = 400
node_radius = 0
thresh = 1800

screen = pygame.display.set_mode((winwidth, winheight))
clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Optimized Gen Art")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

nodes = [Node(random.randint(0, winwidth), random.randint(0, winheight),
              random.uniform(0.25, 0.33), radians(random.randint(0, 359)))
         for _ in range(num_nodes)]

quit = False
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            quit = True

    screen.fill(background)
    
    for node in nodes:
        node.move()
        node.reflect()
        node.draw(screen)
    
    nodes.sort(key=lambda n: n.x)  # Sort nodes by x-coordinate
    
    for i, node1 in enumerate(nodes):
        x1, y1 = node1.x, node1.y
        for j in range(i + 1, min(i + 20, len(nodes))):  # Only check nearby nodes
            node2 = nodes[j]
            x2, y2 = node2.x, node2.y
            d_squared = (x1 - x2) ** 2 + (y1 - y2) ** 2
            if d_squared < thresh:
                pygame.draw.aaline(screen, blue((thresh - d_squared) / thresh), (x1, y1), (x2, y2))
    
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
