import pygame
import math
from pygame.event import Event
import random

# constants
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
background_color = black
robot_color = white
path_color = green

size = 25
height = 380
width = 500

# distance per second
speed = 400
frame_cap = 60
clock = pygame.time.Clock()

debug_draw_path = True
debug_draw_background = True

random_percentage = 0.10

# init stuff
pygame.init()
pygame.font.init()
pygame.display.set_caption('Weird Stuff')
screen = pygame.display.set_mode((width, height))

# variables
game_is_running = True
is_first_game_cycle = True
path = []

# possible game modes: 'MANUAL', 'SQUARE_SPIRAL', 'SPIRAL' and 'RANDOM'
game_mode = 'RANDOM'


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
    if len(path) >= 2:
        pygame.draw.lines(screen, path_color, False, path)


def draw(robot):
    if debug_draw_background:
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


def get_randomized_velocity(velocity_1=None, velocity_2=None):
    if not velocity_1:
        velocity_1 = random.uniform(-1, 1) * speed
        velocity_2 = math.sqrt(speed**2 - velocity_1**2) * (2 * random.randint(0, 1) - 1)
        return velocity_1, velocity_2
    velocity_2_direction = 1
    if velocity_2 < 0:
        velocity_2_direction = -1
    velocity_1 += random.uniform(-1, 1) * speed * random_percentage
    if velocity_1 > speed:
        velocity_1 = velocity_1 - (velocity_1 - speed)
        velocity_2_direction *= -1
    elif velocity_1 < - speed:
        velocity_1 = velocity_1 - (velocity_1 + speed)
        velocity_2_direction *= -1
    velocity_2 = math.sqrt(speed ** 2 - velocity_1 ** 2) * velocity_2_direction
    return velocity_1, velocity_2


def init_game_cycle():
    events = pygame.event.get()
    handle_close_events(events)
    ms_last_frame = clock.tick(frame_cap)
    global is_first_game_cycle
    if is_first_game_cycle:
        ms_last_frame = 0
        is_first_game_cycle = False
    return ms_last_frame, events


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
    finished = False
    while game_is_running:
        ms_last_frame, events = init_game_cycle()
        if finished:
            continue
        # normal movement
        if current_direction == 'RIGHT':
            robot[0] += speed * ms_last_frame / 1000
        elif current_direction == 'DOWN':
            robot[1] += speed * ms_last_frame / 1000
        elif current_direction == 'LEFT':
            robot[0] -= speed * ms_last_frame / 1000
        elif current_direction == 'UP':
            robot[1] -= speed * ms_last_frame / 1000
        # change movement on borders
        if robot[0] > stop_right and current_direction == 'RIGHT':
            current_direction = 'DOWN'
            robot[1] += robot[0] - stop_right
            robot[0] = stop_right
            stop_right -= size
            finished = (stop_bottom - stop_top) + size < 0
        elif robot[1] > stop_bottom and current_direction == 'DOWN':
            current_direction = 'LEFT'
            robot[0] -= robot[1] - stop_bottom
            robot[1] = stop_bottom
            stop_bottom -= size
            finished = (stop_right - stop_left) + size < 0
        elif robot[0] < stop_left and current_direction == 'LEFT':
            current_direction = 'UP'
            robot[1] += robot[0] - stop_left
            robot[0] = stop_left
            stop_left += size
            finished = (stop_bottom - stop_top) + size < 0
        elif robot[1] < stop_top and current_direction == 'UP':
            current_direction = 'RIGHT'
            robot[0] -= robot[1] - stop_top
            robot[1] = stop_top
            stop_top += size
            finished = (stop_right - stop_left) + size < 0
        draw(robot)


def circle_game_loop():
    print('Circle Mode')
    start_position = [(width-size)/2, (height-size)/2]
    robot = [start_position[0], start_position[1]]
    current_radius = 0
    current_angle = 0
    while game_is_running:
        ms_last_frame, events = init_game_cycle()
        temp_speed = speed * ms_last_frame / 1000
        angle_speed = temp_speed / math.sqrt(size**2/(4*math.pi**2)+(current_radius**2))
        radius_speed = math.sqrt(temp_speed**2 - current_radius**2 * angle_speed**2)
        current_radius += radius_speed
        current_angle += angle_speed
        robot[0] = start_position[0] + math.cos(current_angle) * current_radius
        robot[1] = start_position[1] + math.sin(current_angle) * current_radius
        fix_robot_pos(robot)
        draw(robot)


def random_game_loop():
    print('Random Mode')
    robot = [(width-size)/2, (height-size)/2]
    velocity_x, velocity_y = get_randomized_velocity()
    while game_is_running:
        ms_last_frame, events = init_game_cycle()
        robot[0] += velocity_x * ms_last_frame / 1000
        robot[1] += velocity_y * ms_last_frame / 1000
        if robot[0] < 0:
            velocity_x, velocity_y = get_randomized_velocity(velocity_x*-1, velocity_y)
        if robot[0] > width - size:
            velocity_x, velocity_y = get_randomized_velocity(velocity_x*-1, velocity_y)
        if robot[1] < 0:
            velocity_y, velocity_x = get_randomized_velocity(velocity_y*-1, velocity_x)
        if robot[1] > height - size:
            velocity_y, velocity_x = get_randomized_velocity(velocity_y*-1, velocity_x)
        fix_robot_pos(robot)
        draw(robot)


def start():
    if game_mode == 'MANUAL':
        manual_game_loop()
    elif game_mode == 'SQUARE_SPIRAL':
        square_game_loop()
    elif game_mode == 'SPIRAL':
        circle_game_loop()
    elif game_mode == 'RANDOM':
        random_game_loop()
    pygame.quit()


####
start()
