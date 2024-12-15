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

BOID_SPEED = 3.5  # Vitesse initiale des boids
BOID_SPEED_MIN = 1  # Limite minimale
BOID_SPEED_MAX = 4  # Limite maximale
SPEED_FACTOR = 1  # Facteur initial, équivalent à x1.0

MAX_SPEED = 2 # Vitesse maximale des boids.
VITESSE_INITIAL = 0.6
MAX_FORCE = 0.03 # Force maximale appliquée pour ajuster leur direction.
VIEW_RADIUS = 130
PLANE_SPEED=5.0

VIEW_RADIUS_MIN = 20
VIEW_RADIUS_MAX = 150
PROP_ALIGN, PROP_SEPARATION = 2/3, 1/3 # les rayons sont proportionnels au debut
ALIGN_RADIUS = PROP_ALIGN * VIEW_RADIUS  # rayon du alignement
SEPARATION_RADIUS = PROP_SEPARATION * VIEW_RADIUS  # rayon du distanciation

MAX_ROTATION_SPEED = math.pi / 8  # Vitesse de rotation maximale (radians par tick)
WIND_FORCE=3
wind_direction = pygame.Vector2(0, 0)  # Direction initiale : pas de vent
ALIGN_RADIUS_MIN = 20
ALIGN_RADIUS_MAX = VIEW_RADIUS_MAX
SEPARATION_RADIUS_MIN = 10
SEPARATION_RADIUS_MAX = ALIGN_RADIUS_MAX
game_area_dimension=(150, 0, WIDTH+400, HEIGHT - 250)
ALIGN_FORCE_SCALE = 4.0  # Force d'alignement paramétrable
AVOID_FORCE_SCALE = 5.0  # Poids à l'évitement des obstacles

s = 20  # Longueur des côtés du triangle
h_triangle = (math.sqrt(3) / 2) * s  # Hauteur du triangle
button_pause_center = (WIDTH - 250, HEIGHT - 90)
triangle_play_point_1 = (
    button_pause_center[0] + (2 * h_triangle) / 3,  # Décalage à droite
    button_pause_center[1]
)
triangle_play_point_2 = (
    button_pause_center[0] - h_triangle / 3,       # Décalage à gauche
    button_pause_center[1] - s / 2                # Décalage vers le haut
)
triangle_play_point_3 = (
    button_pause_center[0] - h_triangle / 3,       # Décalage à gauche
    button_pause_center[1] + s / 2                # Décalage vers le bas
)

# Couleurs
GOLD=(255, 215, 0)
WHITE=(255,255,255)
BLACK =(0, 0, 0)
BLUE=(0, 0, 255)
LIGHT_BLUE=(173, 216, 230)
VERT_CLAIR=(0, 255, 0)
ROUGE=(255, 0, 0)
TRANSPARENT=(0,0,0,0)
WIND_COLOR = (208, 255, 253, 150)  # Cyan avec transparence

# Etat des boutons initiaux 
paused = False
show_vision = False
plane_active = True  # État initial, avec un avion actif
stats_visible = False

stats_rect_width = 0  # Largeur initiale du rectangle pour l'animation
stats_max_width = 250  # Largeur maximale de la zone des statistiques
stats_toggle_speed = 10  # Vitesse d'animation

field_of_view_angle = math.pi / 4  # Angle initial du champ de vision (45°)

# Hauteur de la barre de manipulation
SETTINGS_BAR_HEIGHT = 300
settings_area_center = (0, HEIGHT - SETTINGS_BAR_HEIGHT+50, WIDTH+100, SETTINGS_BAR_HEIGHT)
RECHARGING_BAR_WIDTH=150
RECHARGING_BAR_HEIGHT=HEIGHT

# Limites du monde torique
TORIC_WORLD_MIN_X = RECHARGING_BAR_WIDTH
TORIC_WORLD_MAX_X = WIDTH + 50
TORIC_WORLD_MIN_Y = 0
TORIC_WORLD_MAX_Y = HEIGHT - SETTINGS_BAR_HEIGHT + 40


# SLIDER Position
SLIDER_HORIZONTAL_OFFSET = -100  # Décalage global horizontal (vers la gauche)
SLIDER_VERTICAL_OFFSET = 25  # Décalage global vertical des sliders

# Centres et zones
screen_center = (WIDTH, HEIGHT)
game_area_center = (0, 0, WIDTH, HEIGHT - SETTINGS_BAR_HEIGHT)

recharging_area_dimension=(0, 0, RECHARGING_BAR_WIDTH, RECHARGING_BAR_HEIGHT+100)
label_numboids_center = (WIDTH - 155, HEIGHT - 50)
circle_plus_center = (WIDTH - 50, HEIGHT - 100)
circle_minus_center = (WIDTH - 125, HEIGHT - 100)
slider_x = 300 + SLIDER_HORIZONTAL_OFFSET
slider_y = HEIGHT - 200 + 10 + SLIDER_VERTICAL_OFFSET # Slider pour l'angle
slider_width = 300
slider_height = 10
plane_speed_slider_y = slider_y - 50
separation_slider_y = slider_y + 50  # Slider pour la séparation
align_slider_y = separation_slider_y + 50  # Slider pour l'alignement
cohesion_slider_y = align_slider_y + 50  # Slider pour la cohésion
pause_width = 8   # Largeur des rectangles
pause_height = 25  # Hauteur des rectangles
gap_between = 10   # Espace entre les deux rectangles

# Calcul des dimensions centrées
tirer_pause_left_dimension = (
    button_pause_center[0] - (pause_width + gap_between // 2),  # Position x du rectangle gauche
    button_pause_center[1] - pause_height // 2,                # Position y pour centrer verticalement
    pause_width,
    pause_height
)
tirer_pause_right_dimension = (
    button_pause_center[0] + gap_between // 2,                 # Position x du rectangle droit
    button_pause_center[1] - pause_height // 2,                # Position y pour centrer verticalement
    pause_width,
    pause_height
)
tirer_pause_left = pygame.Rect(tirer_pause_left_dimension)
tirer_pause_right = pygame.Rect(tirer_pause_right_dimension)
angle_display_center = (slider_x + slider_width + 60, slider_y + slider_height // 2)
radius_display_center = (slider_x + slider_width + 50, separation_slider_y + slider_height // 2)

button_clear_center = (WIDTH - 250, HEIGHT - 140, 80, 40)
button_clear = pygame.Rect(button_clear_center[0] - 40, button_clear_center[1] - 20, 80, 40)
button_pause_center = (WIDTH - 250, HEIGHT - 90)
button_pause = pygame.Rect(button_pause_center[0] - 40, button_pause_center[1] - 20, 80, 40)
button_vision_center = (WIDTH - 250, HEIGHT - 40)
button_vision = pygame.Rect(button_vision_center[0] - 40, button_vision_center[1] - 20, 80, 40)
button_plane_center = (WIDTH - 250, HEIGHT - 190)
button_plane = pygame.Rect(button_plane_center[0] - 40, button_plane_center[1] - 20, 80, 40)
button_stats_center = (WIDTH - 50, HEIGHT - 225)
button_stats = pygame.Rect(button_stats_center[0] - 40, button_stats_center[1] - 20, 120, 40)
settings_area_dimension=(200, HEIGHT - 100, WIDTH, 100)
button_accelerate_center = (WIDTH - 350, HEIGHT - 50)
button_decelerate_center = (WIDTH - 450, HEIGHT - 50)

# Screen
window = pygame.display.set_mode(screen_center, pygame.FULLSCREEN)
pygame.display.set_caption("Simulation de Boids")

# Zones
game_area = pygame.Rect(game_area_center)
settings_area = pygame.Rect(settings_area_center)
recharging_area = pygame.Rect(recharging_area_dimension)
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
text_rect_clear = text3.get_rect(center=(WIDTH - 250, HEIGHT - 140))

# Avertissement bombe
show_warning = False
warning_timer = 0  # Pour gérer le clignotement

## Charger les images avec un chemin dynamique (AVEC DEBUG)
# image Plane
plane_image_path = os.path.join(os.path.dirname(__file__), "imageBoids", "plane.png")
if not os.path.exists(plane_image_path):
    raise FileNotFoundError(f"Le fichier plane.png est introuvable au chemin {plane_image_path}")
plane_image = pygame.image.load(plane_image_path)
plane_image = pygame.transform.scale(plane_image, (200, 200))
plane_image = pygame.transform.rotate(plane_image, -90)  # Rotation initiale

# image Warning
warning_image_path = os.path.join(os.path.dirname(__file__), "imageBoids", "warning.jpg")
if not os.path.exists(warning_image_path):
    raise FileNotFoundError(f"L'image d'avertissement est introuvable au chemin {warning_image_path}")
warning_image = pygame.image.load(warning_image_path)
warning_image = pygame.transform.scale(warning_image, (100, 100))  # Ajustez la taille si nécessaire
warning_blink_timer = 0

# image Bomb
bomb_size = 50
image_path = os.path.join(os.path.dirname(__file__), "imageBoids", "bomb.png")
if not os.path.exists(image_path):
        raise FileNotFoundError(f"Le fichier bomb.png est introuvable au chemin {image_path}")
bomb_image = pygame.image.load(image_path)
bomb_image = pygame.transform.scale(bomb_image, (bomb_size, bomb_size))  # Global
bomb_image = pygame.transform.rotate(bomb_image, -90)  # Tourner l'image de 90 degrés vers la droite

triangle_play = [
            triangle_play_point_1,  # Sommet droit
            triangle_play_point_2,  # Sommet inférieur gauche
            triangle_play_point_3,  # Sommet supérieur gauche
        ]

# RADAR (BONUS)
RADAR_CENTER_X = WIDTH//2 + 100  # Position x du centre du radar dans la barre settings
RADAR_CENTER_Y = HEIGHT - SETTINGS_BAR_HEIGHT // 2 + 20  # Position y du radar
RADAR_RADIUS = 100  # Rayon du radar
RADAR_COLOR = (0, 255, 0)  # Vert radar
RADAR_NUM_CIRCLES = 4  # Nombre de cercles concentriques
RADAR_CIRCLE_SPACING = 30  # Distance entre chaque cercle
RADAR_LINE_COLOR = (0, 255, 0)  # Couleur des lignes centrales
RADAR_LINE_WIDTH = 2  # Épaisseur des lignes centrales

RADAR_BOID_COLOR = LIGHT_BLUE  # Couleur des boids sur le radar
RADAR_PLANE_COLOR = ROUGE  # Couleur de l'avion sur le radar
RADAR_SCALE = 0.1  # Échelle pour réduire la distance réelle des boids

radar_sweep_angle = 0  # Angle initial (en degrés)
radar_sweep_speed = 2  # Vitesse du balayage (en degrés par frame)
radar_trail = []  # Liste des angles précédents pour la trace
message_display_timer = 0  # Durée pour afficher le message

# Mode : Interaction avec la souris
interaction_mode = False  # Mode désactivé par défaut

# Mode : 8 (Lemniscate)
eight_mode = False  # Désactivé par défaut
t = 0 # Temps initial
eight_center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)  # Centre du chemin
eight_scale = 200  # Taille du chemin (rayon)

# Mode : vent
wind_mode = False  # Mode vent désactivé par défaut

# AFFICHAGE MESSAGES
mode_message = ""
message_timer = 0  # Timer pour afficher les messages
MESSAGE_DURATION = 120  # Durée d'affichage du message en frames (ex : 2 secondes)


class Bomb:
    # Initialise une bombe avec sa position et ses attributs par défaut
    def __init__(self, position):
        self.image = bomb_image
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

    # Met à jour l'état de la bombe (descente, fixation, explosion)
    def update(self):
        # Rotation incrémentale
        if not self.rotation_complete:
            self.current_angle += self.rotation_speed # Augmenter l'angle de rotation
            if self.current_angle >= self.target_angle: # Vérifier si la rotation est complète
                self.current_angle = self.target_angle
                self.rotation_complete = True

        # Descente ou fixation
        if not self.fixed:
            self.velocity.y = max(self.velocity.y - 0.1, 0)  # Réduit la vitesse jusqu'à 0
            self.position += self.velocity

            # Gestion des limites toriques
            if self.position.x > TORIC_WORLD_MAX_X:
                self.position.x = TORIC_WORLD_MIN_X
            elif self.position.x < TORIC_WORLD_MIN_X:
                self.position.x = TORIC_WORLD_MAX_X
            if self.position.y > TORIC_WORLD_MAX_Y:
                self.position.y = TORIC_WORLD_MIN_Y
            elif self.position.y < TORIC_WORLD_MIN_Y:
                self.position.y = TORIC_WORLD_MAX_Y

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

    # Dessine la bombe ou l'explosion à l'écran
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

    # Vérifie si la bombe est encore active (pas détruite)
    def is_active(self):
        return self.lifespan > 0

class Plane:
    # Initialise l'avion avec une position et une vitesse par défaut
    def __init__(self):
        self.position = pygame.Vector2(WIDTH // 2, HEIGHT // 2)  # Position initiale
        self.velocity = pygame.Vector2(random.choice([-1, 1]) * 2, random.uniform(-0.5, 0.5)).normalize() * PLANE_SPEED  # Mouvement
        self.image = plane_image
        self.size = 50
    
    # Met à jour la position de l'avion
    def update(self):
        if paused:
            return
        else:
            self.position += self.velocity

            # Gérer les bords pour que l'avion réapparaisse de l'autre côté
            if self.position.x > TORIC_WORLD_MAX_X:
                self.position.x = -self.image.get_width()
            elif self.position.x < -self.image.get_width():
                self.position.x = TORIC_WORLD_MAX_X 
            if self.position.y > TORIC_WORLD_MAX_Y:
                self.position.y = 0
            elif self.position.y < 0:
                self.position.y = TORIC_WORLD_MAX_Y
            
            # Recalibrer la vitesse pour qu'elle reste constante
            self.velocity = self.velocity.normalize() * PLANE_SPEED

    # Dessine l'avion avec une rotation correspondant à sa direction
    def draw(self, screen):
        # Calcul de l'angle basé sur la direction de la vitesse
        angle = math.degrees(math.atan2(self.velocity.y, self.velocity.x))
        
        # Applique la rotation de l'image
        rotated_image = pygame.transform.rotate(self.image, -angle)
        rotated_rect = rotated_image.get_rect(center=(self.position.x, self.position.y))
        
        # Dessine l'image tournée
        screen.blit(rotated_image, rotated_rect.topleft)
    
    # Dépose une bombe à la position actuelle de l'avion
    def drop_bomb(self):
        bombs.append(Bomb(self.position))

class Boid:
    # Initialise un boid avec une position et des attributs par défaut
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(200, WIDTH), random.uniform(0, HEIGHT-SETTINGS_BAR_HEIGHT))
        
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * BOID_SPEED_MAX
        self.acceleration = pygame.Vector2(0, 0)
        self.state = "active"  # "active", "recharging"
        self.battery = random.randint(10,95)
        self.color = (255, 255, 255)  # Couleur par défaut : blanche
        self.wind="none" #"None" , "up" ,"down" ,"right","left"
    
    # Applique les forces comportementales (alignement, cohésion, séparation, etc.)
    def apply_behaviors(self, boids, plane, bombs, eight_mode=False, eight_center=None, eight_scale=None):
        if paused:
            return

        if self.state == "active":
            # Initialiser les forces
            alignment = pygame.Vector2(0, 0)
            cohesion = pygame.Vector2(0, 0)
            separation = pygame.Vector2(0, 0)
            avoid_plane = pygame.Vector2(0, 0)
            eight_force = pygame.Vector2(0, 0)
            attraction_force = pygame.Vector2(0, 0)
            avoidance_force = pygame.Vector2(0, 0)

            # Ajuster dynamiquement le champ de vision en fonction de la distance avec l'avion
            distance_to_plane = float('inf')  # Valeur par défaut si l'avion n'existe pas
            if plane_active and plane is not None:
                distance_to_plane = self.position.distance_to(plane.position)
            adjusted_view_radius = VIEW_RADIUS
            if plane_active and plane is not None and distance_to_plane < plane.size + VIEW_RADIUS:
                adjusted_view_radius = VIEW_RADIUS * 1.5  # Augmenter le champ de vision

            # Appliquer les forces comportementales normales si le mode "interaction" n'est pas activé
            if not interaction_mode:
                alignment = self.align(boids, adjusted_view_radius)
                cohesion = self.cohere(boids, adjusted_view_radius)
                separation = self.separate(boids, adjusted_view_radius)
                avoid_plane = self.avoid_plane(plane) if plane_active and plane is not None else pygame.Vector2(0, 0)

                if eight_mode:
                    eight_force = self.follow_eight_path(eight_center, eight_scale)

            # Gestion du mode interaction avec la souris
            if interaction_mode:
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                distance_to_mouse = self.position.distance_to(mouse_pos)

                # Force d'attraction vers la souris (centre de masse)
                if distance_to_mouse > 50:  # Rayon de sécurité autour de la souris
                    attraction_force = (mouse_pos - self.position).normalize() * MAX_FORCE

                # Force de répulsion pour éviter d'entrer dans le cercle
                if distance_to_mouse < 50:
                    avoidance_force = (self.position - mouse_pos).normalize() * MAX_FORCE

            # Combiner toutes les forces avec des pondérations adaptées
            self.acceleration += (
                0.6 * alignment +
                0.5 * cohesion +
                0.8 * separation +
                1.5 * avoid_plane +
                1.2 * eight_force +
                1.0 * attraction_force +  # Influence de la souris
                1.2 * avoidance_force     # Évite la souris
            )

            # Mettre à jour la couleur en fonction des interactions
            self.check_battery_color()
            if separation.length() > 0:
                self.color = (148, 0, 211)  # Séparation
            elif alignment.length() > 0:
                self.color = (255, 20, 147)  # Alignement
            elif cohesion.length() > 0:
                self.color = (255, 182, 150)  # Cohésion
            else:
                self.color = (255, 255, 255)  # Blanc : aucune interaction

        # Vérifier si le boid entre en collision avec une bombe
        for bomb in bombs:
            distance = self.position.distance_to(bomb.position)
            if distance < bomb.radius:  # Si le boid touche une bombe
                self.position = pygame.Vector2(
                    random.uniform(0, WIDTH),
                    random.uniform(0, HEIGHT - SETTINGS_BAR_HEIGHT)
                )
                break  # Éviter plusieurs téléportations en un seul tick

    # Applique les effets du vent sur le boid    
    def apply_wind(self):
        if paused and wind_mode:
            return
        else:
            if wind_direction.length() > 0:  # Si un vent est actif
                # Normaliser la direction du vent pour obtenir un vecteur directionnel
                target_direction = wind_direction.normalize()

                # Calculer l'angle entre la direction actuelle et la direction cible
                angle = self.velocity.angle_to(target_direction)

                # Limiter la rotation par frame
                max_rotation_angle = 3  # Limite en degrés (par exemple, 3° par frame)

                if abs(angle) > max_rotation_angle:
                    # Déterminer le sens de la rotation
                    rotation_sign = 0.5 if angle > 0 else -1
                    self.velocity = self.velocity.rotate(rotation_sign * max_rotation_angle)
                else:
                    # Si l'angle est inférieur à la limite, aligner directement
                    self.velocity = target_direction * self.velocity.length()

                # Limiter la vitesse à MAX_SPEED
                if self.velocity.length() > BOID_SPEED_MAX:
                    self.velocity = self.velocity.normalize() * BOID_SPEED_MAX

    # Vérifie si un autre boid est dans le champ de vision
    def is_in_field_of_view(self, other_position):
        # Vérifie si un boid est dans le champ de vision
        direction_to_other = (other_position - self.position).normalize()
        velocity_angle = math.atan2(self.velocity.y, self.velocity.x)
        other_angle = math.atan2(direction_to_other.y, direction_to_other.x)
        angle_difference = abs(velocity_angle - other_angle)
        return angle_difference <= field_of_view_angle
    
    # Change les couleurs en fonction de la fatigue
    def check_battery_color(self):
        if self.battery<=20 and self.state=="active":
             self.color=ROUGE
        elif self.battery<=100 and self.battery>=97:
            self.color=VERT_CLAIR    
        else:
             self.color=WHITE

    # Phase de decharge des boids
    def decharging_phase(self):
        if paused==False:
            base_consumption = 0.02  # Consommation normale à une vitesse de base
            self.battery -= base_consumption * BOID_SPEED
        else:
            self.battery=self.battery    

    ## Comportement fondamental pour l'alignement de chaque boid    
    def align(self, boids, view_radius):
        steering = pygame.Vector2(0, 0)
        total = 0
        center_of_mass = pygame.Vector2(0, 0)

        for other in boids:
            if other != self:
                distance = self.position.distance_to(other.position)
                if SEPARATION_RADIUS < distance < view_radius and self.is_in_field_of_view(other.position):
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

    ## Comportement fondamental pour la cohesion de chaque boid    
    def cohere(self, boids, view_radius):
        steering = pygame.Vector2(0, 0)
        total = 0
        for other in boids:
            if other != self:
                distance = self.position.distance_to(other.position)
                if ALIGN_RADIUS < distance < view_radius and self.is_in_field_of_view(other.position):
                    steering += other.position
                    total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            steering = steering.normalize() * MAX_FORCE
        return steering

    ## Comportement fondamental pour la distanciation entre les boids   
    def separate(self, boids, view_radius):
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

    # Met à jour la position et la vitesse du boid
    def update(self):
        if paused:
            return

        # Ajuster la limite de rotation en fonction de la vitesse de l'avion
        global plane
        if plane_active and plane is not None:
            dynamic_max_rotation_speed = MAX_ROTATION_SPEED + (plane.velocity.length() / PLANE_SPEED) * 0.05
        else:
            dynamic_max_rotation_speed = MAX_ROTATION_SPEED  # Utilisez une valeur par défaut si l'avion n'est pas actif

        if eight_mode:  # Si le mode en 8 est activé
            # Force d'attraction vers le chemin en 8
            attraction = self.attract_to_eight(t, eight_center, eight_scale)
            self.acceleration += attraction
            
            # Renforcer l'alignement et la cohésion pour un mouvement fluide
            alignment = self.align(boids, ALIGN_RADIUS)
            cohesion = self.cohere(boids, VIEW_RADIUS)
            self.acceleration += 0.8 * alignment + 0.5 * cohesion
        else:
            # Comportement normal
            self.apply_behaviors(boids, plane, bombs)

        # Calculez la nouvelle direction avec accélération
        new_velocity = self.velocity + self.acceleration
        if new_velocity.length() > BOID_SPEED:
            new_velocity = new_velocity.normalize() * BOID_SPEED * SPEED_FACTOR
        if new_velocity.length() < BOID_SPEED_MIN:
            new_velocity = new_velocity.normalize() * BOID_SPEED_MIN * SPEED_FACTOR

        # Limitez la rotation
        current_angle = math.atan2(self.velocity.y, self.velocity.x)
        target_angle = math.atan2(new_velocity.y, new_velocity.x)
        angle_diff = target_angle - current_angle

        # Ajustez l'angle pour rester dans les limites de rotation
        if abs(angle_diff) > dynamic_max_rotation_speed:
            angle_diff -= math.copysign(2 * math.pi, angle_diff)  # Gère la discontinuité de l'angle (-π à π)

        # Ajustez l'angle pour rester dans les limites de rotation
        if abs(angle_diff) > MAX_ROTATION_SPEED:
            angle_diff = dynamic_max_rotation_speed if angle_diff > 0 else -dynamic_max_rotation_speed

        # Appliquez la rotation limitée
        new_angle = current_angle + angle_diff
        self.velocity = pygame.Vector2(math.cos(new_angle), math.sin(new_angle)) * new_velocity.length()
        # Réduire la batterie seulement si on n'est pas en pause
        self.decharging_phase()
        # Met à jour la position
        self.position += self.velocity
        self.acceleration *= 0
        # Si la batterie est vide, passer en mode "recharge"
        if self.battery <= 0:
            self.state = "recharging"
        # Gérer les bords de l'écran
        if self.position.x > TORIC_WORLD_MAX_X and self.state == "active":
            self.position.x = RECHARGING_BAR_WIDTH
        elif self.position.x < RECHARGING_BAR_WIDTH and self.state == "active":
            self.position.x = TORIC_WORLD_MAX_X 
        if self.position.y > TORIC_WORLD_MAX_Y:
            self.position.y = 0
        elif self.position.y <= 0:
            self.position.y = TORIC_WORLD_MAX_Y

    # Placer les boids a gauche lors de la phase de recharge 
    def find_empty_spot_in_recharging_area(self):
        global recharging_boids
        for y in range(20, RECHARGING_BAR_HEIGHT, 20):
            if y not in recharging_boids:
                # Si cet emplacement est libre, on y place le boid
            
                recharging_boids[y] = boid  # Ajouter le boid à cet emplacement
                return y

        # Si aucun emplacement n'est libre
        
        return None
    
    # Dessine le rectangle de recharge
    def draw_recharging_rectangle(self,y):
        x = 20
        width = 50 #largeur du rectangle charging
        height = 15 #longueur du rectangle charging
        top_y = y - 5  # Rectangle centré sur y

        # Diviser le rectangle en 5 parties égales
        segment_width = width // 5

        for i in range(5):
            # Déterminer la couleur du segment
            if self.battery >= (i + 1) * 20:  # Si la batterie couvre ce segment
                color = VERT_CLAIR  # Vert clair
            elif self.battery <= 20 and i == 0:  # Batterie critique
                color = ROUGE  # Rouge
            else:
                color = TRANSPARENT  # Transparent

            # Calculer les dimensions du segment
            segment_rect = pygame.Rect(x + i * segment_width, top_y, segment_width, height)

            # Dessiner le segment
            pygame.draw.rect(window, color, segment_rect)

    # Met a jour l'animation de recharge
    def update_charging(self):
        global recharging_boids
        offset_y = 30
        if self.state == "recharging":
            # Si le jeu n'est pas en pause, procéder à la mise à jour
            if paused == False:
                # Vérifie si le boid est déjà assigné à un emplacement
                boid_y = None
                for y, assigned_boid in recharging_boids.items():
                    if assigned_boid == self:
                        boid_y = y
                        break

                # Si le boid n'est pas encore assigné, chercher un nouvel emplacement
                if boid_y is None:
                    boid_y = self.find_empty_spot_in_recharging_area()
                    if boid_y is None:
                        return  # Arrête la mise à jour si aucun emplacement n'est disponible

                # Dessiner le rectangle de recharge avec la batterie actuelle
                self.draw_recharging_rectangle(boid_y + offset_y)
                self.position = pygame.Vector2(10, boid_y - 1 + offset_y)

                # Recharge plus lente si la batterie n'est pas pleine
                if self.battery < 100:
                    self.battery += 2.5  # Recharge plus lente

            else:
                # Lorsque le jeu est en pause, maintenir le boid dans son état actuel
                # Dessiner le rectangle de recharge sans mettre à jour la batterie
                boid_y = None
                for y, assigned_boid in recharging_boids.items():
                    if assigned_boid == self:
                        boid_y = y
                        break
                
                if boid_y is not None:
                    self.draw_recharging_rectangle(boid_y)

        # Lorsque la batterie est pleine, déplacer le boid et le réactiver
        if self.battery >= 100:
            self.position = pygame.Vector2(random.uniform(200, WIDTH), random.uniform(0, HEIGHT - 100))
            self.battery = 100
            self.state = "active"
            
            # Libérer l'emplacement dans l'area de recharge
            for y, assigned_boid in recharging_boids.items():
                if assigned_boid == self:
                    recharging_boids.pop(y)
                    break            

    # Dessiner un boid
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
        arrow_tip_bordure = self.position + pygame.Vector2(math.cos(angle), math.sin(angle)) * 10
        arrow_left_bordure = self.position + pygame.Vector2(math.cos(angle + 2.5), math.sin(angle + 2.5)) * 6
        arrow_right_bordure = self.position + pygame.Vector2(math.cos(angle - 2.5), math.sin(angle - 2.5)) * 6
        
        pygame.draw.polygon(screen, self.color, [arrow_tip, arrow_left, arrow_right])
        pygame.draw.polygon(screen, BLACK, [arrow_tip_bordure, arrow_left_bordure, arrow_right_bordure], width = 1)
    
    # Eviter l'avion dependant de la vitesse de celui-ci
    def avoid_plane(self, plane):
        distance = self.position.distance_to(plane.position)
        if distance < plane.size + VIEW_RADIUS:  # Distance d'évitement
            diff = self.position - plane.position
            diff /= distance  # Normaliser et pondérer
            plane_speed_factor = plane.velocity.length() / PLANE_SPEED  # Facteur basé sur la vitesse
            return diff * MAX_FORCE * (1.5 + plane_speed_factor * 3)  # Augmente l'effet en fonction de la vitesse
        return pygame.Vector2(0, 0)
    
    # Attire le boid vers le chemin en forme de 8.
    def attract_to_eight(self, t, center, scale):
        path_position = eight_path(t, center, scale)
        attraction_force = path_position - self.position  # Force vers le chemin
        attraction_strength = 0.05  # Ajustez l'intensité
        return attraction_force.normalize() * attraction_strength
    
    # Calcule une force qui attire le boid vers le chemin en 8
    def follow_eight_path(self, eight_center, eight_scale):
        """
        Calcule une force qui attire le boid vers le chemin en 8.
        :param eight_center: Centre du chemin en 8.
        :param eight_scale: Taille du chemin en 8.
        :return: Une force vectorielle.
        """
        t = (pygame.time.get_ticks() % 5000) / 5000  # Tension dynamique (cycle)
        target = eight_path(t, eight_center, eight_scale)
        steering = pygame.Vector2(target) - self.position  # Calcul de la direction vers le chemin
        distance = steering.length()

        if distance > 0:  # Évite la division par zéro
            steering = steering.normalize() * MAX_FORCE  # Applique une force limitée
        return steering

# Creation des boids
boids = [Boid() for _ in range(NUM_BOIDS)]

recharging_boids={}
wind_offset = 0  # Déplacement initial des lignes
wind_offset = 0  # Déplacement initial des lignes

# Fonction pour dessiner dynamiquement le vent
def draw_wind_in_area(screen, wind_direction, game_area_dimension, wind_offset):
    x, y, w, h = game_area_dimension  # Extraire les dimensions de la zone
    wind_surface = pygame.Surface((w, h), pygame.SRCALPHA)  # Créer une surface pour la zone
    wind_surface.fill((0, 0, 0, 0))  # Remplir avec transparent

    # Dessiner des lignes selon la direction du vent
    if wind_direction.x != 0:  # Vent horizontal (gauche/droite)
        for i in range(0, h, 18):  # Espacement vertical des lignes
            start_x = (wind_offset * abs(wind_direction.x)) % w  # Calcul du point de départ
            if wind_direction.x > 0:  # Vent vers la droite
                end_x = start_x + w
            else:  # Vent vers la gauche
                end_x = start_x - w

            pygame.draw.line(
                wind_surface,
                WIND_COLOR,  # Gris clair avec transparence
                (start_x, i),  # Point de départ
                (end_x, i),  # Point de fin
                3  # Épaisseur de ligne
            )
    elif wind_direction.y != 0:  # Vent vertical (haut/bas)
        for i in range(0, w, 18):  # Espacement horizontal des lignes
            start_y = (wind_offset * abs(wind_direction.y)) % h  # Calcul du point de départ
            if wind_direction.y > 0:  # Vent vers le bas
                end_y = start_y + h
            else:  # Vent vers le haut
                end_y = start_y - h

            pygame.draw.line(
                wind_surface,
                WIND_COLOR ,  # Gris clair avec transparence
                (i, start_y),  # Point de départ
                (i, end_y),  # Point de fin
                3  # Épaisseur de ligne
            )

    # Ajouter la surface de vent à l'écran principal
    screen.blit(wind_surface, (x, y))

# Fonction pour ajouter un boid
def add_boid():
    boid = Boid()
    boids.append(boid)
    return boids

# Fonction pour supprimer un boid
def remove_boid():
    if len(boids) > 0:
        boids.pop()
    return boids

# Fonction pour nettoyer les boids 
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

# Fonction pour dessiner un radar (AFFICHAGE DYNAMIQUE)
def draw_radar(screen, boids, plane):
    global radar_sweep_angle  # Utiliser la variable globale pour mettre à jour l'angle du faisceau

    # Position et dimensions du radar
    radar_center = (RADAR_CENTER_X, RADAR_CENTER_Y)
    radar_radius = RADAR_RADIUS

    # Dessiner le fond du radar
    pygame.draw.circle(screen, (0, 50, 0), radar_center, radar_radius)  # Cercle vert foncé
    pygame.draw.circle(screen, (0, 255, 0), radar_center, radar_radius, 2)  # Bordure externe

    # Dessiner les cercles concentriques du radar
    for i in range(1, RADAR_NUM_CIRCLES):
        pygame.draw.circle(
            screen,
            RADAR_COLOR,
            (RADAR_CENTER_X, RADAR_CENTER_Y),
            i * RADAR_CIRCLE_SPACING,
            width=1  # Épaisseur des cercles
        )

    # Dessiner les lignes horizontale et verticale centrées sur l'avion
    pygame.draw.line(
        screen,
        RADAR_LINE_COLOR,
        (RADAR_CENTER_X - RADAR_RADIUS, RADAR_CENTER_Y),
        (RADAR_CENTER_X + RADAR_RADIUS, RADAR_CENTER_Y),
        RADAR_LINE_WIDTH
    )
    pygame.draw.line(
        screen,
        RADAR_LINE_COLOR,
        (RADAR_CENTER_X, RADAR_CENTER_Y - RADAR_RADIUS),
        (RADAR_CENTER_X, RADAR_CENTER_Y + RADAR_RADIUS),
        RADAR_LINE_WIDTH
    )

    # Surface temporaire pour dessiner le cône transparent
    radar_surface = pygame.Surface((radar_radius * 2, radar_radius * 2), pygame.SRCALPHA)
    radar_surface.fill((0, 0, 0, 0))  # Remplir avec du transparent

    # Calcul des angles du cône
    sweep_start_angle = math.radians(radar_sweep_angle)
    sweep_end_angle = math.radians(radar_sweep_angle + 30)

    # Calcul des coordonnées des extrémités du cône
    start_x = radar_radius + radar_radius * math.cos(sweep_start_angle)
    start_y = radar_radius + radar_radius * math.sin(sweep_start_angle)
    end_x = radar_radius + radar_radius * math.cos(sweep_end_angle)
    end_y = radar_radius + radar_radius * math.sin(sweep_end_angle)

    # Dessiner le cône sur la surface temporaire
    pygame.draw.polygon(
        radar_surface,
        (0, 255, 0, 100),  # Couleur verte translucide
        [(radar_radius, radar_radius), (start_x, start_y), (end_x, end_y)]
    )

    # Dessiner la surface temporaire sur l'écran principal
    screen.blit(radar_surface, (radar_center[0] - radar_radius, radar_center[1] - radar_radius))

    # Dessiner les boids dans le radar
    for boid in boids:
        if plane_active and plane is not None:
            distance = plane.position.distance_to(boid.position)
        else:
            distance = float('inf')  # Assurez-vous que le boid ne réagit pas si l'avion est absent
        if distance < RADAR_NUM_CIRCLES * 100:
            # Normaliser la position par rapport au radar
            normalized_x = (boid.position.x - plane.position.x) / (RADAR_NUM_CIRCLES * 100) * radar_radius
            normalized_y = (boid.position.y - plane.position.y) / (RADAR_NUM_CIRCLES * 100) * radar_radius

            # Calculer la position sur le radar
            boid_radar_x = radar_center[0] + int(normalized_x)
            boid_radar_y = radar_center[1] + int(normalized_y)

            # Calculer l'angle du boid par rapport au centre
            boid_angle = math.degrees(math.atan2(boid_radar_y - radar_center[1], boid_radar_x - radar_center[0])) % 360

            # Vérifier si le boid est dans le cône
            if radar_sweep_angle <= boid_angle <= radar_sweep_angle + 30:
                boid_color = (0, 255, 0)  # Vert vif si dans le cône
            else:
                boid_color = (0, 100, 0)  # Vert foncé sinon

            # Dessiner le boid sur le radar
            pygame.draw.circle(screen, boid_color, (boid_radar_x, boid_radar_y), 3)  # Boid sur le radar

    # Mettre à jour l'angle du balayage uniquement si la simulation n'est pas en pause
    if not paused:
        radar_sweep_angle = (radar_sweep_angle + radar_sweep_speed) % 360  # Rotation continue

# Fonction pour afficher la légende au radar
def draw_radar_legend(screen):
    """Dessine une légende pour le radar."""
    font = pygame.font.Font(None, 30)  # Police pour la légende
    legend_x = RADAR_CENTER_X + RADAR_RADIUS + 20  # Position de la légende
    legend_y = RADAR_CENTER_Y - RADAR_RADIUS

    # Dessiner un exemple de cercle concentrique
    pygame.draw.circle(screen, RADAR_COLOR, (legend_x, legend_y + 20), 10, 1)
    text = font.render("Zones du radar", True, (255, 255, 255))
    screen.blit(text, (legend_x + 20, legend_y + 10))

    # Dessiner un exemple de faisceau (balayage)
    # Créer une surface temporaire
    sweep_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    sweep_surface.fill((0, 0, 0, 0))  # Remplir avec du transparent

    # Dessiner le triangle sur la surface temporaire
    pygame.draw.polygon(sweep_surface, (0, 255, 0, 100), [
        (0, 10),  # Ajustez les points en fonction des dimensions de la surface
        (30, 0),
        (30, 20)
    ])

    # Blitter la surface temporaire sur l'écran principal
    screen.blit(sweep_surface, (legend_x - 15, legend_y + 50))

    text = font.render("Balayage", True, (255, 255, 255))
    screen.blit(text, (legend_x + 20, legend_y + 50))

    # Dessiner un exemple de boid
    pygame.draw.circle(screen, (0, 255, 0), (legend_x, legend_y + 100), 5)
    text = font.render("Boid détecté", True, (255, 255, 255))
    screen.blit(text, (legend_x + 20, legend_y + 90))

# Fonction qui dessine le titre du projet
def draw_project_title(screen, title="ASFOUR"):
    # Couleurs et style
    title_color = (255, 255, 255)  # Blanc
    background_color = (0, 0, 0, 150)  # Noir semi-transparent
    font_size = 72  # Taille de la police
    font = pygame.font.Font(None, font_size)

    # Texte et arrière-plan
    title_surface = font.render(title, True, title_color)
    title_rect = title_surface.get_rect(center=(WIDTH // 2 + 100, 50))  # Centré en haut
    background_rect = pygame.Rect(
        title_rect.left - 20, title_rect.top - 10,  # Marges
        title_rect.width + 40, title_rect.height + 20
    )
 
    # Dessiner le rectangle semi-transparent
    temp_surface = pygame.Surface((background_rect.width, background_rect.height), pygame.SRCALPHA)
    temp_surface.fill(background_color)
    screen.blit(temp_surface, (background_rect.left, background_rect.top))

    # Dessiner le texte
    screen.blit(title_surface, title_rect)

# Calcule un point regroupant les boids sur le chemin en 8
def eight_path(t, center, scale):
    """
    Calcule un point sur le chemin en 8.
    :param t: Position relative sur le chemin (entre 0 et 1).
    :param center: Centre de la forme (pygame.Vector2).
    :param scale: Taille de la forme.
    :return: Un point (pygame.Vector2) sur le chemin.
    """
    x = center[0] + scale * math.sin(t * 2 * math.pi)
    y = center[1] + scale * math.sin(t * 4 * math.pi) * math.cos(t * 2 * math.pi)
    return (x, y)  # Retourne un tuple pour compatibilité avec pygame.draw.line

# Fonction pour afficher dependant du mode active/desactive
def display_message(window, message, duration, color=(255, 255, 255), bg_color=(0, 0, 0)):
    font_message = pygame.font.Font(None, 50)
    text_surface = font_message.render(message, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
    pygame.draw.rect(window, bg_color, text_rect.inflate(20, 10))
    window.blit(text_surface, text_rect)


clock = pygame.time.Clock()
running = True
slider_angle_active = False
slider_align_active = False
slider_cohesion_active = False
slider_separation_active = False
slider_plane_speed_active = False

# Creation d'un avion avec ses bombes par defaut
plane = Plane()
bombs = []
 
# Boucle principal
while running:
    clock.tick(60)
    window.fill(LIGHT_BLUE)
    draw_project_title(window, title="ASFOUR")
    t+=1

    show_warning = len(bombs) > 0  # Active l'avertissement si au moins une bombe est présente

    if show_warning:
        warning_timer += 1
    else:
        warning_timer = 0

    if plane_active and plane is not None:
        plane.update()
        plane.draw(window)

    pygame.draw.rect(window, (50, 50, 50), settings_area)
    pygame.draw.rect(window,GOLD,recharging_area)
    font_medium = pygame.font.Font(None, 36)  # Police pour le texte "Recharging bar"
    
    ### DESINER LES SLIDERS ###
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
    
    # Dessiner le slider pour la vitesse de l'avion
    plane_speed_knob_x = slider_x + int((PLANE_SPEED / 10.0) * slider_width)  # Position initiale
    draw_slider(
        slider_x, plane_speed_slider_y, slider_width, slider_height,
        plane_speed_knob_x, (255, 165, 0), f"     Plane Speed: {PLANE_SPEED:.1f}", 
        (slider_x + slider_width + 70, plane_speed_slider_y + slider_height // 2)
    )

    ### DESINER LES BOUTTONS ###
    circle_plus_color = (173, 216, 230) if pygame.Rect(circle_plus_center[0] - 30, circle_plus_center[1] - 30, 60, 60).collidepoint(mouse_pos) else (0, 143, 8)
    circle_minus_color = (173, 216, 230) if pygame.Rect(circle_minus_center[0] - 30, circle_minus_center[1] - 30, 60, 60).collidepoint(mouse_pos) or len(boids) == 0 else (0, 143, 8)
    button_accelerate_color = (173, 216, 230) if pygame.Rect(button_accelerate_center[0] - 30, button_accelerate_center[1] - 30, 60, 60).collidepoint(mouse_pos) or BOID_SPEED >= BOID_SPEED_MAX else (0, 143, 8)
    button_decelerate_color = (173, 216, 230) if pygame.Rect(button_decelerate_center[0] - 30, button_decelerate_center[1] - 30, 60, 60).collidepoint(mouse_pos) or BOID_SPEED <= BOID_SPEED_MIN else (0, 143, 8)

    button_clear_color = (173, 216, 230) if button_clear.collidepoint(mouse_pos) or len(boids) == 0 else (0, 143, 8)
    button_pause_color = (173, 216, 230) if button_pause.collidepoint(mouse_pos) else (0, 143, 8)
    button_vision_color = (173, 216, 230) if button_vision.collidepoint(mouse_pos) else (0, 143, 8)
    button_plane_color = (173, 216, 230) if button_plane.collidepoint(mouse_pos) else (0, 143, 8)
    button_stats_color = (173, 216, 230) if button_stats.collidepoint(mouse_pos) else (0, 143, 8)
    
    circle_plus = pygame.draw.circle(window, circle_plus_color, circle_plus_center, 25)
    circle_minus = pygame.draw.circle(window, circle_minus_color, circle_minus_center, 25)
    button_accelerate = pygame.draw.circle(window, button_accelerate_color, button_accelerate_center, 25)
    button_decelerate = pygame.draw.circle(window, button_decelerate_color, button_decelerate_center, 25)
    pygame.draw.rect(window, button_clear_color, button_clear)
    pygame.draw.rect(window, button_pause_color, button_pause)
    pygame.draw.rect(window, button_vision_color, button_vision)
    pygame.draw.rect(window, button_plane_color, button_plane)
    pygame.draw.rect(window, button_stats_color, button_stats)

    label = font_petit.render(f"Boids num: {len(boids)}", True, (255, 255, 255))

    text_vision = font_petit.render("Hide" if show_vision else "Show", True, (255, 255, 255))
    text_vision_rect = text_vision.get_rect(center=button_vision_center)
    text_plane = font_petit.render("Plane", True, (255, 255, 255))
    text_plane_rect = text_plane.get_rect(center=button_plane_center)
    text_stats = font_petit.render("STATS", True, (255, 255, 255))
    text_stats_rect = text_stats.get_rect(center=button_stats_center)
    text_accelerate = font.render(">>", True, WHITE)
    text_decelerate = font.render("<<", True, WHITE)
    speed_factor_text = font_petit.render(f"Speed: x{SPEED_FACTOR:.1f}", True, (255, 255, 255))
    speed_factor_text_rect = speed_factor_text.get_rect(topleft=(WIDTH - 470, HEIGHT -20))


    window.blit(text1, text_rect_p)
    window.blit(text2, text_rect_m)
    window.blit(text3, text_rect_clear)
    window.blit(label, label_numboids_center)
    
    window.blit(text_vision, text_vision_rect)
    window.blit(text_plane, text_plane_rect)
    window.blit(text_stats, text_stats_rect)
    window.blit(text_accelerate, text_accelerate.get_rect(center=button_accelerate_center))
    window.blit(text_decelerate, text_decelerate.get_rect(center=button_decelerate_center))
    window.blit(speed_factor_text, speed_factor_text_rect)
    

    # Les events (interaction simul-utilsateur)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:  # Si une touche est pressée
            if event.key == pygame.K_ESCAPE:  # Si c'est "Échap"
                running = False
            if event.key == pygame.K_b and plane_active and plane is not None:  # Si l'utilisateur appuie sur la barre d'espace
                plane.drop_bomb()
            elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:  # Ajouter un boid
                add_boid()
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  # Supprimer un boid
                remove_boid()       
            elif event.key == pygame.K_SPACE:
                paused = not paused    
            elif event.key == pygame.K_c:
                clear()
            elif event.key == pygame.K_w and wind_mode:  # Vent vers le haut
                wind_direction = pygame.Vector2(0, -0.5) * WIND_FORCE
            elif event.key == pygame.K_a and wind_mode:  # Vent vers la gauche
                wind_direction = pygame.Vector2(-0.5, 0) * WIND_FORCE
            elif event.key == pygame.K_d and wind_mode:  # Vent vers la droite
                wind_direction = pygame.Vector2(0.5, 0) * WIND_FORCE
            elif event.key == pygame.K_s and wind_mode:  # Vent vers le bas
                wind_direction = pygame.Vector2(0, 0.5) * WIND_FORCE
            elif event.key == pygame.K_i:
                interaction_mode = not interaction_mode
                mode_message = "Mode Interaction: ON" if interaction_mode else "Mode Interaction: OFF"
                message_timer = MESSAGE_DURATION
            elif event.key == pygame.K_8:
                eight_mode = not eight_mode  # Alterne le mode
                mode_message = "Mode Lemniscate: ON" if eight_mode else "Mode Lemniscate: OFF"
                message_timer = MESSAGE_DURATION
            elif event.key == pygame.K_v:  # Activer/désactiver le mode vent
                wind_mode = not wind_mode  # Alterne l'état du mode vent
                if not wind_mode:
                    wind_direction = pygame.Vector2(0, 0)  # Réinitialiser la direction du vent
                mode_message = "Mode Vent: ON" if wind_mode else "Mode Vent: OFF"
                message_timer = MESSAGE_DURATION

             


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
            elif is_knob_clicked(plane_speed_knob_x, plane_speed_slider_y + slider_height // 2, mouse_pos):
                slider_plane_speed_active = True
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
            elif button_plane.collidepoint(event.pos):
                if plane_active:
                    plane = None
                    mode_message = "Avion détruit"
                else :
                    plane = Plane() 
                    mode_message = "Avion créé"
                plane_active = not plane_active  # Alterne entre actif et inactif
                message_timer = MESSAGE_DURATION
            elif button_stats.collidepoint(event.pos):
                stats_visible = not stats_visible
            elif button_accelerate.collidepoint(event.pos):
                if SPEED_FACTOR < 2.0:  # Limite supérieure (par exemple, x2.0)
                    SPEED_FACTOR += 0.1
                    SPEED_FACTOR = round(SPEED_FACTOR, 1)  # Assurez-vous que le facteur reste précis
            elif button_decelerate.collidepoint(event.pos):
                if SPEED_FACTOR > 0.1:  # Limite inférieure (par exemple, x0.1)
                    SPEED_FACTOR -= 0.1
                    SPEED_FACTOR = round(SPEED_FACTOR, 1)
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            slider_angle_active = False
            slider_align_active = False
            slider_cohesion_active = False
            slider_separation_active = False
            slider_plane_speed_active = False

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

        if slider_plane_speed_active and pygame.mouse.get_pressed()[0]:
            if slider_x <= mouse_pos[0] <= slider_x + slider_width:
                PLANE_SPEED = (mouse_pos[0] - slider_x) / slider_width * 10.0  # Ajustez le facteur de mise à l'échelle
                PLANE_SPEED = max(0.1, min(PLANE_SPEED, 10.0))  # Limitez la vitesse entre 0.1 et 10.0

        if plane_active and plane is not None:
            plane.velocity = plane.velocity.normalize() * PLANE_SPEED

    
    if stats_visible and stats_rect_width < stats_max_width:
        stats_rect_width += stats_toggle_speed  # Ouvrir la zone progressivement
    elif not stats_visible and stats_rect_width > 0:
        stats_rect_width -= stats_toggle_speed  # Fermer la zone progressivement

    # Met a jour l'etat des boid a chaque iteration
    for boid in boids:
            boid.apply_behaviors(boids, plane, bombs, eight_mode, (WIDTH // 2, HEIGHT // 2), 200)
            boid.update()
            boid.decharging_phase()
            boid.check_battery_color()
            boid.apply_wind()
   
            boid.draw(window)
            boid.update_charging()

    # Animer la barre des statistiques
    stats_surface = pygame.Surface((stats_rect_width, 300), pygame.SRCALPHA)
    stats_surface.fill((50, 50, 50, 150))  # Alpha à 150 pour une semi-transparence
    window.blit(stats_surface, (WIDTH - stats_rect_width+60, 10))
    stats_rect = pygame.Rect(WIDTH - stats_rect_width+ 60, 10, stats_rect_width, 300)
    if stats_rect_width > 0:  # Affiche les statistiques si la zone est visible
        stats_texts = [
            f"Boids: {len(boids)}",
            f"Bombes actives: {len(bombs)}",
            f"Avions actifs: {1 if plane_active else 0}",
            f"FPS: {int(clock.get_fps())}"
        ]
        for i, text in enumerate(stats_texts):
            stat_surface = font_petit.render(text, True, (255, 255, 255))
            window.blit(stat_surface, (WIDTH - stats_rect_width + 70, 20 + i * 30))
    
    # Animer la pause/resume
    if paused:
        #dessiner du triangle play    
        pygame.draw.polygon(window, WHITE, triangle_play)
    else:
        # Traits (Pause)
        pygame.draw.rect(window, WHITE, tirer_pause_left)
        pygame.draw.rect(window, WHITE, tirer_pause_right)        

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
            warning_image_rect = warning_image.get_rect(topleft=(200, 20))  # Position en haut à gauche
            window.blit(warning_image, warning_image_rect.topleft)

    if len(bombs) == 0:
        warning_blink_timer = 0  # Réinitialiser le timer lorsque plus de bombes

    if interaction_mode:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(window, (255, 255, 255), mouse_pos, 50, width=2)  # Cercle de rayon 50
    
    # Afficher le message temporaire si le timer est actif
    if message_timer > 0:
        display_message(window, mode_message, message_timer)
        message_timer -= 1

    # Filtrer les bombes inactives
    bombs = [bomb for bomb in bombs if bomb.is_active()]

    # Affiche le titre "Recharging bar"
    pygame.draw.rect(window, BLACK, (5, 5, 190, 30))
    text_surface = font_medium.render(" Recharging bar", True, (255, 255, 255))  # Texte blanc
    text_rect = text_surface.get_rect(center=(RECHARGING_BAR_WIDTH // 2 + 20, 20))  # Centrer le texte en haut
    window.blit(text_surface, text_rect)  # Afficher le texte sur l'écran
    
    wind_offset = (wind_offset + 2) % (WIDTH + 200)          
    draw_wind_in_area(window, wind_direction, game_area_dimension, wind_offset)        
    
    # Dessiner le radar
    draw_radar(window, boids, plane)
    draw_radar_legend(window)

    pygame.display.flip()

pygame.quit()