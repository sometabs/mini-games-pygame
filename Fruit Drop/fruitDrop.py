import pygame
from random import randint
import os

#Initialise game
pygame.init()

#Set display 
WINDOW_WIDTH=900
WINDOW_HEIGHT=700
display_surface=pygame.display.set_mode((WINDOW_WIDTH ,WINDOW_HEIGHT))
pygame.display.set_caption("Fruit drop")


#FPS and Clock
FPS=60
clock=pygame.time.Clock()


#Game values
PLAYER_STARTING_LIVES=3
PLAYER_VELOCITY=10
APPLE_VELOCITY=6
BANANA_VELOCITY=8
CAKE_VELOCITY=9
MELON_VELOCITY=10
STRAWBERRY_VELOCITY=11


score=0
player_lives=PLAYER_STARTING_LIVES


#Colors
WHITE=(255,255,255)
BLACK=(0,0,0)

#Fonts
font=pygame.font.SysFont("Comicsans",28)

#Text
score_text=font.render("Score: " + str(score) ,True , WHITE)
score_rect=score_text.get_rect()
score_rect.topleft=(10,10)

title_text=font.render("Fruit Drop " ,True , WHITE)
title_rect=title_text.get_rect()
title_rect.centerx=WINDOW_WIDTH//2
title_rect.y=10

lives_text=font.render("Lives "+ str(player_lives) ,True , WHITE)
lives_rect=lives_text.get_rect()
lives_rect.topright=(WINDOW_WIDTH-15 , 10)

game_over_text=font.render("GAMEOVER" , True ,WHITE)
game_over_rect=game_over_text.get_rect()
game_over_rect.center=(WINDOW_WIDTH//2 , WINDOW_HEIGHT//2)

continue_text=font.render("Press any key to continue" ,True ,WHITE)
continue_text_rect=continue_text.get_rect()
continue_text_rect.center=(WINDOW_WIDTH//2 , WINDOW_HEIGHT//2+32)

start_text=font.render("Press any key to start the game" ,True ,WHITE)
start_text_rect=start_text.get_rect()
start_text_rect.center=(WINDOW_WIDTH//2 , WINDOW_HEIGHT//2)



# Get the directory where THIS script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the images
basket_img = os.path.join(script_dir, "assets", "basket.png")
apple_img = os.path.join(script_dir, "assets", "apple.png")
banana_img = os.path.join(script_dir, "assets", "banana.png")
melon_img = os.path.join(script_dir, "assets", "melon.png")
cake_img = os.path.join(script_dir, "assets", "cake.png")
strawberry_img = os.path.join(script_dir, "assets", "strawberry.png")
bg_img = os.path.join(script_dir, "assets", "bg.png")
pause_img = os.path.join(script_dir, "assets", "pause.png")

#Images
basket=pygame.image.load(basket_img)
basket_rect=basket.get_rect()
basket_rect.y=WINDOW_HEIGHT-48
basket_rect.centerx=WINDOW_WIDTH//2

apple=pygame.image.load(apple_img)
banana=pygame.image.load(banana_img)
melon=pygame.image.load(melon_img)
strawberry=pygame.image.load(strawberry_img)
cake=pygame.image.load(cake_img)
bg=pygame.image.load(bg_img)

pause_game=pygame.image.load(pause_img)
pause_game_rect=pause_game.get_rect()
pause_game_rect.centerx=WINDOW_WIDTH//2
pause_game_rect.centery=WINDOW_HEIGHT//2-32

curr_drop=apple
curr_drop_rect=apple.get_rect()
curr_drop_rect.x=randint(0,WINDOW_WIDTH-32)
curr_drop_rect.y=70
choose_drop=0
curr_drop_speed=APPLE_VELOCITY


# Paths to the sfx
collect_sf = os.path.join(script_dir, "sounds", "collect.wav")
reduction_sf = os.path.join(script_dir, "sounds", "collect2.wav")

#Sound fx
collect=pygame.mixer.Sound(collect_sf)
score_reduction=pygame.mixer.Sound(reduction_sf)

#Main game loop
running=True
is_paused_on_command=True
first_launch=True

while running:


    for event in pygame.event.get():
        #Check if the player wants to quit
        if event.type ==pygame.QUIT:
            running=False

        #Check if the player wants to pause the game
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_paused_on_command=True


    #Basket's movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and basket_rect.right<WINDOW_WIDTH-10:
        basket_rect.x+=PLAYER_VELOCITY
    if keys[pygame.K_LEFT] and basket_rect.left>10:
        basket_rect.x-=PLAYER_VELOCITY


    #Collision
    if basket_rect.colliderect(curr_drop_rect):
        
        #Sound fx
        if curr_drop==cake:
            score_reduction.play()
            player_lives-=1
        else:
            collect.play()
        
        #Score attribution
        if 0<=choose_drop<=3:
            score+=50   
        elif 4<=choose_drop<=6:
            score+=100    
        elif 7<=choose_drop<=9:
            score-=200   
        elif 10<=choose_drop<=11:
            score+=150 
        else:
            score+=300
            

        #Random fruit and velocity attribution
        choose_drop=randint(0,12)

        if 0<=choose_drop<=3:
            curr_drop=apple
            curr_drop_speed=APPLE_VELOCITY

        elif 4<=choose_drop<=6:
            curr_drop=banana
            curr_drop_speed=BANANA_VELOCITY

        elif 7<=choose_drop<=9:
            curr_drop=cake
            curr_drop_speed=CAKE_VELOCITY

        elif 10<=choose_drop<=11:
            curr_drop=melon
            curr_drop_speed=MELON_VELOCITY

        else:
            curr_drop=strawberry
            curr_drop_speed=STRAWBERRY_VELOCITY

        curr_drop_rect.x=randint(0,WINDOW_WIDTH-32)
        curr_drop_rect.y=70




    #Fruits' movement
    if curr_drop_rect.y > WINDOW_HEIGHT:
        
        if curr_drop!=cake:
            score_reduction.play()
            player_lives-=1

            #Score deduction
            if curr_drop==apple:
                score-=50
            elif curr_drop==banana:
                score-=100
            elif curr_drop==melon:
                score-=200
            else:
                score-=300
        else:
            #Choose another fruit after the cake disappears
            choose_drop=randint(0,12)
            if 0<=choose_drop<=3:
                curr_drop=apple
            elif 4<=choose_drop<=6:
                curr_drop=banana
            elif 7<=choose_drop<=9:
                curr_drop=cake
            elif 10<=choose_drop<=11:
                curr_drop=melon
            else:
                curr_drop=strawberry

        curr_drop_rect.x=randint(0,WINDOW_WIDTH-32)
        curr_drop_rect.y=70

    else:
        curr_drop_rect.y+=curr_drop_speed
   


    #Update HUD
    score_text= font.render("Score: " + str(score) , True ,WHITE )
    lives_text= font.render("Lives: " + str(player_lives) , True ,WHITE)

    #Display
    display_surface.blit(bg,(0,0))
    #display_surface.fill(BLACK)

    #HUD
    display_surface.blit(score_text , score_rect)
    display_surface.blit(title_text , title_rect)
    display_surface.blit(lives_text , lives_rect)
    pygame.draw.line(display_surface, WHITE , (0,64) ,(WINDOW_WIDTH,64) ,2)

    #Blit assets
    display_surface.blit(basket, basket_rect)
    display_surface.blit(curr_drop, curr_drop_rect)

    #Game Over
    if player_lives==0:
        display_surface.blit(game_over_text ,game_over_rect)
        display_surface.blit(continue_text ,continue_text_rect)
        pygame.display.update()

        #Pause the game
        is_paused=True
        while is_paused:
            for event in pygame.event.get():
                #Check if the player wants to play again
                if event.type==pygame.KEYDOWN:
                    score=0
                    player_lives=PLAYER_STARTING_LIVES
                    basket_rect.centerx=WINDOW_WIDTH//2
                    basket_rect.y=WINDOW_HEIGHT-48
                    is_paused=False

                #Check if the player wants to quit
                if event.type ==pygame.QUIT:
                    is_paused=False
                    running=False


    #Pause on command
    while is_paused_on_command:
        if first_launch:
            display_surface.blit(start_text ,start_text_rect)
        else:
            display_surface.blit(pause_game ,pause_game_rect)
            display_surface.blit(continue_text ,continue_text_rect)
        
        pygame.display.update()
        for event in pygame.event.get():
            #Check if the player wants to play again
            if event.type==pygame.KEYDOWN:
                is_paused_on_command=False
                first_launch=False

            #Check if the player wants to quit
            if event.type ==pygame.QUIT:
                is_paused_on_command=False
                running=False
                



    #Update display
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
