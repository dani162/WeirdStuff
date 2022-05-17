import pygame
from pygame.event import Event
import random

# constants
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
background_color = black
robot_color = white
path_color = green

size = 60
height = 1000
width = 1400

# distance per second
speed = 500
frame_cap = 60
clock = pygame.time.Clock()

debug_draw_path = True

# init stuff
pygame.init()
pygame.font.init()
pygame.display.set_caption('Weird Stuff')
screen = pygame.display.set_mode((width, height))

# variables
game_is_running = True
path = []

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


def draw_path(robot):
    path.append((robot[0] + size / 2, robot[1] + size / 2))
    for el in path:
        pygame.draw.circle(screen, path_color, el, 2)
    if len(path) >= 2:
        pygame.draw.lines(screen, path_color, False, path)


def draw(robot):
    screen.fill(background_color)
    if debug_draw_path:
        draw_path(robot)
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
    current_direction = 'UP'
    stop_top = 0
    stop_left = 0
    stop_right = width - size
    stop_bottom = height - size
    while game_is_running:
        ms_last_frame, events = init_game_cycle()
        if stop_bottom - stop_top < - 2 * size or stop_right - stop_left < - 2 * size:
            print("kleiner 0")
            continue

        # normal movement
        if current_direction == 'RIGHT':
            robot[0] += speed * ms_last_frame / 1000
        if current_direction == 'DOWN':
            robot[1] += speed * ms_last_frame / 1000
        if current_direction == 'LEFT':
            robot[0] -= speed * ms_last_frame / 1000
        if current_direction == 'UP':
            robot[1] -= speed * ms_last_frame / 1000
        # change movement on borders
        if robot[0] > stop_right and current_direction == 'RIGHT':
            current_direction = 'DOWN'
            robot[1] += robot[0] - stop_right
            robot[0] = stop_right
            stop_right -= size
        if robot[1] > stop_bottom and current_direction == 'DOWN':
            current_direction = 'LEFT'
            robot[0] -= robot[1] - stop_bottom
            robot[1] = stop_bottom
            stop_bottom -= size
        if robot[0] < stop_left and current_direction == 'LEFT':
            current_direction = 'UP'
            robot[1] += robot[0] - stop_left
            robot[0] = stop_left
            stop_left += size
        if robot[1] < stop_top and current_direction == 'UP':
            current_direction = 'RIGHT'
            robot[0] -= robot[1] - stop_top
            robot[1] = stop_top
            stop_top += size
        draw(robot)


def start():
    if game_mode == 'MANUAL':
        manual_game_loop()
    elif game_mode == 'SQUARE':
        square_game_loop()
    pygame.quit()


####
start()
