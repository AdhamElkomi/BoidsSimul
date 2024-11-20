import pygame
import random
import math

# Configuration de la simulation
WIDTH, HEIGHT = 800, 800
NUM_BOIDS = 200
MAX_SPEED = 2
MAX_FORCE = 0.03
VIEW_RADIUS = 60
PROP_ALIGN, PROP_SEPARATION = 2 / 3, 1 / 3
ALIGN_RADIUS = PROP_ALIGN * VIEW_RADIUS
SEPARATION_RADIUS = PROP_SEPARATION * VIEW_RADIUS
MAX_ROTATION_SPEED = math.pi / 8
SETTINGS_BAR_HEIGHT = 200
field_of_view_angle = math.pi / 4

paused = False
show_vision = True
LOD_DISTANCE_THRESHOLD = 100  # Distance pour réduire les détails

# Initialisation de Pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation de Boids")
font_petit = pygame.font.Font(None, 30)

class Boid:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT - SETTINGS_BAR_HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED
        self.acceleration = pygame.Vector2(0, 0)
        self.color = (255, 255, 255)

    def apply_behaviors(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)
        self.acceleration += alignment + cohesion + separation

    def is_in_field_of_view(self, other_position):
        direction_to_other = (other_position - self.position).normalize()
        velocity_angle = math.atan2(self.velocity.y, self.velocity.x)
        other_angle = math.atan2(direction_to_other.y, direction_to_other.x)
        angle_difference = abs(velocity_angle - other_angle)
        return angle_difference <= field_of_view_angle

    def align(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other != self:
                distance = self.position.distance_to(other.position)
                if SEPARATION_RADIUS < distance < ALIGN_RADIUS and self.is_in_field_of_view(other.position):
                    steering += other.velocity
                    total += 1
        if total > 0:
            steering /= total
            steering = steering.normalize() * MAX_FORCE  # Normalisation et limitation de la force
            steering *= 1.5  # Facteur multiplicatif pour renforcer l'alignement
        return steering

    def cohere(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other != self:
                distance = self.position.distance_to(other.position)
                if ALIGN_RADIUS < distance < VIEW_RADIUS and self.is_in_field_of_view(other.position):
                    steering += other.position
                    total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            steering = steering.normalize() * MAX_FORCE
        return steering

    def separate(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other != self:
                distance = self.position.distance_to(other.position)
                if distance < SEPARATION_RADIUS and self.is_in_field_of_view(other.position):
                    diff = self.position - other.position
                    diff /= distance
                    steering += diff
                    total += 1
        if total > 0:
            steering /= total
            steering = steering.normalize() * MAX_FORCE
        return steering

    def update(self):
        if paused:
            return
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            self.velocity = self.velocity.normalize() * MAX_SPEED
        self.position += self.velocity
        self.acceleration *= 0
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT - SETTINGS_BAR_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT - SETTINGS_BAR_HEIGHT

    def draw(self, screen):
        angle = math.atan2(self.velocity.y, self.velocity.x)

        if show_vision:
            # Déterminer la complexité des polygones en fonction de la distance
            distance_to_center = self.position.distance_to((WIDTH / 2, HEIGHT / 2))
            num_segments = 10 if distance_to_center > LOD_DISTANCE_THRESHOLD else 30

            # Zones avec opacité réduite (alpha)
            zones = [
                (VIEW_RADIUS, (0, 0, 255, 20)),  # Bleu avec faible opacité
                (ALIGN_RADIUS, (0, 255, 0, 20)),  # Vert avec faible opacité
                (SEPARATION_RADIUS, (255, 0, 0, 20)),  # Rouge avec faible opacité
            ]
            for radius, color in zones:
                points = [self.position]
                start_angle = angle - field_of_view_angle
                end_angle = angle + field_of_view_angle
                for i in range(num_segments + 1):
                    theta = start_angle + (end_angle - start_angle) * i / num_segments
                    x = self.position.x + radius * math.cos(theta)
                    y = self.position.y + radius * math.sin(theta)
                    points.append((x, y))
                # Dessiner le polygone semi-transparent
                pygame.draw.polygon(screen, color, points)

        # Dessin de l'indicateur de direction (triangle)
        arrow_tip = self.position + pygame.Vector2(math.cos(angle), math.sin(angle)) * 8
        arrow_left = self.position + pygame.Vector2(math.cos(angle + 2.5), math.sin(angle + 2.5)) * 5
        arrow_right = self.position + pygame.Vector2(math.cos(angle - 2.5), math.sin(angle - 2.5)) * 5
        pygame.draw.polygon(screen, self.color, [arrow_tip, arrow_left, arrow_right])


boids = [Boid() for _ in range(NUM_BOIDS)]

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    window.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not paused:
        for boid in boids:
            boid.apply_behaviors(boids)
            boid.update()

    for boid in boids:
        boid.draw(window)

    pygame.display.flip()

pygame.quit()
