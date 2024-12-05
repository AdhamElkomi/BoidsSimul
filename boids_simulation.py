import pygame
import random
import math

import os #Debug pour image


# Initialisation de Pygame
pygame.init()

# Configuration de la simulation
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h # Dimension de la fenêtre
NUM_BOIDS = 20 
MAX_SPEED = 2 # Vitesse maximale des boids.
VITESSE_INITIAL = 0.6
MAX_FORCE = 0.03 # Force maximale appliquée pour ajuster leur direction.
VIEW_RADIUS = 130
VIEW_RADIUS_MIN = 20
VIEW_RADIUS_MAX = 150
PROP_ALIGN, PROP_SEPARATION = 2/3, 1/3 # les rayons sont proportionnels au debut
ALIGN_RADIUS = PROP_ALIGN * VIEW_RADIUS  # rayon du alignement
SEPARATION_RADIUS = PROP_SEPARATION * VIEW_RADIUS  # rayon du distanciation
MAX_ROTATION_SPEED = math.pi / 8  # Vitesse de rotation maximale (radians par tick)

ALIGN_RADIUS_MIN = 20
ALIGN_RADIUS_MAX = VIEW_RADIUS_MAX
SEPARATION_RADIUS_MIN = 10
SEPARATION_RADIUS_MAX = ALIGN_RADIUS_MAX

ALIGN_FORCE_SCALE = 4.0  # Force d'alignement paramétrable
AVOID_FORCE_SCALE = 5.0  # Poids à l'évitement des obstacles

paused = False
show_vision = False
field_of_view_angle = math.pi / 4  # Angle initial du champ de vision (45°)

# Hauteur de la barre de manipulation
SETTINGS_BAR_HEIGHT = 200
settings_area_center = (0, HEIGHT - SETTINGS_BAR_HEIGHT - 200, WIDTH, SETTINGS_BAR_HEIGHT + 200)

# Centres et zones
screen_center = (WIDTH, HEIGHT)
game_area_center = (0, 0, WIDTH, HEIGHT - SETTINGS_BAR_HEIGHT)
settings_area_center = (0, HEIGHT - SETTINGS_BAR_HEIGHT, WIDTH, SETTINGS_BAR_HEIGHT)
label_numboids_center = (WIDTH - 155, HEIGHT - 50)
circle_plus_center = (WIDTH - 50, HEIGHT - 100)
circle_minus_center = (WIDTH - 125, HEIGHT - 100)
slider_x = 200
slider_y = HEIGHT - 200 + 10  # Slider pour l'angle
slider_width = 300
slider_height = 10
separation_slider_y = slider_y + 50  # Slider pour la séparation
align_slider_y = separation_slider_y + 50  # Slider pour l'alignement
cohesion_slider_y = align_slider_y + 50  # Slider pour la cohésion

angle_display_center = (slider_x + slider_width + 60, slider_y + slider_height // 2)
radius_display_center = (slider_x + slider_width + 50, separation_slider_y + slider_height // 2)

button_clear_center = (WIDTH - 700, HEIGHT - 140, 80, 40)
button_clear = pygame.Rect(button_clear_center[0] - 40, button_clear_center[1] - 20, 80, 40)
button_pause_center = (WIDTH - 700, HEIGHT - 90)
button_pause = pygame.Rect(button_pause_center[0] - 40, button_pause_center[1] - 20, 80, 40)
button_vision_center = (WIDTH - 700, HEIGHT - 40)
button_vision = pygame.Rect(button_vision_center[0] - 40, button_vision_center[1] - 20, 80, 40)

# Screen
window = pygame.display.set_mode(screen_center, pygame.FULLSCREEN)
pygame.display.set_caption("Simulation de Boids")

# Zones
game_area = pygame.Rect(game_area_center)
settings_area = pygame.Rect(settings_area_center)

# Fonts
font = pygame.font.Font(None, 36)
font_grand = pygame.font.Font(None, 75)
font_petit = pygame.font.Font(None, 30)

# Textes
text1 = font_grand.render("+", True, (255, 255, 255))
text2 = font_grand.render("-", True, (255, 255, 255))
text3 = font_petit.render("Clear", True, (255, 255, 255))
text_rect_p = text1.get_rect(center=(WIDTH - 50, HEIGHT - 103))
text_rect_m = text2.get_rect(center=circle_minus_center)
text_rect_clear = text3.get_rect(center=(WIDTH - 700, HEIGHT - 140))

# Avertissement bombe
show_warning = False
warning_timer = 0  # Pour gérer le clignotement
warning_image_path = os.path.join(os.path.dirname(__file__), "imageBoids", "warning.jpg")
if not os.path.exists(warning_image_path):
    raise FileNotFoundError(f"L'image d'avertissement est introuvable au chemin {warning_image_path}")
warning_image = pygame.image.load(warning_image_path)
warning_image = pygame.transform.scale(warning_image, (100, 100))  # Ajustez la taille si nécessaire
warning_blink_timer = 0

bomb_size = 50
image_path = os.path.join(os.path.dirname(__file__), "imageBoids", "bomb.png")
if not os.path.exists(image_path):
        raise FileNotFoundError(f"Le fichier bomb.png est introuvable au chemin {image_path}")
bomb_image = pygame.image.load(image_path)
bomb_image = pygame.transform.scale(bomb_image, (bomb_size, bomb_size))  # Global
bomb_image = pygame.transform.rotate(bomb_image, -90)  # Tourner l'image de 90 degrés vers la droite


class Bomb:
    def __init__(self, position):
        self.image = bomb_image
        # Redimensionnez l'image et définissez le rayon de la bombe
        self.radius = bomb_size/2  # Définit le rayon (la moitié de la largeur/redimensionnement)
        
        self.position = position.copy()
        self.velocity = pygame.Vector2(0, random.uniform(2, 5))  # La bombe tombe verticalement
        self.alpha = 255  # Opacité initiale
        self.blink_timer = 0  # Pour gérer le clignotement
        self.fixed = False  # Indique si la bombe est fixée

        # Animation de rotation
        self.current_angle = 0  # Angle actuel
        self.target_angle = 90  # Rotation à atteindre
        self.rotation_speed = 5  # Vitesse de rotation par tick (ajustez si nécessaire)
        self.rotation_complete = False  # Indique si la rotation est terminée

        # Explosion
        self.exploding = False  # Indique si la bombe est en phase d'explosion
        self.explosion_radius = 0  # Rayon d'explosion croissant
        self.explosion_max_radius = 150  # Rayon maximum de l'explosion
        self.explosion_color = (255, 69, 0)  # Couleur initiale de l'explosion (rouge-orangé)

        self.lifespan = 200  # Durée de vie de la bombe (en ticks)

    def update(self):
        # Rotation incrémentale
        if not self.rotation_complete:
            self.current_angle += self.rotation_speed
            if self.current_angle >= self.target_angle:
                self.current_angle = self.target_angle
                self.rotation_complete = True

        # Descente ou fixation
        if not self.fixed:
            self.velocity.y = max(self.velocity.y - 0.1, 0)  # Réduit la vitesse jusqu'à 0
            self.position += self.velocity
            if self.velocity.y == 0:
                self.fixed = True
        elif not self.exploding:
            # Clignotement après fixation
            self.blink_timer += 1
            if self.blink_timer % 20 < 10:
                self.alpha = 255
            else:
                self.alpha = 50
            # Déclencher l'explosion après le clignotement
            if self.blink_timer > 100:  # Temps avant explosion
                self.exploding = True

        # Explosion
        if self.exploding:
            self.explosion_radius += 5  # Augmenter progressivement le rayon
            if self.explosion_radius >= self.explosion_max_radius:
                self.lifespan = 0  # Détruire la bombe après l'explosion

        # Réduire la durée de vie pour les bombes non fixées
        if not self.exploding:
            self.lifespan -= 1

    def draw(self, screen):
        if not self.exploding:
            # Afficher la bombe avec rotation
            rotated_image = pygame.transform.rotate(self.image, self.current_angle)
            rotated_rect = rotated_image.get_rect(center=(self.position.x, self.position.y))

            temp_surface = rotated_image.copy()
            temp_surface.set_alpha(self.alpha)
            screen.blit(temp_surface, rotated_rect.topleft)
        else:
            # Dessiner l'explosion
            pygame.draw.circle(
                screen,
                self.explosion_color,
                (int(self.position.x), int(self.position.y)),
                self.explosion_radius,
                width=5  # Bordure pour un effet de choc
            )

            # Dégradé de couleur
            fade_factor = max(0, (self.explosion_max_radius - self.explosion_radius) / self.explosion_max_radius)
            self.explosion_color = (
                int(255 * fade_factor),  # Rouge diminue
                int(165 * fade_factor),  # Orange diminue
                int(0 * fade_factor)    # Jaune diminue
            )

    def is_active(self):
        return self.lifespan > 0

class Plane:
    def __init__(self):
        self.position = pygame.Vector2(WIDTH // 2, HEIGHT // 2)  # Position initiale
        self.velocity = pygame.Vector2(random.choice([-1, 1]) * 2, random.uniform(-0.5, 0.5))  # Mouvement

        # Charger l'image avec un chemin dynamique AVEC DEBUG
        image_path = os.path.join(os.path.dirname(__file__), "imageBoids", "plane.png")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Le fichier plane.png est introuvable au chemin {image_path}")
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.image = pygame.transform.rotate(self.image, -90)  # Tourner l'image de 90 degrés vers la droite
        self.size = 50

    def update(self):
        self.position += self.velocity

        # Gérer les bords pour que l'avion réapparaisse de l'autre côté
        if self.position.x > WIDTH:
            self.position.x = -self.image.get_width()
        elif self.position.x < -self.image.get_width():
            self.position.x = WIDTH
        if self.position.y > HEIGHT - SETTINGS_BAR_HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT - SETTINGS_BAR_HEIGHT

    def draw(self, screen):
        # Calcul de l'angle basé sur la direction de la vitesse
        angle = math.degrees(math.atan2(self.velocity.y, self.velocity.x))
        
        # Applique la rotation de l'image
        rotated_image = pygame.transform.rotate(self.image, -angle)
        rotated_rect = rotated_image.get_rect(center=(self.position.x, self.position.y))
        
        # Dessine l'image tournée
        screen.blit(rotated_image, rotated_rect.topleft)

    
    def drop_bomb(self):
        bombs.append(Bomb(self.position))


class Boid:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT - SETTINGS_BAR_HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED
        self.acceleration = pygame.Vector2(0, 0)
        self.color = (255, 255, 255)  # Couleur par défaut : blanche

    def apply_behaviors(self, boids, plane, bombs):
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)
        avoid_plane = self.avoid_plane(plane)
        # Ajustement pondéré des forces pour garder le groupe
        self.acceleration += ( 
            0.6 * alignment +
            0.5 * cohesion +
            0.8 * separation +
            1.0 * avoid_plane 
        )

        for bomb in bombs:
            distance = self.position.distance_to(bomb.position)
            if distance < bomb.radius:  # Si le boid touche une bombe
                self.position = pygame.Vector2(
                    random.uniform(0, WIDTH),
                    random.uniform(0, HEIGHT - SETTINGS_BAR_HEIGHT)
                )
                break  # Évitez plusieurs téléportations en un seul tick

        # Déterminer la couleur en fonction des interactions
        if separation.length() > 0:
            self.color = (148, 0, 211)  #  : séparation
        elif alignment.length() > 0:
            self.color = (255, 20, 147)  #  : alignement
        elif cohesion.length() > 0:
            self.color = (255, 182, 150)  #  : cohésion
        else:
            self.color = (255, 255, 255)  # Blanc : aucune interaction

    def is_in_field_of_view(self, other_position):
        # Vérifie si un boid est dans le champ de vision
        direction_to_other = (other_position - self.position).normalize()
        velocity_angle = math.atan2(self.velocity.y, self.velocity.x)
        other_angle = math.atan2(direction_to_other.y, direction_to_other.x)
        angle_difference = abs(velocity_angle - other_angle)
        return angle_difference <= field_of_view_angle

    def align(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        center_of_mass = pygame.Vector2(0, 0)

        for other in boids:
            if other != self:
                distance = self.position.distance_to(other.position)
                if SEPARATION_RADIUS < distance < ALIGN_RADIUS and self.is_in_field_of_view(other.position):
                    center_of_mass += other.position
                    steering += other.velocity
                    total += 1
        if total > 0:
            center_of_mass /= total
            center_diff = center_of_mass - self.position
            steering /= total
            steering = steering.normalize() * MAX_FORCE * ALIGN_FORCE_SCALE
            return steering + 0.3 * center_diff.normalize() * MAX_FORCE
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

        # Calculez la nouvelle direction avec accélération
        new_velocity = self.velocity + self.acceleration
        if new_velocity.length() > MAX_SPEED:
            new_velocity = new_velocity.normalize() * MAX_SPEED

        # Limitez la rotation
        current_angle = math.atan2(self.velocity.y, self.velocity.x)
        target_angle = math.atan2(new_velocity.y, new_velocity.x)
        angle_diff = target_angle - current_angle

        # Ajustez l'angle pour rester dans les limites de rotation
        if abs(angle_diff) > math.pi:
            angle_diff -= math.copysign(2 * math.pi, angle_diff)  # Gère la discontinuité de l'angle (-π à π)

        # Ajustez l'angle pour rester dans les limites de rotation
        if abs(angle_diff) > MAX_ROTATION_SPEED:
            angle_diff = MAX_ROTATION_SPEED if angle_diff > 0 else -MAX_ROTATION_SPEED

        # Appliquez la rotation limitée
        new_angle = current_angle + angle_diff
        self.velocity = pygame.Vector2(math.cos(new_angle), math.sin(new_angle)) * new_velocity.length()

        # Met à jour la position
        self.position += self.velocity
        self.acceleration *= 0

        # Gérer les bords de l'écran
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT - SETTINGS_BAR_HEIGHT:
            self.position.y = 0
        elif self.position.y <= 0:
            self.position.y = HEIGHT - SETTINGS_BAR_HEIGHT

    def draw(self, screen):
        angle = math.atan2(self.velocity.y, self.velocity.x)

        if show_vision:  # Afficher les champs de vision uniquement si show_vision est True
            temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            zones = [
                (VIEW_RADIUS, (0, 0, 255, 50)),
                (ALIGN_RADIUS, (0, 255, 0, 50)),
                (SEPARATION_RADIUS, (255, 0, 0, 50))
            ]
            for radius, color in zones:
                points = [self.position]
                num_segments = 50
                start_angle = angle - field_of_view_angle
                end_angle = angle + field_of_view_angle
                for i in range(num_segments + 1):
                    theta = start_angle + (end_angle - start_angle) * i / num_segments
                    x = int(self.position.x + radius * math.cos(theta))
                    y = int(self.position.y + radius * math.sin(theta))
                    points.append((x, y))
                pygame.draw.polygon(temp_surface, color, points)
            screen.blit(temp_surface, (0, 0))

        arrow_tip = self.position + pygame.Vector2(math.cos(angle), math.sin(angle)) * 8
        arrow_left = self.position + pygame.Vector2(math.cos(angle + 2.5), math.sin(angle + 2.5)) * 5
        arrow_right = self.position + pygame.Vector2(math.cos(angle - 2.5), math.sin(angle - 2.5)) * 5
        pygame.draw.polygon(screen, self.color, [arrow_tip, arrow_left, arrow_right])
    
    def avoid_plane(self, plane):
        distance = self.position.distance_to(plane.position)
        if distance < plane.size + VIEW_RADIUS:  # Distance d'évitement
            diff = self.position - plane.position
            diff /= distance  # Normaliser et pondérer
            return diff * MAX_FORCE
        return pygame.Vector2(0, 0)


boids = [Boid() for _ in range(NUM_BOIDS)]


def add_boid():
    boid = Boid()
    boids.append(boid)
    return boids


def remove_boid():
    if len(boids) > 0:
        boids.pop()
    return boids


def clear():
    boids.clear()

# Fonction pour dessiner un slider
def draw_slider(x, y, width, height, knob_x, knob_color, display_text, text_position):
    slider_rect = pygame.Rect(x, y, width, height)
    # Dessiner le rectangle du slider
    pygame.draw.rect(window, (200, 200, 200), slider_rect)
    # Dessiner le trait au milieu du slider
    pygame.draw.line(window, (100, 100, 100), (x, y + height // 2-1), (x + width, y + height // 2-1), 2)
    # Dessiner un tiret vertical au milieu
    mid_x = x + width // 2  # Position horizontale au milieu du slider
    pygame.draw.rect(window, (100, 100, 100), pygame.Rect(mid_x-5, y-7, 10, height+14))
    # Dessiner le cercle du bouton du slider
    pygame.draw.circle(window, knob_color, (knob_x, y + height // 2), 10)

    # Afficher le texte
    text = font_petit.render(display_text, True, (255, 255, 255))
    text_rect = text.get_rect(center=text_position)
    window.blit(text, text_rect)

# Fonction pour vérifier si la souris est sur le cercle d'un slider
def is_knob_clicked(knob_x, knob_y, mouse_pos):
    return knob_x - 10 <= mouse_pos[0] <= knob_x + 10 and knob_y - 10 <= mouse_pos[1] <= knob_y + 10

clock = pygame.time.Clock()
running = True
slider_angle_active = False
slider_align_active = False
slider_cohesion_active = False
slider_separation_active = False

#DEBUG
print(f"Slider positions: Angle({slider_y}), Separation ({separation_slider_y}), Align({align_slider_y}), Cohesion({cohesion_slider_y}))")

plane = Plane()
bombs = []


while running:
    clock.tick(60)
    window.fill((0, 0, 0))

    show_warning = len(bombs) > 0  # Active l'avertissement si au moins une bombe est présente

    if show_warning:
        warning_timer += 1
    else:
        warning_timer = 0

    plane.update()
    plane.draw(window)

    pygame.draw.rect(window, (255, 215, 0), settings_area)
    pygame.draw.rect(window, (50, 50, 50), (0, HEIGHT - 200, WIDTH, 200))

    mouse_pos = pygame.mouse.get_pos()

    # Dessiner le slider pour l'angle
    slider_knob_x = slider_x + int((field_of_view_angle / math.pi) * slider_width)
    draw_slider(slider_x, slider_y, slider_width, slider_height, slider_knob_x, (0, 0, 255),
                f"Angle: {int((field_of_view_angle / math.pi) * 180)}°", angle_display_center)

    # Dessiner le slider pour l'alignement
    align_knob_x = slider_x + int(((ALIGN_RADIUS - ALIGN_RADIUS_MIN) / (ALIGN_RADIUS_MAX - ALIGN_RADIUS_MIN)) * slider_width)
    draw_slider(slider_x, align_slider_y, slider_width, slider_height, align_knob_x, (0, 255, 0),
                f"Align: {int(ALIGN_RADIUS)}", (slider_x + slider_width + 50, align_slider_y + slider_height // 2))

    # Dessiner le slider pour la cohésion
    cohesion_knob_x = slider_x + int(((VIEW_RADIUS - VIEW_RADIUS_MIN) / (VIEW_RADIUS_MAX - VIEW_RADIUS_MIN)) * slider_width)
    draw_slider(slider_x, cohesion_slider_y, slider_width, slider_height, cohesion_knob_x, (0, 0, 255),
                f"Cohesion: {int(VIEW_RADIUS)}", (slider_x + slider_width + 70, cohesion_slider_y + slider_height // 2))

    # Dessiner le slider pour la séparation
    separation_knob_x = slider_x + int(((SEPARATION_RADIUS - SEPARATION_RADIUS_MIN) / (SEPARATION_RADIUS_MAX - SEPARATION_RADIUS_MIN)) * slider_width)
    draw_slider(slider_x, separation_slider_y, slider_width, slider_height, separation_knob_x, (255, 255, 0),
                f"Separation: {int(SEPARATION_RADIUS)}", (slider_x + slider_width + 80, separation_slider_y + slider_height // 2))

    circle_plus_color = (173, 216, 230) if pygame.Rect(circle_plus_center[0] - 30, circle_plus_center[1] - 30, 60, 60).collidepoint(mouse_pos) else (0, 143, 8)
    circle_minus_color = (173, 216, 230) if pygame.Rect(circle_minus_center[0] - 30, circle_minus_center[1] - 30, 60, 60).collidepoint(mouse_pos) or len(boids) == 0 else (0, 143, 8)
    button_clear_color = (173, 216, 230) if button_clear.collidepoint(mouse_pos) or len(boids) == 0 else (0, 143, 8)
    button_pause_color = (173, 216, 230) if button_pause.collidepoint(mouse_pos) else (0, 143, 8)
    button_vision_color = (173, 216, 230) if button_vision.collidepoint(mouse_pos) else (0, 143, 8)

    circle_plus = pygame.draw.circle(window, circle_plus_color, circle_plus_center, 25)
    circle_minus = pygame.draw.circle(window, circle_minus_color, circle_minus_center, 25)
    pygame.draw.rect(window, button_clear_color, button_clear)
    pygame.draw.rect(window, button_pause_color, button_pause)
    pygame.draw.rect(window, button_vision_color, button_vision)

    label = font_petit.render(f"Boids num: {len(boids)}", True, (255, 255, 255))
    text_pause = font_petit.render("Pause" if not paused else "Resume", True, (255, 255, 255))
    text_pause_rect = text_pause.get_rect(center=button_pause_center)
    text_vision = font_petit.render("Hide" if show_vision else "Show", True, (255, 255, 255))
    text_vision_rect = text_vision.get_rect(center=button_vision_center)

    window.blit(text1, text_rect_p)
    window.blit(text2, text_rect_m)
    window.blit(text3, text_rect_clear)
    window.blit(label, label_numboids_center)
    window.blit(text_pause, text_pause_rect)
    window.blit(text_vision, text_vision_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
            if event.key == pygame.K_ESCAPE:  # Si c'est "Échap"
                running = False
            if event.key == pygame.K_SPACE:  # Si l'utilisateur appuie sur la barre d'espace
                plane.drop_bomb()


        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifiez les clics sur chaque slider
            if is_knob_clicked(slider_knob_x, slider_y + slider_height // 2, mouse_pos):
                slider_angle_active = True
            elif is_knob_clicked(align_knob_x, align_slider_y + slider_height // 2, mouse_pos):
                slider_align_active = True
            elif is_knob_clicked(cohesion_knob_x, cohesion_slider_y + slider_height // 2, mouse_pos):
                slider_cohesion_active = True
            elif is_knob_clicked(separation_knob_x, separation_slider_y + slider_height // 2, mouse_pos):
                slider_separation_active = True
            elif circle_minus.collidepoint(event.pos):
                remove_boid()
            elif circle_plus.collidepoint(event.pos):
                add_boid()
            elif button_clear.collidepoint(event.pos):
                clear()
            elif button_pause.collidepoint(event.pos):
                paused = not paused
            elif button_vision.collidepoint(event.pos):
                show_vision = not show_vision

        elif event.type == pygame.MOUSEBUTTONUP:
            slider_angle_active = False
            slider_align_active = False
            slider_cohesion_active = False
            slider_separation_active = False

        if slider_angle_active and pygame.mouse.get_pressed()[0]:
            if slider_x <= mouse_pos[0] <= slider_x + slider_width:
                field_of_view_angle = ((mouse_pos[0] - slider_x) / slider_width) * math.pi
                field_of_view_angle = max(0, min(field_of_view_angle, math.pi))  # Limite l'angle

        if slider_align_active and pygame.mouse.get_pressed()[0]:
            if slider_x <= mouse_pos[0] <= slider_x + slider_width:
                ALIGN_RADIUS = ALIGN_RADIUS_MIN + ((mouse_pos[0] - slider_x) / slider_width) * (ALIGN_RADIUS_MAX - ALIGN_RADIUS_MIN)
                ALIGN_RADIUS = max(ALIGN_RADIUS_MIN, min(ALIGN_RADIUS, VIEW_RADIUS))  # ALIGN dépend de VIEW

                # Mise à jour de SEPARATION_RADIUS si elle dépasse ALIGN_RADIUS
                SEPARATION_RADIUS = min(SEPARATION_RADIUS, ALIGN_RADIUS)

        if slider_cohesion_active and pygame.mouse.get_pressed()[0]:
            if slider_x <= mouse_pos[0] <= slider_x + slider_width:
                VIEW_RADIUS = max(ALIGN_RADIUS, VIEW_RADIUS_MIN + ((mouse_pos[0] - slider_x) / slider_width) * (VIEW_RADIUS_MAX - VIEW_RADIUS_MIN))
                VIEW_RADIUS = min(VIEW_RADIUS, VIEW_RADIUS_MAX)

        if slider_separation_active and pygame.mouse.get_pressed()[0]:
            if slider_x <= mouse_pos[0] <= slider_x + slider_width:
                SEPARATION_RADIUS = SEPARATION_RADIUS_MIN + ((mouse_pos[0] - slider_x) / slider_width) * (ALIGN_RADIUS - SEPARATION_RADIUS_MIN)
                SEPARATION_RADIUS = max(SEPARATION_RADIUS_MIN, min(SEPARATION_RADIUS, ALIGN_RADIUS))  # Synchronisé avec ALIGN_RADIUS

    # Mise à jour et affichage des bombes et des boids
    for bomb in bombs:
        bomb.update()
        bomb.draw(window)
        # Vérifier si les boids sont affectés par l'explosion
        if bomb.exploding:
            boids = [
                boid for boid in boids
                if boid.position.distance_to(bomb.position) >= bomb.explosion_radius
            ]

    # Avertissement de bombes (texte et image)
    if len(bombs) > 0:
        warning_blink_timer += 1
        # Clignotement (visible une frame sur deux)
        if warning_blink_timer % 20 < 10:  # Même logique pour le texte et l'image
            # Affichage du texte d'avertissement
            warning_text = font_petit.render("Warning: Bombs launched!", True, (255, 0, 0))
            window.blit(warning_text, (WIDTH - 300, 20))  # Position en haut à droite

            # Affichage de l'image d'avertissement
            warning_image_rect = warning_image.get_rect(topleft=(20, 20))  # Position en haut à gauche
            window.blit(warning_image, warning_image_rect.topleft)

    if len(bombs) == 0:
        warning_blink_timer = 0  # Réinitialiser le timer lorsque plus de bombes


    # Filtrer les bombes inactives
    bombs = [bomb for bomb in bombs if bomb.is_active()]

    if not paused:
        for boid in boids:
            boid.apply_behaviors(boids, plane, bombs)
            boid.update()

    for boid in boids:
        boid.draw(window)

    pygame.display.flip()

pygame.quit()