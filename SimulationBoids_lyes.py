import pygame
import math
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation de Boids avec Prédateur")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Paramètres de simulation
BOID_COUNT = 100
BOID_SPEED = 2
PREDATOR_SPEED = BOID_SPEED * 1.1  # Le prédateur est légèrement plus rapide
WAIT_TIME_AFTER_ATTACK = 600  # Temps d'attente après une attaque (en frames, 10 sec à 60 FPS)
SEPARATION_RADIUS = 20
ALIGNMENT_RADIUS = 50
COHESION_RADIUS = 100
PREDATOR_DETECTION_RADIUS = 120
VISION_ANGLE = math.pi / 4  # 45° pour alignement et cohésion




#####################################################################################




def normalize_vector(vx, vy, target_magnitude):
    magnitude = math.sqrt(vx**2 + vy**2)
    if magnitude == 0:
        return 0, 0
    return (vx / magnitude) * target_magnitude, (vy / magnitude) * target_magnitude

def calculate_angle(dx, dy):
    return math.atan2(dy, dx)

def draw_triangle(screen, color, x, y, angle, size):
    """Dessine un triangle orienté à un angle donné."""
    points = [
        (x + size * math.cos(angle), y + size * math.sin(angle)),
        (x + size * math.cos(angle + 2.5), y + size * math.sin(angle + 2.5)),
        (x + size * math.cos(angle - 2.5), y + size * math.sin(angle - 2.5)),
    ]
    pygame.draw.polygon(screen, color, points)




########################################################################################




class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx, self.vy = normalize_vector(random.uniform(-1, 1), random.uniform(-1, 1), BOID_SPEED)

    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        self.x %= WIDTH
        self.y %= HEIGHT

    def apply_rules(self, boids, predator):
        separation = self.separation(boids)
        alignment = self.alignment(boids)
        cohesion = self.cohesion(boids)
        flee = self.flee(predator)

        # Combiner les comportements avec des pondérations
        self.vx += separation[0] * 1.5 + alignment[0] * 0.8 + cohesion[0] * 0.8 + flee[0] * 2
        self.vy += separation[1] * 1.5 + alignment[1] * 0.8 + cohesion[1] * 0.8 + flee[1] * 2
        self.vx, self.vy = normalize_vector(self.vx, self.vy, BOID_SPEED)

    def separation(self, boids):
        steer_x, steer_y = 0, 0
        for other in boids:
            if other != self and self.distance_to(other) < SEPARATION_RADIUS:
                steer_x -= (other.x - self.x)
                steer_y -= (other.y - self.y)
        return steer_x, steer_y

    def alignment(self, boids):
        avg_vx, avg_vy, count = 0, 0, 0
        for other in boids:
            if other != self and self.is_in_cone(other, ALIGNMENT_RADIUS):
                avg_vx += other.vx
                avg_vy += other.vy
                count += 1
        if count > 0:
            avg_vx /= count
            avg_vy /= count
            return avg_vx - self.vx, avg_vy - self.vy
        return 0, 0

    def cohesion(self, boids):
        center_x, center_y, count = 0, 0, 0
        for other in boids:
            if other != self and self.is_in_cone(other, COHESION_RADIUS):
                center_x += other.x
                center_y += other.y
                count += 1
        if count > 0:
            center_x /= count
            center_y /= count
            return center_x - self.x, center_y - self.y
        return 0, 0

    def flee(self, predator):
        dx, dy = predator.x - self.x, predator.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance < PREDATOR_DETECTION_RADIUS:
            return -dx / distance, -dy / distance
        return 0, 0

    def is_in_cone(self, other, radius):
        dx, dy = other.x - self.x, other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > radius:
            return False
        angle = calculate_angle(dx, dy)
        velocity_angle = calculate_angle(self.vx, self.vy)
        angle_diff = (angle - velocity_angle + math.pi) % (2 * math.pi) - math.pi
        return -VISION_ANGLE <= angle_diff <= VISION_ANGLE

    def distance_to(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def draw(self, screen):
        angle = calculate_angle(self.vx, self.vy)
        draw_triangle(screen, BLUE, self.x, self.y, angle, 5)




#######################################################################################




class Predator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.target = None
        self.wait_time = 0

    def update_position(self, boids):
        if self.wait_time > 0:  # Si le prédateur est en période de repos
            self.wait_time -= 1
            
            # Mouvement circulaire avec un rayon qui varie au fil du temps
            time_factor = self.wait_time / WAIT_TIME_AFTER_ATTACK  # Facteur pour modifier l'évolution du rayon
            radius = 50 + 50 * math.sin(0.1*time_factor * 2 * math.pi)  # Rayon oscillant entre 50 et 100
            
            # Calcul du mouvement circulaire avec réduction de la vitesse à 75%
            angle = time_factor * 2 * math.pi  # Angle en fonction du temps
            self.vx = math.cos(angle) * radius * 0.04 * 0.75  # Réduction de la vitesse à 75%
            self.vy = math.sin(angle) * radius * 0.04 * 0.75  # Réduction de la vitesse à 75%
            
            # Appliquer le mouvement circulaire au prédateur
            self.x += self.vx
            self.y += self.vy
            self.x %= WIDTH
            self.y %= HEIGHT
            return

        if not self.target or self.distance_to(self.target) > PREDATOR_DETECTION_RADIUS:
            self.target = self.find_closest_boid(boids)
            if not self.target:
                # Mouvement circulaire en l'absence de cible
                angle_variation = random.uniform(-0.05, 0.05)
                self.vx += math.cos(angle_variation) * 0.1
                self.vy += math.sin(angle_variation) * 0.1
                self.vx, self.vy = normalize_vector(self.vx, self.vy, PREDATOR_SPEED)
        else:
            # Poursuite de la cible
            dx, dy = self.target.x - self.x, self.target.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                self.vx, self.vy = normalize_vector(dx, dy, PREDATOR_SPEED)

        self.x += self.vx
        self.y += self.vy
        self.x %= WIDTH
        self.y %= HEIGHT

    def find_closest_boid(self, boids):
        visible_boids = [boid for boid in boids if self.is_in_cone(boid, PREDATOR_DETECTION_RADIUS)]
        if visible_boids:
            return min(visible_boids, key=lambda b: self.distance_to(b))
        return None

    def eliminate_boids(self, boids):
        if self.target and self.distance_to(self.target) < 10:
            self.wait_time = WAIT_TIME_AFTER_ATTACK
            boids.remove(self.target)
            self.target = None
        return boids

    def is_in_cone(self, boid, radius):
        dx, dy = boid.x - self.x, boid.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > radius:
            return False
        angle = calculate_angle(dx, dy)
        velocity_angle = calculate_angle(self.vx, self.vy)
        angle_diff = (angle - velocity_angle + math.pi) % (2 * math.pi) - math.pi
        return -VISION_ANGLE <= angle_diff <= VISION_ANGLE

    def distance_to(self, boid):
        return math.sqrt((boid.x - self.x) ** 2 + (boid.y - self.y) ** 2)

    def draw(self, screen):
        angle = calculate_angle(self.vx, self.vy)
        draw_triangle(screen, RED, self.x, self.y, angle, 10)





############################################################################################




boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(BOID_COUNT)]
predator = Predator(WIDTH // 2, HEIGHT // 2)



# Boucle principale
running = True
clock = pygame.time.Clock()

while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quitter l'application
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:  # Ajouter un boid
                boids.append(Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  # Supprimer un boid
                if boids:  # Vérifie s'il y a des boids à supprimer
                    boids.pop()

    # Mise à jour des boids
    for boid in boids:
        boid.apply_rules(boids, predator)
        boid.update_position()

    # Mise à jour du prédateur
    predator.update_position(boids)
    boids = predator.eliminate_boids(boids)

    # Dessin des boids et du prédateur
    screen.fill(BLACK)  # Efface l'écran
    for boid in boids:
        boid.draw(screen)
    predator.draw(screen)

    # Rafraîchissement de l'écran
    pygame.display.flip()
    clock.tick(60)  # Limite à 60 FPS

pygame.quit()
