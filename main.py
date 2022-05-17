import pygame
import random

# constants
from pygame.event import Event

black = (0, 0, 0)
white = (255, 255, 255)
robot_color = white

size = 60
height = 1000
width = 1200

# distance per second
speed = 500
frame_cap = 120
clock = pygame.time.Clock()

# init stuff
pygame.init()
pygame.font.init()
pygame.display.set_caption('Weird Stuff')
screen = pygame.display.set_mode((width, height))

# variables
game_is_running = True

# possible game modes: 'MANUAL', 'SQUARE', 'Spiral' and 'RANDOM'
game_mode = 'SQUARE'


####
def handle_close_events(events: list[Event]):
    global game_is_running
    for event in events:
        if event.type == pygame.QUIT:
            game_is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_is_running = False


# drawing stuff
def draw_robot(robot):
    pygame.draw.circle(screen, robot_color, (robot[0] + size / 2, robot[1] + size / 2), size / 2)


def draw(robot):
    screen.fill(black)
    draw_robot(robot)
    pygame.display.update()


# other stuff
def fix_robot_pos(robot):
    if robot[0] < 0:
        robot[0] = 0
    if robot[0] > width - size:
        robot[0] = width - size
    if robot[1] < 0:
        robot[1] = 0
    if robot[1] > height - size:
        robot[1] = height - size


def init_game_cycle():
    events = pygame.event.get()
    handle_close_events(events)
    return clock.tick(frame_cap), events


# different game loops
def manual_game_loop():
    print('Manual Mode')
    robot = [0.0, 0.0]
    while game_is_running:
        ms_last_frame, events = init_game_cycle()
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            robot[1] -= speed * ms_last_frame / 1000
        if pressed_keys[pygame.K_a]:
            robot[0] -= speed * ms_last_frame / 1000
        if pressed_keys[pygame.K_s]:
            robot[1] += speed * ms_last_frame / 1000
        if pressed_keys[pygame.K_d]:
            robot[0] += speed * ms_last_frame / 1000
        fix_robot_pos(robot)
        draw(robot)


def square_game_loop():
    print('Square Mode')
    robot = [0.0, 0.0]
    current_direction = 'RIGHT'
    while game_is_running:
        ms_last_frame, events = init_game_cycle()
        if current_direction == 'RIGHT':
            robot[0] += speed * ms_last_frame / 1000
        if current_direction == 'DOWN':
            robot[1] += speed * ms_last_frame / 1000
        if current_direction == 'LEFT':
            robot[0] -= speed * ms_last_frame / 1000
        if current_direction == 'UP':
            robot[1] -= speed * ms_last_frame / 1000
        if robot[0] > width - size:
            current_direction = 'DOWN'
            robot[1] += robot[0] - (width - size)
        if robot[1] > height - size:
            current_direction = 'LEFT'
            robot[0] -= robot[1] - (height - size)
        if robot[0] < 0:
            current_direction = 'UP'
            robot[1] += robot[0]
        if robot[1] < 0:
            current_direction = 'RIGHT'
            robot[0] += robot[1]
        fix_robot_pos(robot)
        draw(robot)


def start():
    if game_mode == 'MANUAL':
        manual_game_loop()
    elif game_mode == 'SQUARE':
        square_game_loop()
    pygame.quit()


####
start()
