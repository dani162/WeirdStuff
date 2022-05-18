import pygame
import math
from pygame.event import Event
import random

# constants
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
light_gray = (211, 211, 211)
background_color = black
robot_color = white
path_color = green

size = 30
height = 600
width = 800

# distance per second
speed = 400
frame_cap = 60
clock = pygame.time.Clock()

debug_draw_path = False
debug_draw_background = True
debug_show_help = True

random_percentage = 0.10

# init stuff
pygame.init()
pygame.font.init()
pygame.display.set_caption('Weird Stuff')
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont("Arial", 40)
font_settings = pygame.font.SysFont("Arial", 20)
font_help = pygame.font.SysFont("Arial", 18)

# variables
game_is_running = True
is_first_game_cycle = True
path = []


####
def handle_close_events(events: list[Event]):
    for event in events:
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True


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
def reset_game_loop_vars():
    global game_is_running
    global is_first_game_cycle
    global path
    game_is_running = True
    is_first_game_cycle = True
    path = []


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
    global game_is_running
    events = pygame.event.get()
    game_is_running = handle_close_events(events)
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
        if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            robot[1] -= speed * ms_last_frame / 1000
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            robot[0] -= speed * ms_last_frame / 1000
        if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            robot[1] += speed * ms_last_frame / 1000
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
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
    hit_corners = [False, False, False, False]
    while game_is_running:
        ms_last_frame, events = init_game_cycle()
        if hit_corners[0] and hit_corners[1] and hit_corners[2] and hit_corners[3]:
            continue
        temp_speed = speed * ms_last_frame / 1000
        angle_speed = temp_speed / math.sqrt(size**2/(4*math.pi**2)+(current_radius**2))
        radius_speed = math.sqrt(temp_speed**2 - current_radius**2 * angle_speed**2)
        current_radius += radius_speed
        current_angle += angle_speed
        robot[0] = start_position[0] + math.cos(current_angle) * current_radius
        robot[1] = start_position[1] + math.sin(current_angle) * current_radius
        if robot[0] <= 0 and robot[1] <= 0:
            hit_corners[0] = True
        if robot[0] >= width - size and robot[1] <= 0:
            hit_corners[1] = True
        if robot[0] <= 0 and robot[1] >= height - size:
            hit_corners[2] = True
        if robot[0] >= width and robot[1] >= height - size:
            hit_corners[3] = True
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


def menu_loop(selected_index):
    print('Game Menu')
    help_texts = [
        ['ESC', 'Close program or go back to main menu'],
        ['W / UP', 'Navigate up - Move up in manual mode'],
        ['A / LEFT', 'Move left in manual mode'],
        ['S / DOWN', 'Navigate down - Move down in manual mode'],
        ['D / RIGHT', 'Move right in manual mode'],
        ['Return', 'Select menu item'],
    ]
    texts = [
        [font.render("Manual", True, white), 'MANUAL'],
        [font.render("Square Spiral", True, white), 'SQUARE_SPIRAL'],
        [font.render("Spiral", True, white), 'SPIRAL'],
        [font.render("Random", True, white), 'RANDOM'],
        [font.render("Exit", True, white), 'EXIT'],
        [font_settings.render("Draw Path", True, green if debug_draw_path else red), 'DEBUG_PATH'],
        [font_settings.render("Redraw Background", True, green if debug_draw_background else red), 'DEBUG_BACKGROUND'],
        [font_settings.render("Show Help", True, green if debug_show_help else red), 'DEBUG_SHOW_HELP']
    ]
    mode = ""

    while mode == "":
        events = pygame.event.get()
        if not handle_close_events(events):
            mode = "EXIT"
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    selected_index -= 1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    selected_index += 1
                selected_index = selected_index % len_texts
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    mode = texts[selected_index][1]

        screen.fill(black)
        len_texts = len(texts)
        temp_height_help = 0
        if debug_show_help:
            for help_text in help_texts:
                key = font_help.render(help_text[0], True, yellow)
                key_text = font_help.render(help_text[1], True, light_gray)
                screen.blit(key, (0, temp_height_help))
                screen.blit(key_text, (90, temp_height_help))
                temp_height_help += key.get_height()
        index = 0
        offset = 12
        border_offset = offset / 2
        sum_height = 0
        for text in texts:
            sum_height += text[0].get_height() + offset
        sum_height -= offset
        temp_height = 0
        for text in texts:
            screen.blit(text[0], (
                (width - text[0].get_width()) / 2,
                (height - temp_height_help - sum_height) / 2 + temp_height + temp_height_help
            ))
            if selected_index == index:
                pygame.draw.rect(screen, yellow, (
                    (width - (text[0].get_width() + border_offset)) / 2,
                    (height - temp_height_help - sum_height) / 2 + temp_height_help + temp_height - border_offset / 2,
                    text[0].get_width() + border_offset,
                    text[0].get_height() + border_offset,
                ), 1)
            temp_height += text[0].get_height()
            index += 1
        pygame.display.update()
        clock.tick(frame_cap)
    return mode, selected_index


def start():
    mode = ""
    index = 0
    while mode != "EXIT":
        global debug_draw_path
        global debug_draw_background
        global debug_show_help
        mode, index = menu_loop(index)
        screen.fill(black)
        if mode == 'MANUAL':
            manual_game_loop()
        elif mode == 'SQUARE_SPIRAL':
            square_game_loop()
        elif mode == 'SPIRAL':
            circle_game_loop()
        elif mode == 'RANDOM':
            random_game_loop()
        elif mode == 'DEBUG_PATH':
            debug_draw_path = not debug_draw_path
        elif mode == 'DEBUG_BACKGROUND':
            debug_draw_background = not debug_draw_background
        elif mode == 'DEBUG_SHOW_HELP':
            debug_show_help = not debug_show_help
        reset_game_loop_vars()
    pygame.quit()


####
start()
