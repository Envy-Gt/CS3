import pygame
import random
import csv
import time 
import os
import serial  # Module pour la communication série avec Arduino

# Configuration du port série


# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Chargement et initialisation de la musique
pygame.mixer.music.load("N'to - Croche.mp3")  # Charger la musique de fond
pygame.mixer.music.set_volume(0.3)  # Régler le volume de la musique

# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # Sol
RED = (255, 0, 0)    # Plafond

# Dimensions des bandes (plafond et sol)
band_height = 50  # Hauteur des bandes du plafond et du sol

# Dimensions du joueur, des ennemis et des icônes
player_width = 40
player_height = 40
enemy_width = 40
enemy_height = 40
icon_width = 30
icon_height = 30
jump_force = -25

# Variables pour le suivi du jeu et des tentatives
player_name = "Joueur"  # Pseudo du joueur à demander dans la vraie implémentation
attempt_number = 0     # Numéro de la tentative, à incrémenter pour chaque partie
jumps = 0               # Nombre de sauts dans chaque partie
start_time = 0   

# Chargement et redimensionnement des images
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (player_width, player_height))
player_image_flipped = pygame.transform.rotate(player_image, 180)

enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))

# Créer une version retournée de l'image de l'ennemi
enemy_image_flipped = pygame.transform.rotate(enemy_image, 180)

icon_image = pygame.image.load("icon.png")
icon_image = pygame.transform.scale(icon_image, (icon_width, icon_height))

# Charger les textures pour les bandes du plafond et du sol
top_band_image = pygame.image.load("bande.png")
top_band_image = pygame.transform.scale(top_band_image, (screen_width, band_height))

bottom_band_image = pygame.image.load("bande.png")
bottom_band_image = pygame.transform.scale(bottom_band_image, (screen_width, band_height))

# Initialisation des variables pour le fond d'écran
background_x1 = 0
background_x2 = screen_width
background_speed = 2

# Initialisation des variables pour les bandes
top_band_x1 = 0
top_band_x2 = screen_width
bottom_band_x1 = 0
bottom_band_x2 = screen_width

# Initialisation des variables de jeu
scoreboard = []

icon_velocity = 4

def reset_game():
    global player_x, player_y, player_velocity_y, is_jumping, is_at_top, enemies, icons, icon_velocity, score, game_state, enemy_velocity, player_name, name_input_active, background_speed, top_band_x1, top_band_x2, bottom_band_x1, bottom_band_x2,jumps, start_time, attempt_number
    attempt_number +=1
    # Position et état du joueur
    player_x = screen_width // 4 - player_width // 2
    player_y = screen_height - player_height - band_height
    player_velocity_y = 0
    is_jumping = False
    is_at_top = False
    jumps = 0  # Réinitialiser les sauts
   
   
    # Démarrer le chronomètre
    start_time = time.time()  # Heure de début de la partie

    # Réinitialiser les ennemis et les icônes
    enemies.clear()
    icons.clear()
   
    generate_enemies()
    generate_icon()
    
    # Score et état du jeu
    score = 0
    game_state = 'start'
    player_name = ""
    name_input_active = False
   

    # Initialiser la vitesse des ennemis et du fond
    enemy_velocity = 5
    background_speed = 4  # Initial speed of the background

    # Réinitialiser les positions des bandes
    top_band_x1 = 0
    top_band_x2 = screen_width
    bottom_band_x1 = 0
    bottom_band_x2 = screen_width


def save_player_data(player_name, attempt_number, score, duration):
    # Créer le nom du fichier CSV basé sur le pseudo du joueur
    file_name = f"{player_name}.csv"
    
    # Vérifier si le fichier existe déjà
    file_exists = os.path.isfile(file_name)
    
    # Ouvrir le fichier en mode ajout (append) pour ajouter les nouvelles données
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Écrire les en-têtes si le fichier est créé pour la première fois
        if not file_exists: 
            attempt_number=1
            writer.writerow(["Attempt Number", "Score", "Duration (seconds)"])
        writer.writerow([attempt_number, score, round(duration, 2)])
        # Écrire les données de la nouvelle tentative
        
    
    print(f"Données sauvegardées pour {player_name} dans {file_name}.")


# Générer un ennemi à une position aléatoire
def generate_enemies():
    enemy1_x = random.randint(screen_width, screen_width + 500)
    enemy1_y = random.choice([band_height, screen_height - band_height - enemy_height])
    enemy2_x = random.randint(screen_width, screen_width + 500)
    while (abs(enemy1_x-enemy2_x) < 200):
        enemy2_x = random.randint(screen_width, screen_width + 500)
    enemy2_y = random.choice([band_height, screen_height - band_height - enemy_height])
  
    enemies.append([enemy1_x, enemy1_y])
    enemies.append([enemy2_x, enemy2_y])

# Générer une icône à une position aléatoire
def generate_icon():
    icon_x = random.randint(screen_width, screen_width + 200)
    icon_y = random.randint(band_height + 30, screen_height - band_height - 30)
    icons.append([icon_x, icon_y])

# Vérifier si le joueur entre en collision avec un objet
def check_collision(player_rect, rects):
    for rect in rects:
        if player_rect.colliderect(rect):
            return rect
    return None

# Augmenter la vitesse des ennemis et du fond d'écran en fonction du score
def update_game_speeds():
    global enemy_velocity, background_speed, icon_velocity
    # Les ennemis et le fond vont accélérer à mesure que le score augmente
    enemy_velocity = 4 * score / 100 + 8  # Ajuste la vitesse des ennemis
    background_speed = 4 + 4*score / 100  # Ajuste la vitesse du fond
    icon_velocity =  4 + 4*score / 100 

# Initialiser les listes d'ennemis et d'icônes globalement
enemies = []
icons = []

# Initialiser le jeu au départ
reset_game()

# Boucle principale
running = True
while running:

   
    # Si le jeu est en mode "playing" ou "game_over", faire défiler le fond
    if game_state == 'playing':
          
        # Déplacer le fond
        background_x1 -= background_speed
        background_x2 -= background_speed

        # Réinitialiser la position si une des images sort de l'écran
        if background_x1 <= -screen_width:
            background_x1 = screen_width
        if background_x2 <= -screen_width:
            background_x2 = screen_width

        # Déplacer les bandes
        top_band_x1 -= background_speed
        top_band_x2 -= background_speed
        bottom_band_x1 -= background_speed
        bottom_band_x2 -= background_speed

        # Réinitialiser la position des bandes si elles sortent de l'écran
        if top_band_x1 <= -screen_width:
            top_band_x1 = screen_width
        if top_band_x2 <= -screen_width:
            top_band_x2 = screen_width
        if bottom_band_x1 <= -screen_width:
            bottom_band_x1 = screen_width
        if bottom_band_x2 <= -screen_width:
            bottom_band_x2 = screen_width

        # Afficher les deux images de fond d'écran
        screen.blit(background_image, (background_x1, 0))
        screen.blit(background_image, (background_x2, 0))

        # Afficher les bandes du plafond et du sol
        screen.blit(top_band_image, (top_band_x1, 0))
        screen.blit(top_band_image, (top_band_x2, 0))
        screen.blit(bottom_band_image, (bottom_band_x1, screen_height - band_height))
        screen.blit(bottom_band_image, (bottom_band_x2, screen_height - band_height))
    else:
        # Arrêter le fond lors de l'écran "game_over"
        screen.blit(background_image, (0, 0))

        # Arrêter la musique en cours et la redémarrer
        pygame.mixer.music.play(-1, 0.0)  # Relance la musique en boucle

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == 'start' and event.key == pygame.K_RETURN:
                game_state = 'playing'
            elif game_state == 'playing' and event.key == pygame.K_SPACE:
                if not is_jumping and not is_at_top:
                    player_velocity_y = jump_force
                    is_jumping = True
                    player_rect = screen.blit(player_image, (player_x, player_y))
                   
                elif is_at_top:
                    player_velocity_y = -jump_force
                    is_jumping = True
                    is_at_top = False
                    
                    
            elif game_state == 'game_over':
                # Sauvegarder les informations de la partie
                
                if name_input_active:
                    if event.key == pygame.K_RETURN:
                        if player_name:
                            scoreboard.append((player_name, score))
                            scoreboard.sort(key=lambda x: x[1], reverse=True)
                            game_state = 'start'
                           # Calculer la durée de la partie en secondes
                            duration = time.time() - start_time
                            
                            save_player_data(player_name, attempt_number, score, duration)

                            # Réinitialiser pour une nouvelle tentative
                            
                            reset_game()
                            
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
                elif event.key == pygame.K_KP_ENTER:
                     # Calculer la durée de la partie en secondes
                        duration = time.time() - start_time
                        
                        save_player_data(player_name, attempt_number, score, duration)

                        # Réinitialiser pour une nouvelle tentative
                        reset_game()

                


    if game_state == 'start':
        # Écran d'accueil avec tableau des scores
        font = pygame.font.SysFont(None, 40)
        start_text = font.render("Appuyez sur Entrée pour commencer", True, (255, 0, 0))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 6))
        
        # Afficher le tableau des scores
        font = pygame.font.SysFont(None, 30)
        title_text = font.render("Tableau des scores:", True, (255, 255, 255))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 3))
        for i, (name, player_score) in enumerate(scoreboard[:5]):
            score_text = font.render(f"{i+1}. {name} - {player_score}", True, (255, 255, 255))
            screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2  + i * 30))

        # Afficher les bandes et le joueur sur l'écran d'accueil
        screen.blit(top_band_image, (0, 0))
        screen.blit(bottom_band_image, (0, screen_height - band_height))
        player_rect = screen.blit(player_image, (player_x, player_y))

    elif game_state == 'playing':
        # Afficher les bandes du plafond et du sol avec textures
        screen.blit(top_band_image, (top_band_x1, 0))
        screen.blit(top_band_image, (top_band_x2, 0))
        screen.blit(bottom_band_image, (bottom_band_x1, screen_height - band_height))
        screen.blit(bottom_band_image, (bottom_band_x2, screen_height - band_height))

        # Afficher le score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Mouvement vertical du joueur
        if is_jumping:
            player_y += player_velocity_y
           

        # Détection des collisions avec le sol et le plafond
        if player_y >= screen_height - player_height - band_height:
            player_y = screen_height - player_height - band_height
            is_jumping = False
        elif player_y <= band_height:
            player_y = band_height
            is_jumping = False
            is_at_top = True

        # Afficher le joueur
        player_rect = screen.blit(player_image, (player_x, player_y))

        # Afficher les ennemis
        enemy_rects = []
        for enemy in enemies:
            enemy[0] -= enemy_velocity
            if enemy[0] < -enemy_width:
                enemy[0] = screen_width + random.randint(50, 200)
                enemy[1] = random.choice([band_height, screen_height - band_height - enemy_height])
            
            # Vérifier si l'ennemi est sur la bande supérieure et choisir l'image appropriée
            if enemy[1] == band_height:
                enemy_rect = screen.blit(enemy_image_flipped, (enemy[0], enemy[1]))
            else:
                enemy_rect = screen.blit(enemy_image, (enemy[0], enemy[1]))
            
            enemy_rects.append(enemy_rect)

        # Afficher les icônes
        icon_rects = []
        for icon in icons:
            icon[0] -= icon_velocity
            if icon[0] < -icon_width:
                icon[0] = screen_width + random.randint(50, 200)
                icon[1] = random.randint(band_height + 30, screen_height - band_height - 30)
            icon_rect = screen.blit(icon_image, (icon[0], icon[1]))
            icon_rects.append(icon_rect)

        # Vérifier les collisions entre le joueur et les ennemis
        collided_enemy = check_collision(player_rect, enemy_rects)
        if collided_enemy:
            
            game_state = 'game_over'
            name_input_active = True
           
        # Vérifier les collisions entre le joueur et les icônes
        for i, icon in enumerate(icons):
            icon_rect = pygame.Rect(icon[0], icon[1], icon_width, icon_height)
            if player_rect.colliderect(icon_rect):
                icons.pop(i)  # Remove the icon at the matched index
                generate_icon()  # Generate a new icon
                score += 10
                break  # Stop after finding and removing the matched icon


        # Mettre à jour la vitesse des ennemis et du fond en fonction du score
        update_game_speeds()

    elif game_state == 'game_over':
        # Afficher le message de fin de jeu
        font = pygame.font.SysFont(None, 55)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 60))
        
        if name_input_active:
            font = pygame.font.SysFont(None, 36)
            name_text = font.render(f"Votre nom: {player_name}", True, (255, 255, 255))
            screen.blit(name_text, (screen_width // 2 - name_text.get_width() // 2, screen_height // 2 + 20))
            instruction_text = font.render("Appuyez sur Entrée pour valider", True, (255, 255, 255))
            screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, screen_height // 2 + 60))
        else:
            restart_text = font.render("Appuyez sur R pour redémarrer", True, (255, 255, 255))
            screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2))

        # Afficher les bandes du plafond et du sol pendant "game over"
        screen.blit(top_band_image, (0, 0))
        screen.blit(bottom_band_image, (0, screen_height - band_height))
        

    # Mettre à jour l'écran
    pygame.display.flip()
    pygame.time.delay(15)

pygame.quit()
