import pygame
import math
import time
from random import randint

pygame.init()
pygame.mixer.init()
# Resolution
width, height = 1080, 720
screen = pygame.display.set_mode((width, height))
background = pygame.image.load('assets/background/city-over-water-at-sunset-background.jpg').convert()


level_song = pygame.mixer.Sound('assets/music/Level.mp3')
level_song.set_volume(0.1)
level_song.play(-1)
ow = pygame.mixer.Sound('assets/sfx/ow.wav')
jump = pygame.mixer.Sound('assets/sfx/jump.wav')
jump.set_volume(0.1)
song_playing = False


# Objects
class Player:
    # surf = pygame.image.load('assets/player/slime_player.png').convert_alpha()
    surf = pygame.surface.Surface((30,40))
    rect = surf.get_rect(bottomleft=(10, height-30))

    move_left = False
    move_right = False
    gravity = 0

    def player_movement(self, keys):

        # left/right control logic
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.move_right = True
        else:
            self.move_right = False

        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.move_left = True
        else:
            self.move_left = False

        if self.move_right:
            if self.rect.right < width:
                self.rect.right += 10

        elif self.move_left:
            if self.rect.left > 0:
                self.rect.left -= 10

        # jump physics
        if keys[pygame.K_SPACE]:
            if self.rect.bottom == ground.rect.top:
                jump.play()
                self.gravity = -20
            for block in block_list:
                if self.rect.bottom == block[1].top and (self.rect.left <= block[1].right and self.rect.right >= block[1].left):
                    print(self.rect.bottom)
                    jump.play()
                    self.gravity = -20

        self.gravity += 1
        self.rect.bottom += self.gravity

        if self.gravity >= 0:
            if self.rect.colliderect(ground.rect):
                self.gravity = 0
                self.rect.bottom = ground.rect.top
            for block in block_list:
                if self.rect.colliderect(block[1]) and self.rect.bottom >= block[1].top:
                    self.gravity = 0
                    self.rect.bottom = block[1].top


class Enemy:
    surf = pygame.surface.Surface((50,50))
    surf.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
    rect = surf.get_rect(bottomright=(710, height-30))

    move_left = True
    move_right = False

    def enemy_movement(self):
        if self.rect.left >= 0 and self.move_left:
            self.rect.left -= 5
            if round_score > 150:
                self.rect.left -= 3
            if round_score > 300:
                self.rect.left -= 3
            if round_score > 600:
                self.rect.left -= 3
            if round_score > 1000:
                self.rect.left -= 4
            if round_score > 1500:
                self.rect.left -= 4
            if round_score > 2000:
                self.rect.left -= 5

        else:
            self.move_left = False
            self.move_right = True

        if self.rect.right <= width and self.move_right:
            self.rect.right += 5
            if round_score > 150:
                self.rect.right += 3
            if round_score > 300:
                self.rect.right += 3
            if round_score > 600:
                self.rect.right += 3
            if round_score > 1000:
                self.rect.right += 4
            if round_score > 1500:
                self.rect.right += 4
            if round_score > 2000:
                self.rect.right += 5

        else:
            self.move_left = True
            self.move_right = False


class Ground:
    surf = pygame.surface.Surface((width, 70))
    rect = surf.get_rect(midtop=(width/2, height-30))


# QoL functions
def truncate_to_decimals(number, decimals=0):
    if not isinstance(decimals, int):
        raise TypeError("decimals places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimals must be greater than or equal to 0")
    if decimals == 0:
        return math.trunc(number)
    return math.trunc(number * 10.0 ** decimals) / 10.0 ** decimals


def get_FPS():
    font = pygame.font.SysFont('agencyfb', 20)
    fps_surf = font.render('FPS: ' + str(truncate_to_decimals(clock.get_fps(), decimals=2)), True, 'White')
    fps_rect = fps_surf.get_rect(topleft=(20, 20))
    screen.blit(fps_surf, fps_rect)


def draw_text(message, size, color, x, y):
    font = pygame.font.SysFont('agencyfb', size)
    font_surf = font.render(str(message), True, color)
    font_rect = font_surf.get_rect(center=(x, y))
    screen.blit(font_surf,font_rect)


def draw_background():
    screen.fill((48,48,48))
    # surf = background
    # surf = pygame.transform.scale(surf,(width+5,height))
    # rect = surf.get_rect(center=(width/2,height/2))
    # screen.blit(surf, rect)


def play_song(song):
    global song_playing

    if not song_playing:
        song.set_volume(0.1)
        song.play(-1)
        song_playing = True


def stop_song(song):
    global song_playing

    if song_playing:
        song.stop()
        song_playing = False


def generate_block():
    block = pygame.surface.Surface((randint(50, 200), 20))
    block.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
    block_rect = block.get_rect(midleft=(-200, (randint(200, height-150))))
    block_list.append((block, block_rect))

def draw_blocks():
    # draw blocks
    for block in block_list:
        block[1].x += 2
        if block[1].x > width + 500:
            block_list.remove(block)
        else:
            if round_score > 150:
                block[1].x += 1
            if round_score > 300:
                block[1].x += 1
            if round_score > 600:
                block[1].x += 1
            if round_score > 1000:
                block[1].x += 2
            if round_score > 1500:
                block[1].x += 2
            if round_score > 2000:
                block[1].x += 3
            screen.blit(block[0], block[1])


# Game variables (not all variables are in use yet)
running = True
start_screen = True
game_over = False

clock = pygame.time.Clock()
running_time = 0
round_score = 0
top_score = 0

block_timer = pygame.USEREVENT+1
pygame.time.set_timer(block_timer,randint(1750,2000))
block_list = []

ground = Ground()
player = Player()
enemy = Enemy()
pygame.Surface.fill(ground.surf, (36,36,36))
pygame.Surface.fill(enemy.surf, 'red')
pygame.Surface.fill(player.surf, 'blue')

print("------------------------------------------------------")
print("Use A and D keys to move left and right")
print("Use space to jump")

while running:
    
    # all keys pressed this frame
    playerInput = pygame.key.get_pressed()
    
    # main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if start_screen and event.type == pygame.KEYDOWN:
            time.sleep(0.5)
            start_screen = False
        if game_over and event.type == pygame.KEYDOWN:
            player.rect.x = 10
            enemy.rect.x = 710
            time.sleep(0.5)  # prevents accidental screen skip from key mashing
            game_over = False
            running_time = pygame.time.get_ticks()
        if not game_over and not start_screen and event.type == block_timer:
            generate_block()

    if start_screen:
        draw_background()
        draw_text("Dodge and Weave", 80, 'Black', width/2+5, height/2-25)
        draw_text("Dodge and Weave", 80, 'White', width/2, height/2-30)
        draw_text("Use A and D to move left and right, and Space to jump.", 20, 'white', width/2, height/2+55)
        draw_text("Earn points by staying alive and not running into enemies.", 20, 'white', width/2, height/2+85)
        draw_text("Press any key to start", 30, 'white', width/2, height-40)

    # run main game
    if not game_over and not start_screen:

        # Tracks the score
        round_score = truncate_to_decimals((pygame.time.get_ticks() - running_time)/100, 0)
        # Adds high score
        if round_score > top_score:
            top_score = round_score

        # player movement, taken out of event loop for speed
        player.player_movement(playerInput)
        enemy.enemy_movement()

        # draw screens
        draw_background()
        get_FPS() # draws FPS on screen
        draw_text(str(round_score), 40, 'Red', width/2, 50)
        draw_text("Cool game bro", 60, 'white', width/2, height/2)
        draw_blocks()
        screen.blit(ground.surf, ground.rect)
        screen.blit(player.surf, player.rect)
        screen.blit(enemy.surf, enemy.rect)


        if player.rect.colliderect(enemy.rect):
            ow.play()
            game_over = True

    #run end screen
    if game_over:
        pygame.Surface.fill(screen, 'Black')
        font = pygame.font.SysFont('agencyfb', 100)
        draw_text('GAME OVER', 100, 'white', width/2, height/2-30)
        draw_text(f"Top score: {top_score}", 30, "white", width/2, height/2+40)
        draw_text(f"Your score: {round_score}", 30, "red", width / 2, height / 2 + 75)
        draw_text("Press any key to restart", 50, "white", width/2, height-60)


    # update screen
    pygame.display.update()
    clock.tick(60)
