import pygame
import random
import math

# Configuration de la simulation
WIDTH, HEIGHT = 800, 600
NUM_BOIDS = 10
MAX_SPEED = 0.6
VITESSE_INITIAL=0.6
MAX_FORCE = 0.03
VIEW_RADIUS = 60
ALIGN_RADIUS=50 #rayon du alignement
SEPARATION_RADIUS = 10#rayon du distanciation
#colors
WHITE=(255,255,255)
BLACK =(0, 0, 0)
GOLD=(255, 215, 0)
BLUE=(0, 0, 255)
LIGHT_BLUE=(173, 216, 230)



pause=False
side_length_triangle_vitesse = (2 / 3) * 20  # Rayon donné (ajusté) 
triangle_vitesse_height = (math.sqrt(3) / 2) * side_length_triangle_vitesse  # Hauteur du triangle équilatéral
# Décalage entre les triangles du vitesse
triangle_spacing = 10  
decalage_droit = -5  # Décalage à gauche pour le triangle droit
decalage_gauche = 5  # Décalage à droite pour le triangle gauche
#longeuer hauteur du triangle play
s = 20        # Longueur des côtés du triangle play
h_triangle = (math.sqrt(3) / 2) * s #hauteur du triangle 


# Initialisation de Pygame
pygame.init()
#center/ main screen
screen_center=(WIDTH, HEIGHT)
#dimensions/zone

game_area_dimension=(0, 0, WIDTH, HEIGHT - 100)
settings_area_dimension=(200, HEIGHT - 100, WIDTH, 100)
recharging_area_dimension=(0, 0, 200, HEIGHT)
#centers/label
label_numboids_center=(WIDTH-155,HEIGHT-25)
#centers/circle buttons
circle_plus_center=(WIDTH-50,HEIGHT-60)
circle_minus_center=(WIDTH-125,HEIGHT-60)
circle_augmente_vitesse_center=(WIDTH - 340, HEIGHT - 60)
circle_diminue_vitesse_center=(WIDTH - 480, HEIGHT - 60)
#dimension/ rectangle buttons
button_clear_dimension=(WIDTH - 250, HEIGHT - 80, 80, 40)
button_pause_dimension= (WIDTH - 450, HEIGHT - 80, 80, 40)
tirer_pause_left_dimension=(WIDTH-423, HEIGHT-70, 8, 25)
tirer_pause_right_dimension=(WIDTH-405,HEIGHT-70,8,25)

#TRIANGLE POUR PARTIE AUGMENTATION/DIMINUTION DU VITESSE CHAQUE PARTIE NECESSITE 2 TRIANGLE CONSECUTIF
#les 3 point du premier triangle dans le cercle a droit(AUGMENTATION VTESSE)
triangle_vitesse_droit_1_point_1=(circle_augmente_vitesse_center[0] + side_length_triangle_vitesse / 2 -5, circle_augmente_vitesse_center[1])
triangle_vitesse_droit_1_point_2=(circle_augmente_vitesse_center[0] - side_length_triangle_vitesse / 4 -5, circle_augmente_vitesse_center[1] - triangle_vitesse_height)
triangle_vitesse_droit_1_point_3=(circle_augmente_vitesse_center[0] - side_length_triangle_vitesse / 4 -5, circle_augmente_vitesse_center[1] + triangle_vitesse_height)
#les 3 point du deuxieme triangle dans le cercle a droit(AUGMENTATION VITESSE)
triangle_vitesse_droit_2_point_1=(circle_augmente_vitesse_center[0] + side_length_triangle_vitesse / 2 + triangle_spacing  -5, circle_augmente_vitesse_center[1])
triangle_vitesse_droit_2_point_2=(circle_augmente_vitesse_center[0] - side_length_triangle_vitesse / 4 + triangle_spacing  -5, circle_augmente_vitesse_center[1] - triangle_vitesse_height)
triangle_vitesse_droit_2_point_3=(circle_augmente_vitesse_center[0] - side_length_triangle_vitesse / 4 + triangle_spacing  -5, circle_augmente_vitesse_center[1] + triangle_vitesse_height)
#les 3 point du premier triangle dans le cercle a gauche(DIMINUTION VTESSE)
triangle_vitesse_gauche_1_point_1=(circle_diminue_vitesse_center[0] - side_length_triangle_vitesse / 2 + 5, circle_diminue_vitesse_center[1])
triangle_vitesse_gauche_1_point_2=(circle_diminue_vitesse_center[0] + side_length_triangle_vitesse / 4 + 5, circle_diminue_vitesse_center[1] - triangle_vitesse_height)
triangle_vitesse_gauche_1_point_3=(circle_diminue_vitesse_center[0] + side_length_triangle_vitesse / 4 + 5, circle_diminue_vitesse_center[1] + triangle_vitesse_height)
#les 3 point du deuxieme triangle dans le cercle a gauche(DIMINUTION VTESSE)
triangle_vitesse_gauche_2_point_1=(circle_diminue_vitesse_center[0] - side_length_triangle_vitesse / 2 - triangle_spacing + 5, circle_diminue_vitesse_center[1])
triangle_vitesse_gauche_2_point_2=(circle_diminue_vitesse_center[0] + side_length_triangle_vitesse / 4 - triangle_spacing + 5, circle_diminue_vitesse_center[1] - triangle_vitesse_height)
triangle_vitesse_gauche_2_point_3=(circle_diminue_vitesse_center[0] + side_length_triangle_vitesse / 4 - triangle_spacing + 5, circle_diminue_vitesse_center[1] + triangle_vitesse_height)
#les 3 point du triangle play
triangle_play_point_1=(WIDTH - 410 + (2 * h_triangle) / 3, HEIGHT - 60)
triangle_play_point_2=(WIDTH - 410 - h_triangle / 3, HEIGHT - 60 - s / 2)
triangle_play_point_3=(WIDTH - 410 - h_triangle / 3, HEIGHT - 60 + s / 2)



#center/ rectangle buttons
button_clear_center=(WIDTH - 210, HEIGHT - 60)
#screen
window = pygame.display.set_mode(screen_center) #area pour les boids
#zone du screen
game_area = pygame.Rect(game_area_dimension)  # La zone de jeu (partie principale)
settings_area = pygame.Rect(settings_area_dimension) #la zone du modification
recharging_area=pygame.Rect(recharging_area_dimension)#la zone du charging
#rectangle buttons
button_reset = pygame.Rect(button_clear_dimension)
button_pause= pygame.Rect(button_pause_dimension)
# Rectangle gauche
tirer_pause_left = pygame.Rect(tirer_pause_left_dimension)
tirer_pause_right = pygame.Rect(tirer_pause_right_dimension)
# 2 triangle dans le cercle pour l augmentation du vitesse
# Cercle droit (augmentation de vitesse) : triangles pointant vers la droite
triangle_droite_1 = [
    triangle_vitesse_droit_1_point_1,
    triangle_vitesse_droit_1_point_2,
    triangle_vitesse_droit_1_point_3,
]
triangle_droite_2 = [
    triangle_vitesse_droit_2_point_1,
    triangle_vitesse_droit_2_point_2,
    triangle_vitesse_droit_2_point_3,
]

# 2 triangle dans le cercle pour la diminution du vitesse
# Cercle gauche (diminution de vitesse) : triangles pointant vers la gauche
triangle_gauche_1 = [
    triangle_vitesse_gauche_1_point_1,
    triangle_vitesse_gauche_1_point_2,
    triangle_vitesse_gauche_1_point_3,
]
triangle_gauche_2 = [
    triangle_vitesse_gauche_2_point_1,
    triangle_vitesse_gauche_2_point_2,
    triangle_vitesse_gauche_2_point_3,
]
#triangle play
triangle_play = [
            triangle_play_point_1,  # Sommet droit
            triangle_play_point_2,  # Sommet inférieur gauche
            triangle_play_point_3,  # Sommet supérieur gauche
        ]



#font types
font_grand = pygame.font.Font(None, 75) 
font_petit=pygame.font.Font(None,30)


#text in buttons(circles and rect) specifier le text et le couleur

text_plus=font_grand.render("+", True, WHITE)
text_moin=font_grand.render("-",True,WHITE)
text_clear=font_petit.render("Clear",True,WHITE)

#text in buttons(circles and rect) specifier centre ou le placer
text_rect_plus = text_plus.get_rect(center=circle_plus_center)
text_rect_moin = text_moin.get_rect(center=circle_minus_center)
text_rect_clear=text_clear.get_rect(center=button_clear_center)





pygame.display.set_caption("Simulation de Boids")
#button_rect = pygame.Rect(850, 600, 200, 60)

class Boid:
    def __init__(self,color=WHITE):
        #chaque boid contenant position vitesse accelaration comme etant chaque un un vecteur
        self.position = pygame.Vector2(random.uniform(200, WIDTH), random.uniform(0, HEIGHT-100))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED
        self.acceleration = pygame.Vector2(0, 0)
        self.state = "active"  # "active", "recharging"
        self.battery = 100 
        
        self.color = color  # Couleur principale (par ex. blanc)
        
    #juste pour faire call au ces 3 fonction
                
    def apply_behaviors(self, boids):
        if pause:
            return
        if self.state == "active" :
            alignment = self.align(boids)
            cohesion = self.cohere(boids)
            separation = self.separate(boids)

            # Pondération des règles
            self.acceleration += alignment 
            self.acceleration += cohesion 
            self.acceleration += separation
            
            # Réduction de la batterie de manière plus lente
             # Consommation plus lente
    
           
    #mafrud alignement tamem
    def check_color(self):
        if self.battery<=20 and self.state=="active":
            self.color=(255, 0, 0)
        elif self.battery<=100 and self.battery>=95:
            self.color=(0, 255, 0)    
        else:
            self.color=(255,255,255)    
    def align(self, boids):
        steering = pygame.Vector2(0, 0)#initialisation du vecteur 0,0
        total = 0
        diff=pygame.Vector2(0,0)
        # if self.velocity.length() !=0:
        #         vitesse_normaliser=self.velocity.normalize()
        # else:
        #     vitesse_normaliser=pygame.Vector2(1, 0)
        for other in boids:
          #  direction_vers_autre_boid=(other.position -self.position)
            distance_vers_autre_boid = self.position.distance_to(other.position)
                # Normaliser le vecteur direction vers l'autre boid
            #if direction_vers_autre_boid.length() != 0:
            #    direction_vers_autre_boid = direction_vers_autre_boid.normalize()  
            
            if other != self and SEPARATION_RADIUS < distance_vers_autre_boid < ALIGN_RADIUS:
                #direction vers autre boids
                # direction_vers_autre_boid=direction_vers_autre_boid.normalize()
                # angle = vitesse_normaliser.angle_to(direction_vers_autre_boid)
                

                # Vérification si l'angle est dans la zone de détection
               # if -180/4 <= angle <= 180/4:
                #somme du vecteur PPi
                    diff = diff+ (other.velocity)
                    total += 1  
                    
        if total > 0:
            steering = (1/total)*diff
            steering = steering.normalize() * VITESSE_INITIAL
            #juste pour negliger et limiter le vitesse
            steering = steering.normalize() * MAX_FORCE
        return steering
    #Mafrud cohere tamem
    def cohere(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        diff=pygame.Vector2(0,0)
        # if self.velocity.length() !=0:
        #     vitesse_normaliser=self.velocity.normalize()
        # else:
        #     vitesse_normaliser=pygame.Vector2(1, 0)
        for other in boids:
           # direction_vers_autre_boid=(other.position -self.position)
            distance_vers_autre_boid = self.position.distance_to(other.position)
                # Normaliser le vecteur direction vers l'autre boid
            # if direction_vers_autre_boid.length() != 0:
            #     direction_vers_autre_boid = direction_vers_autre_boid.normalize()  
            
            if other != self and ALIGN_RADIUS< distance_vers_autre_boid < VIEW_RADIUS:
                #direction vers autre boids
                #direction_vers_autre_boid=direction_vers_autre_boid.normalize()
               # angle = math.degrees(vitesse_normaliser.angle_to(direction_vers_autre_boid))
                

                # Vérification si l'angle est dans la zone de détection
                #if -180/4 <= angle <= 180/4:
                #somme du vecteur PPi
                    diff = diff+other.position 
                    total += 1
            
        #juste formule
        if total > 0:
            steering =(1/ total)*diff
            steering -= self.position
            steering = steering.normalize() * VITESSE_INITIAL
            #juste limitation pour negliger les mvt pas necessaire
            steering = steering.normalize() * MAX_FORCE
        return steering
    #mafroud separate tamem
    def separate(self, boids):
        #steering vitesse
        steering = pygame.Vector2(0, 0)
        diff=pygame.Vector2(0,0)
        total = 0
        # if self.velocity.length() !=0:
        #         vitesse_normaliser=self.velocity.normalize()
        # else:
        #     vitesse_normaliser=pygame.Vector2(1, 0)
        for other in boids:
            # direction_vers_autre_boid=(other.position -self.position)
            distance_vers_autre_boid = self.position.distance_to(other.position)
                # Normaliser le vecteur direction vers l'autre boid
            # if direction_vers_autre_boid.length() != 0:
            #     direction_vers_autre_boid = direction_vers_autre_boid.normalize()  
            
            if other != self and distance_vers_autre_boid < SEPARATION_RADIUS:
                #direction vers autre boids
                # direction_vers_autre_boid=direction_vers_autre_boid.normalize()
                # angle = math.degrees(vitesse_normaliser.angle_to(direction_vers_autre_boid))

              

                # Vérification si l'angle est dans la zone de détection
          #      if -180/4 <= angle <= 180/4:
                #somme du vecteur PPi
                    diff = diff+ (other.position - self.position)
                    total += 1      
                
        if total > 0:
            steering =(-1/total)*diff # wd 
            steering = steering.normalize() * VITESSE_INITIAL #VBUT
            #juste pour negliger et limiter le vitesse
            steering = steering.normalize() * MAX_FORCE
           # vitesse=MAX_SPEED*(steering)/steering.normalize()

        return steering

    def update(self):
    # Si en pause, on ne fait rien
        if pause:
            return
        
        # Réduire la batterie seulement si on n'est pas en pause
        base_consumption = 0.02  # Consommation normale à une vitesse de base
        self.battery -= base_consumption * MAX_SPEED

        self.velocity += self.acceleration

        # Pour conserver une vitesse maximale
        if self.velocity.length() > MAX_SPEED:
            self.velocity = self.velocity.normalize() * MAX_SPEED

        self.position += self.velocity
        self.acceleration *= 0

        # Si la batterie est vide, passer en mode "recharge"
        if self.battery <= 0:
            self.state = "recharging"
        
        # Gestion des bords (tore)
        if self.position.x > WIDTH and self.state == "active":
            self.position.x = 200
        elif self.position.x <= 200 and self.state == "active":
            self.position.x = WIDTH
        if self.position.y > HEIGHT - 100:
            self.position.y = 0
        elif self.position.y <= 0:
            self.position.y = HEIGHT - 100

    def find_empty_spot_in_recharging_area(self):
        global recharging_boids
        for y in range(20, 600, 20):
            if y not in recharging_boids:
                # Si cet emplacement est libre, on y place le boid
            
                recharging_boids[y] = boid  # Ajouter le boid à cet emplacement
                return y

        # Si aucun emplacement n'est libre
        
        return None
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
                color = (0, 255, 0)  # Vert clair
            elif self.battery <= 20 and i == 0:  # Batterie critique
                color = (255, 0, 0)  # Rouge
            else:
                color = (0, 0, 0, 0)  # Transparent

            # Calculer les dimensions du segment
            segment_rect = pygame.Rect(x + i * segment_width, top_y, segment_width, height)

            # Dessiner le segment
            pygame.draw.rect(window, color, segment_rect)


    def update_charging(self):
        global recharging_boids
        if self.state == "recharging":
            # Si le jeu n'est pas en pause, procéder à la mise à jour
            if pause == False:
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
                self.draw_recharging_rectangle(boid_y)
                self.position = pygame.Vector2(7.5, boid_y - 1)

                # Recharge plus lente si la batterie n'est pas pleine
                if self.battery < 100:
                    self.battery += 0.1  # Recharge plus lente

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

    def draw(self, screen):
        angle = math.atan2(self.velocity.y, self.velocity.x)
        point1 = self.position + pygame.Vector2(math.cos(angle), math.sin(angle)) * 8
        point2 = self.position + pygame.Vector2(math.cos(angle + 2.5), math.sin(angle + 2.5)) * 8
        point3 = self.position + pygame.Vector2(math.cos(angle - 2.5), math.sin(angle - 2.5)) * 8
        pygame.draw.polygon(screen,self.color, [point1, point2, point3])
        

# Création des boids
boids = [Boid() for _ in range(NUM_BOIDS)]
recharging_boids={}
          
# def add_boid():
#     boid = Boid()  # Cree un nouveau boid
#     boids.append(boid)  # Ajoute ce boid a la liste des boids
#     return boids
# def remove_boid():
#     if len(boids) > 0:  # Verifier si des boids existent avant de retirer
#         boids.pop()  # Retire le dernier boid de la liste
#     return boids

#fonction pour augmenter le vitesse
def augmenter_vitesse():
    global MAX_SPEED
    MAX_SPEED=MAX_SPEED+0.1
    if MAX_SPEED>=2:
        MAX_SPEED=2
#fonction pour diminuer le vitesse      
def diminuer_vitesse():
    global MAX_SPEED
    MAX_SPEED=MAX_SPEED-0.1
    if MAX_SPEED<=0.1:
        MAX_SPEED=0.1
#fonction pour ajouter les boids
def add_boid():
    if not pause:  # Ajouter un boid uniquement si la simulation n est pas en pause
        boid = Boid()  # Crée un nouveau boid
        boids.append(boid)  # Ajoute ce boid a la liste des boids
    return boids
#fonction pour enlever les boids
def remove_boid():
    if not pause and len(boids) > 0:  # Retirer un boid uniquement si la simulation n est pas en pause
        boids.pop()  # Retire le dernier boid de la liste
    return boids
#fonction qui enleve tous les boids a une click
def clear():
    for i in range(len(boids)):
        boids.pop()

# Boucle principale
running = True
while running:
    
    window.fill(BLACK)
    # Dessiner la zone du jeu et la zone des paramètres
    pygame.draw.rect(window, (0, 0, 0), game_area)
    pygame.draw.rect(window, (255, 215, 0), settings_area)
    pygame.draw.rect(window,(255,215,0),recharging_area)
    
    # Obtenir la position de la souris
    mouse_pos = pygame.mouse.get_pos()
    
    # Definir les couleurs des cercles et du bouton en fonction de la position de la souris
    circle_plus_color = LIGHT_BLUE if pygame.Rect(circle_plus_center[0] - 30, circle_plus_center[1] - 30, 60, 60).collidepoint(mouse_pos) or pause==True else BLUE
    circle_minus_color = LIGHT_BLUE if pygame.Rect(circle_minus_center[0] - 30, circle_minus_center[1] - 30, 60, 60).collidepoint(mouse_pos) or len(boids) == 0 or pause==True else BLUE
    button_reset_color = LIGHT_BLUE if button_reset.collidepoint(mouse_pos) or len(boids) == 0 else BLUE
    button_pause_color = LIGHT_BLUE if button_pause.collidepoint(mouse_pos) else BLUE
    circle_augmente_vitesse_color=LIGHT_BLUE if pygame.Rect(circle_augmente_vitesse_center[0] - 30, circle_augmente_vitesse_center[1] - 30, 60, 60).collidepoint(mouse_pos) or MAX_SPEED==2 else BLUE
    circle_diminue_vitesse_color=LIGHT_BLUE if pygame.Rect(circle_diminue_vitesse_center[0] - 30, circle_diminue_vitesse_center[1] - 30, 60, 60).collidepoint(mouse_pos) or MAX_SPEED==0.1 else BLUE
    
    # Dessiner les button cercle
    circle_plus = pygame.draw.circle(window, circle_plus_color, circle_plus_center, 30)
    circle_minus = pygame.draw.circle(window, circle_minus_color, circle_minus_center, 30)
    circle_augmente_vitesse=pygame.draw.circle(window,circle_augmente_vitesse_color ,circle_augmente_vitesse_center , 20)
    circle_diminue_vitesse=pygame.draw.circle(window,circle_diminue_vitesse_color,circle_diminue_vitesse_center, 20)
    # Dessiner les button rectangle
    pygame.draw.rect(window, button_reset_color, button_reset)
    pygame.draw.rect(window, button_pause_color, button_pause)
    #dessiner les triangle necessaire
    pygame.draw.polygon(window, WHITE, triangle_droite_1)
    pygame.draw.polygon(window, WHITE, triangle_droite_2)
    pygame.draw.polygon(window, WHITE, triangle_gauche_1)
    pygame.draw.polygon(window, WHITE, triangle_gauche_2)
    #label pour le nombre de boids
    label = font_petit.render(f"Boids num: {len(boids)}", True, WHITE)
    #pour specifier que on met le text avec sont couleur dans la posisiton convenable
    window.blit(text_plus, text_rect_plus)
    window.blit(text_moin, text_rect_moin)
    window.blit(text_clear, text_rect_clear)
    window.blit(label,label_numboids_center)
    # Dessiner le triangle ou les deux traits selon l'état de pause
    if pause:
        #dessiner du triangle play    
        pygame.draw.polygon(window, WHITE, triangle_play)
    else:
        # Traits (Pause)
        pygame.draw.rect(window, WHITE, tirer_pause_left)
        pygame.draw.rect(window, WHITE, tirer_pause_right)
    
    # Dessiner les boids et autres éléments
    for boid in boids:
        boid.check_color()
        boid.apply_behaviors(boids)
        boid.update_charging()
        boid.update()
        boid.draw(window)
    
    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if circle_minus.collidepoint(event.pos):
                remove_boid()

            elif circle_plus.collidepoint(event.pos):
                add_boid()

            elif button_reset.collidepoint(event.pos):
                clear()

            elif button_pause.collidepoint(event.pos):
                pause = not pause  # Basculer entre pause et play

            elif circle_augmente_vitesse.collidepoint(event.pos):
                augmenter_vitesse() 

            elif circle_diminue_vitesse.collidepoint(event.pos): 
                diminuer_vitesse()  

    pygame.display.flip()

pygame.quit()

