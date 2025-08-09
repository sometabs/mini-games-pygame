import pygame 
from random import randint
import os

#Initialise pygame
pygame.init()


#Set display
WINDOW_WIDTH=1000
WINDOW_HEIGHT=600
display_surface=pygame.display.set_mode((WINDOW_WIDTH ,WINDOW_HEIGHT))

pygame.display.set_caption("Pong")
clock=pygame.time.Clock()


#Game values
FPS=40

PADDLES_WIDTH=10
PADDLES_HEIGHT=100

BALL_RADIUS=8

score_right_paddle=0
score_left_paddle=0

ball_velocity=10
ball_x=WINDOW_WIDTH//2
ball_y=WINDOW_HEIGHT//2
ball_dir=[ball_velocity,0]

right_paddle_y=WINDOW_HEIGHT//2-50
left_paddle_y=WINDOW_HEIGHT//2-50

#Font
font = pygame.font.SysFont('comicsansms', 20)

# Get the directory where THIS script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

score_sf = os.path.join(script_dir, "score.mp3")
paddle_sf = os.path.join(script_dir, "paddle.mp3")
#Sound fx
score_sound=pygame.mixer.Sound(score_sf)
paddle_sound=pygame.mixer.Sound(paddle_sf)

#Colors
WHITE = (255, 255, 255)
BLACK=(0, 0, 0)
RED = (255, 0, 0)

#Text
score_text_right_paddle=font.render(str(score_right_paddle) ,True , WHITE ,BLACK)
score_rect_right_paddle=score_text_right_paddle.get_rect()
score_rect_right_paddle.topright=((3*WINDOW_WIDTH)//4 ,10)


score_text_left_paddle=font.render(str(score_left_paddle) ,True , WHITE ,BLACK)
score_rect_left_paddle=score_text_left_paddle.get_rect()
score_rect_left_paddle.topleft=(WINDOW_WIDTH//4 ,10)


#Images
rigth_paddle_coord=(WINDOW_WIDTH-20 ,WINDOW_HEIGHT//2-50 , PADDLES_WIDTH ,PADDLES_HEIGHT )
rigth_paddle_rect=pygame.draw.rect(display_surface , WHITE , rigth_paddle_coord)


left_paddle_coord=(10 , WINDOW_HEIGHT//2-50 ,PADDLES_WIDTH, PADDLES_HEIGHT )
left_paddle_rect=pygame.draw.rect(display_surface , WHITE , left_paddle_coord)

line_coord=(WINDOW_WIDTH//2 , 0 , 1 , WINDOW_HEIGHT)
line_rect=pygame.draw.rect(display_surface , WHITE , line_coord)


ball_coord=(WINDOW_WIDTH//2 , WINDOW_HEIGHT//2 )
ball_rect=pygame.draw.circle(display_surface ,RED ,ball_coord ,BALL_RADIUS)

#Collided one and two are written to avoid double collision with the same paddle
collided_one=False
collided_two=False

#Main game loop
running=True
while running:

    for event in pygame.event.get():
        #Check if the user wants to quit
        if event.type==pygame.QUIT:
            running=False

    #Paddles' movements
    keys = pygame.key.get_pressed()
    #Paddle one
    if keys[pygame.K_UP]:
        if right_paddle_y>10:
            right_paddle_y-=20
    if keys[pygame.K_DOWN]:
        if right_paddle_y<WINDOW_HEIGHT-PADDLES_HEIGHT-10:
            right_paddle_y+=20

    #Paddle two
    if keys[pygame.K_z]:
        if left_paddle_y>10:
            left_paddle_y-=20
    if keys[pygame.K_s]:
        if left_paddle_y<WINDOW_HEIGHT-PADDLES_HEIGHT-10:
            left_paddle_y+=20
    

    #Background color
    display_surface.fill(BLACK)


    #Update HUD
    score_text_player_one=font.render(str(score_right_paddle) ,True , WHITE ,BLACK)
    score_text_player_two=font.render(str(score_left_paddle) ,True , WHITE ,BLACK)


    #HUD
    display_surface.blit(score_text_player_two , score_rect_left_paddle)
    display_surface.blit(score_text_player_one , score_rect_right_paddle)

    
    #Draw ball
    ball_coord=(ball_x , ball_y)
    ball_rect=pygame.draw.circle(display_surface ,RED ,ball_coord ,BALL_RADIUS)

    #Collision rigth paddle with the ball
    if ball_rect.colliderect(rigth_paddle_rect) and collided_one==False:

        paddle_sound.play()
        random_y_direction=randint(0,2)
        ball_velocity=randint(10,15)
        
        ball_dir[0]=-1*ball_velocity-3
        if random_y_direction==0:
            ball_dir[1]=-1*ball_velocity
        elif random_y_direction==1:
            ball_dir[1]=1*ball_velocity
        else:
            ball_dir[1]=0
        
        collided_one=True
        collided_two=False
    
    #Collision left paddle with the ball
    if ball_rect.colliderect(left_paddle_rect) and collided_two==False:

        paddle_sound.play()
        random_y_direction=randint(0,2)
        ball_velocity=randint(10,15)
        
        ball_dir[0]=1*ball_velocity+3
        if random_y_direction==0:
            ball_dir[1]=-1 *ball_velocity
        elif random_y_direction==1:
            ball_dir[1]=1*ball_velocity
        else:
            ball_dir[1]=0
            
        collided_two=True
        collided_one=False


    #Ball behavior
    ball_x+=ball_dir[0]
    ball_y+=ball_dir[1]


    #Wall collision
    if ball_rect.top-BALL_RADIUS<0 :
        ball_dir[1]=5
    if ball_rect.bottom+BALL_RADIUS >WINDOW_HEIGHT:
        ball_dir[1]=-5

    #Update score
    if ball_rect.left < 0 :
        score_right_paddle+=1
        ball_x=WINDOW_WIDTH//2
        ball_y=WINDOW_HEIGHT//2
        ball_dir=[-7 ,0]
        score_sound.play()

    if ball_rect.right > WINDOW_WIDTH:
        score_left_paddle+=1
        ball_x=WINDOW_WIDTH//2
        ball_y=WINDOW_HEIGHT//2
        ball_dir=[7 ,0]
        score_sound.play()

    
    #Update paddles' positions
    rigth_paddle_coord=(WINDOW_WIDTH-20 ,right_paddle_y ,PADDLES_WIDTH , PADDLES_HEIGHT)
    rigth_paddle_rect=pygame.draw.rect(display_surface , WHITE , rigth_paddle_coord)

    left_paddle_coord=(10 , left_paddle_y ,PADDLES_WIDTH, PADDLES_HEIGHT )
    left_paddle_rect=pygame.draw.rect(display_surface , WHITE , left_paddle_coord)

    #Draw line
    line_rect=pygame.draw.rect(display_surface , WHITE , line_coord)

    
    
    pygame.display.update()
    clock.tick(FPS)

#End game      
pygame.quit()

