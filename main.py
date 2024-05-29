import pygame
from pygame import mixer
from fighter import Fighter

mixer.init() #keyword to implement the Sound for the game
pygame.init() #keyword to start the pygame

#Create game window
Screen_Width = 1900
Screen_Height = 950

screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Street Fighter")


#setframerate
clock = pygame.time.Clock()
FPS = 100

#define Colours
RED = (255, 0, 0)
YELLOW = (255,255,0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PURPLE = (255, 127, 0)

#define game variables
intro_count = 5
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player score[p1, p2]
round_over = False
ROUND_OVER_COOLDOWN = 2000


#define font
count_font = pygame.font.Font("Font/Turok.ttf", 100)
vic_font = pygame.font.Font("Font/Turok.ttf", 100)
score_font  = pygame.font.Font("Font/Turok.ttf", 50)
title_font  = pygame.font.Font("Font/Act_Of_Rejection.ttf", 50)


#function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#load background image
bg_image = pygame.image.load("Images/Bg.jpg").convert_alpha()
#function for inserting the image
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (Screen_Width, Screen_Height))
    screen.blit(scaled_bg, (0,0))


#function for drawing healthbars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, BLUE, (x, y, 512, 50))
    pygame.draw.rect(screen, RED,(x, y, 506, 45))
    pygame.draw.rect(screen, YELLOW, (x, y, 500*ratio, 40))

title_screen_shown = False
def show_title_screen(screen):
    title_b = pygame.image.load("Images/Title_bg.png").convert_alpha()
    scaled_title_bg = pygame.transform.scale(title_b, (Screen_Width, Screen_Height))
    title_name = pygame.image.load("Images/Title_name.png").convert_alpha()
    scaled_title_name = pygame.transform.scale(title_name, (Screen_Width, Screen_Height/2 * 1.5))

    running = True
    while running:
        clock.tick(FPS)
        # draw background
        screen.blit(scaled_title_bg, (0, 0))
        screen.blit(scaled_title_name, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()#program will terminate
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer_music.stop()
                    pygame.mixer.music.load("Music/street-fighter.mp3")
                    pygame.mixer.music.set_volume(0.95)
                    pygame.mixer.music.play(-1, 0.0, 1000)

                    running = False

        # Display the title screen
        #escreen.fill((0, 0, 0))  # Clear the screen
        #title_font = pygame.font.Font("Font/Act_Of_Rejection.ttf", 250)
        #title_text = title_font.render("STREET FIGHTER", True, PURPLE)
        #title_rect = title_text.get_rect(center=(Screen_Width / 2, Screen_Height / 2))
        message_font = pygame.font.Font("Font/Act_Of_Rejection.ttf", 75)
        message_text = message_font.render("PRESS SPACE TO START",True, BLUE)
        message_rect = message_text.get_rect(center=(Screen_Width / 2, Screen_Height - 100  ))
        #screen.blit(title_text, title_rect)
        screen.blit(message_text, message_rect)
        pygame.display.flip()








#define fighter variables
WARRIOR_SIZE = 200
WARRIOR_SCALE = 7
WARRIOR_OFFSET = [70, 107]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 126
WIZARD_SCALE = 9
WIZARD_OFFSET = [35, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load sounds
pygame.mixer_music.load("Music/guile-stage.mp3")
pygame.mixer_music.set_volume(0.95)
pygame.mixer_music.play(-1, 50, 100)
katana_fx= pygame.mixer.Sound("Music/Samurai.wav")
katana_fx.set_volume(0.75)
sword_fx= pygame.mixer.Sound("Music/Villan.wav")
sword_fx.set_volume(0.75)




#load sprite sheets
warrrior_sheets = pygame.image.load("Images/Villan.png").convert_alpha()
wizard_sheets = pygame.image.load("Images/HERO.png").convert_alpha()

#find no. of steps / frames
WARRIOR_ANIMATION_STEPS = [4, 8, 4, 4, 4, 3, 7]
WIZARD_ANIMATION_STEPS = [10, 8, 6, 6, 7, 3, 11]


#creating the Fighters
fighter_1 = Fighter(1, 10, 500, False, WARRIOR_DATA, warrrior_sheets, WARRIOR_ANIMATION_STEPS, katana_fx)
fighter_2 = Fighter(2, 1500, 500,True, WIZARD_DATA, wizard_sheets, WIZARD_ANIMATION_STEPS, sword_fx)
run = True
# game loop
while run:
    clock.tick(FPS)
    # draw background
    draw_bg()
    if not title_screen_shown:
        show_title_screen(screen)
        title_screen_shown = True


    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 1370, 20)
    draw_text("Player_1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("Player_2: " + str(score[1]), score_font, RED, 1370, 60)

     #update count
    if intro_count <= 0:
        fighter_1.move(Screen_Width, Screen_Height, screen, fighter_2, round_over)
        fighter_2.move(Screen_Width, Screen_Height, screen, fighter_1, round_over)
    else:
        #display count timer
        draw_text(str(intro_count), count_font, RED, Screen_Width / 2, Screen_Height / 2)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
                  intro_count -=1
                  last_count_update = pygame.time.get_ticks()
    # update fighters
    fighter_1.update()
    fighter_2.update()

    #drawing the fighter
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                vic = "Player_2 has Won"
                if score[1] >= 3:
                    pygame.quit()
                    quit()
        elif fighter_2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                vic = "Player_1 has Won"
                if score[0] >= 3:
                    pygame.quit()
                    quit()
    else:
            draw_text(vic, vic_font, YELLOW, Screen_Width / 3, Screen_Height / 2)
            if pygame.time.get_ticks() - round_over_time>ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 5
                # creating the Fighters
                fighter_1 = Fighter(1, 10, 500, False, WARRIOR_DATA, warrrior_sheets, WARRIOR_ANIMATION_STEPS, katana_fx)
                fighter_2 = Fighter(2, 1500, 500, True, WIZARD_DATA, wizard_sheets, WIZARD_ANIMATION_STEPS, sword_fx)

    #0event handler
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


    #update diaplay()
    pygame.display.update()
#exiting pygame
pygame.quit()

