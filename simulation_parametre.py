import pygame
import math
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1024 , 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation de Boids avec Prédateur")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (148, 0, 211)

# Paramètres de simulation
BOID_COUNT = 500
BOID_SPEED = 4
PREDATOR_SPEED = BOID_SPEED * 1.1
WAIT_TIME_AFTER_ATTACK = 300
SEPARATION_RADIUS = 20
ALIGNMENT_RADIUS = 150
COHESION_RADIUS = 300
PREDATOR_DETECTION_RADIUS = 150
VISION_ANGLE = math.pi / 4
CELL_SIZE = 100
FRAME_RATE = 30
COHESION_ALIGNMENT_UPDATE_INTERVAL = 10 # Fréquence de mise à jour


###################################################


def normalize_vector(vx, vy, target_magnitude):
    magnitude = math.sqrt(vx**2 + vy**2)
    if magnitude == 0:
        return 0, 0
    return (vx / magnitude) * target_magnitude, (vy / magnitude) * target_magnitude

def calculate_angle(dx, dy):
    return math.atan2(dy, dx)

def draw_triangle(screen, color, x, y, angle, size):
    points = [
        (x + size * math.cos(angle), y + size * math.sin(angle)),
        (x + size * math.cos(angle + 2.5), y + size * math.sin(angle + 2.5)),
        (x + size * math.cos(angle - 2.5), y + size * math.sin(angle - 2.5)),
    ]
    pygame.draw.polygon(screen, color, points)


#####################################################

def assign_to_grid(boids):
    grid = {}
    for boid in boids:
        cell_x = int(boid.x // CELL_SIZE)
        cell_y = int(boid.y // CELL_SIZE)
        cell = (cell_x, cell_y)
        if cell not in grid:
            grid[cell] = []
        grid[cell].append(boid)
    return grid

def get_nearby_boids(boid, grid):
    cell_x = int(boid.x // CELL_SIZE)
    cell_y = int(boid.y // CELL_SIZE)
    nearby_boids = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            cell = (cell_x + dx, cell_y + dy)
            if cell in grid:
                nearby_boids.extend(grid[cell])
    return nearby_boids


#########################################################


class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx, self.vy = normalize_vector(random.uniform(-1, 1), random.uniform(-1, 1), BOID_SPEED)
        self.update_frame = random.randint(0, COHESION_ALIGNMENT_UPDATE_INTERVAL)  # Décalage initial aléatoire

        # Ces vecteurs sont stockés pour éviter de recalculer la cohésion/alignement trop souvent
        self.last_cohesion = (0, 0)
        self.last_alignment = (0, 0)

    def update_position(self):
        """Met à jour la position du boid avec gestion des bords de l'écran."""
        self.x += self.vx
        self.y += self.vy
        self.x %= WIDTH
        self.y %= HEIGHT

    def apply_rules(self, boids, predator, grid, current_frame):
        """Applique les règles de séparation, alignement, cohésion et fuite."""

        # Toujours recalculer la séparation et la fuite
        separation = self.separation(grid)
        flee = self.flee(predator,BOID_SPEED)

        # Cohésion et alignement sont recalculés selon l'intervalle
        if current_frame % COHESION_ALIGNMENT_UPDATE_INTERVAL == self.update_frame:
            self.last_cohesion = self.cohesion(grid)
            self.last_alignment = self.alignment(grid)

        # Combinaison des comportements avec des pondérations
        self.vx += (
            separation[0] * 2 +
            self.last_alignment[0] * 8 +
            self.last_cohesion[0] * 1 +
            flee[0] * 16
        )
        self.vy += (
            separation[1] * 2 +
            self.last_alignment[1] * 8 +
            self.last_cohesion[1] * 1 +
            flee[1] * 16
        )

        # Normalisation de la vitesse
        self.vx, self.vy = normalize_vector(self.vx, self.vy, BOID_SPEED)

    def separation(self, grid):
        """Évite les collisions avec les boids proches."""
        steer_x, steer_y = 0, 0
        nearby_boids = get_nearby_boids(self, grid)
        for other in nearby_boids:
            if other != self and self.distance_to(other) < SEPARATION_RADIUS:
                steer_x -= (other.x - self.x)
                steer_y -= (other.y - self.y)
        return steer_x, steer_y

    def alignment(self, grid):
        """Aligne la vitesse avec les boids proches."""
        avg_vx, avg_vy, count = 0, 0, 0
        nearby_boids = get_nearby_boids(self, grid)
        for other in nearby_boids:
            if other != self and self.is_in_cone(other, ALIGNMENT_RADIUS):
                avg_vx += other.vx
                avg_vy += other.vy
                count += 1
        if count > 0:
            avg_vx /= count
            avg_vy /= count
            return avg_vx - self.vx, avg_vy - self.vy
        return 0, 0

    def cohesion(self, grid):
        """Se rapproche du centre de masse des boids proches."""
        center_x, center_y, count = 0, 0, 0
        nearby_boids = get_nearby_boids(self, grid)
        for other in nearby_boids:
            if other != self and self.is_in_cone(other, COHESION_RADIUS):
                center_x += other.x
                center_y += other.y
                count += 1
        if count > 0:
            center_x /= count
            center_y /= count
            return center_x - self.x, center_y - self.y
        return 0, 0

    def flee(self, predator, BOID_SPEED):
        """Fuit le prédateur s'il est détecté."""
        dx, dy = predator.x - self.x, predator.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance < PREDATOR_DETECTION_RADIUS:
            return -dx * BOID_SPEED / distance, -dy * BOID_SPEED / distance
        return 0, 0

    def is_in_cone(self, other, radius):
        """Vérifie si un autre boid est dans le champ de vision."""
        dx, dy = other.x - self.x, other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > radius:
            return False
        angle = calculate_angle(dx, dy)
        velocity_angle = calculate_angle(self.vx, self.vy)
        angle_diff = (angle - velocity_angle + math.pi) % (2 * math.pi) - math.pi
        return -VISION_ANGLE <= angle_diff <= VISION_ANGLE

    def distance_to(self, other):
        """Calcule la distance entre deux boids."""
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def draw(self, screen):
        """Dessine le boid sur l'écran."""
        angle = calculate_angle(self.vx, self.vy)
        draw_triangle(screen, BLUE, self.x, self.y, angle, 5)



##########################################################


class Predator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.target = None
        self.wait_time = 0

    def update_position(self, boids):
        """Met à jour la position du prédateur."""
        if self.wait_time > 0:  # Période de repos
            self.wait_time -= 1
            angle = (self.wait_time / WAIT_TIME_AFTER_ATTACK) * 2 * math.pi
            self.vx = math.cos(angle) * PREDATOR_SPEED * 0.81  # 0.75
            self.vy = math.sin(angle) * PREDATOR_SPEED * 0.81   # 0.75
            self.x += self.vx
            self.y += self.vy
            self.x %= WIDTH
            self.y %= HEIGHT
            return

        if not self.target or self.distance_to(self.target) > PREDATOR_DETECTION_RADIUS:
            self.target = self.find_closest_boid(boids)
        else:
            dx, dy = self.target.x - self.x, self.target.y - self.y
            self.vx, self.vy = normalize_vector(dx, dy, PREDATOR_SPEED)

        self.x += self.vx
        self.y += self.vy
        self.x %= WIDTH
        self.y %= HEIGHT

    def find_closest_boid(self, boids):
        """Trouve le boid le plus proche."""
        visible_boids = [boid for boid in boids if self.is_in_cone(boid, PREDATOR_DETECTION_RADIUS)]
        if visible_boids:
            return min(visible_boids, key=lambda b: self.distance_to(b))
        return None

    def eliminate_boids(self, boids):
        """Élimine les boids à proximité immédiate."""
        if self.target and self.distance_to(self.target) < 10:
            self.wait_time = WAIT_TIME_AFTER_ATTACK
            boids.remove(self.target)
            self.target = None
        return boids

    def is_in_cone(self, boid, radius):
        """Vérifie si un boid est dans le champ de vision."""
        dx, dy = boid.x - self.x, boid.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > radius:
            return False
        angle = calculate_angle(dx, dy)
        velocity_angle = calculate_angle(self.vx, self.vy)
        angle_diff = (angle - velocity_angle + math.pi) % (2 * math.pi) - math.pi
        return -VISION_ANGLE <= angle_diff <= VISION_ANGLE

    def distance_to(self, boid):
        """Calcule la distance au boid."""
        return math.sqrt((boid.x - self.x) ** 2 + (boid.y - self.y) ** 2)

    def draw(self, screen):
        """Dessine le prédateur sur l'écran."""
        angle = calculate_angle(self.vx, self.vy)
        draw_triangle(screen, RED, self.x, self.y, angle, 10)


##########################################################


# Initialisation des boids et du prédateur
boids = [Boid(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)) for _ in range(BOID_COUNT)]
predator = Predator(WIDTH // 2, HEIGHT // 2)


# Boucle principale
running = True
clock = pygame.time.Clock()

current_frame = 0  # Compteur global des frames

while running:
    
    current_frame += 1  # Incrémente le compteur de frames
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP :
                boids.append(Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
            elif event.key == pygame.K_DOWN and boids :
                boids.pop()

    grid = assign_to_grid(boids)
    for boid in boids:
        boid.apply_rules(boids, predator, grid, current_frame)
        boid.update_position()

    predator.update_position(boids)
    boids = predator.eliminate_boids(boids)

    screen.fill(BLACK)
    for boid in boids:
        boid.draw(screen)
    predator.draw(screen)
    pygame.display.flip()

 # Limite le nombre de frames par second
    clock.tick(FRAME_RATE)
