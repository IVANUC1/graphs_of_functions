import pygame
from math import *
from random import randint
import platform
import json
show_all = False
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
if platform.system() == "Windows":
    OS = 'windows'
else:
    OS = 'linux'

# game settings
mouse_act = False
dev_mod = False
act = True
frame_time = 0
multiplier = 1.2
pygame.init()
size = 1000  # расстояние между точками
if OS == 'windows':
    board_size_x = 50
    board_size_y = 50
else:
    board_size_x = 20
    board_size_y = 30
k_down = False
k_up = False
k_right = False
k_left = False
grid_size = 50
mid_pos_x = WIDTH / 2
mid_pos_y = HEIGHT / 2
pygame.display.set_caption('qwe')
clock = pygame.time.Clock()
# main_color = (230, 230, 230)
main_color = (0, 0, 30)
second_color = (47, 79, 79)
RED = (255, 0, 0)
FPS = 59
limit = False
running = True
screen.fill(main_color)
# main_funk = input('y = ')
main_funk = 'sin(x)'

button_plus_rect = pygame.Rect(25, HEIGHT - 180, 300, 150)
button_plus_surface = pygame.Surface((300, 150))
button_minus_rect = pygame.Rect(25, HEIGHT - 350, 300, 150)
button_minus_surface = pygame.Surface((300, 150))
button_plus_pressed = False
button_minus_pressed = False

def clip_line(y1, y2, y_limit):
    global limit
    if abs(y1) > y_limit or abs(y2) > y_limit:
        limit = True
        if abs(y2) > y_limit:
            return y_limit if y2 > 0 else -y_limit
    return y2


def android_UI():

    # Кнопка 1 (+)
    if button_plus_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_plus_surface, (100, 100, 255), (0, 0, 300, 150))
    else:
        pygame.draw.rect(button_plus_surface, (0, 0, 0), (0, 0, 300, 150))
        pygame.draw.rect(button_plus_surface, (200, 200, 200), (2, 2, 290, 145))

    # Кнопка 2 (-)
    if button_minus_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(button_minus_surface, (255, 100, 100), (0, 0, 300, 150))
    else:
        pygame.draw.rect(button_minus_surface, (0, 0, 0), (0, 0, 300, 150))
        pygame.draw.rect(button_minus_surface, (200, 200, 200), (2, 2, 290, 145))

    screen.blit(button_plus_surface, (25, HEIGHT - 180, 300, 150))
    screen.blit(button_minus_surface, (25, HEIGHT - 350, 300, 150))

    font = pygame.font.Font(None, 36)
    text1 = font.render("+", True, (0, 0, 0))
    text2 = font.render("-", True, (0, 0, 0))
    button_plus_surface.blit(text1, (50, 15))
    button_minus_surface.blit(text2, (50, 15))

class Funk(pygame.sprite.Sprite):
    def __init__(self, funk, color, show):
        pygame.sprite.Sprite.__init__(self)
        self.funk = funk
        self.color = color
        self.show = show
        self.math_functions = {
            'sin': sin,
            'cos': cos,
            'tan': tan,
            'asin': asin,
            'acos': acos,
            'atan': atan,
            'sinh': sinh,
            'cosh': cosh,
            'tanh': tanh,
            'exp': exp,
            'log': log,
            'log10': log10,
            'sqrt': sqrt,
            'pi': pi,
            'e': e,
            'abs': abs,
            'round': round,
            'int': int,
            'float': float
        }

    def draw(self):
        if self.show:
            global size, board_size_x, board_size_y, screen, grid_size, mid_pos_x, mid_pos_y, limit
            s = 100 / size
            old_pos_x = -board_size_x
            try:
                old_pos_y = eval(self.funk, {"__builtins__": {}}, {**self.math_functions, 'x': old_pos_x})
            except:
                old_pos_y = 0
    
            for i in range(0, int((board_size_x * 10) * (size / 500))):
                try:
                    x = old_pos_x + s
                    y = eval(self.funk, {"__builtins__": {}}, {**self.math_functions, 'x': x})
    
                    if abs(old_pos_y) <= board_size_y or abs(y) <= board_size_y:
                        draw_y1 = max(-board_size_y, min(board_size_y, old_pos_y))
                        draw_y2 = max(-board_size_y, min(board_size_y, y))
                        draw_line(self.color, old_pos_x, draw_y1, x, draw_y2, 4, False)
    
                    old_pos_y = y
                    old_pos_x = x
                except:
                    x = old_pos_x + s
                    old_pos_x = x
                    continue

with open('functions.json', 'r', encoding='utf-8') as f:
    functions_data = json.load(f)

functions = []
for item in functions_data:
    color = tuple(item['color'])
    functions.append(Funk(item['funk'], color, item['show']))

current_index = 0
for i, func in enumerate(functions):
    if func.show:
        current_index = i
        break

def draw_line(color, pos_x_1, pos_y_1, pos_x_2, pos_y_2, width, exl):
    global screen, mid_pos_x, mid_pos_y, grid_size
    form1 = (mid_pos_x + grid_size * pos_x_1, mid_pos_y + grid_size * -pos_y_1)
    form2 = (mid_pos_x + grid_size * pos_x_2, mid_pos_y - grid_size * pos_y_2)
    if not ((form1[0] < 0 or form1[1] < 0 or form1[0] > WIDTH or form1[1] > HEIGHT) and (
            form2[0] < 0 or form2[1] < 0 or form2[0] > WIDTH or form2[1] > HEIGHT)) or exl:
        pygame.draw.line(screen, color, form1, form2, width)


def grid_draw(screen, grid_size, mid_pos_x, mid_pos_y):
    screen.fill(main_color)
    for j in range(-board_size_y, board_size_y + 1):
        y_pos = mid_pos_y + grid_size * -j
        if 0 <= y_pos <= HEIGHT:
            pygame.draw.line(screen, second_color, (mid_pos_x + grid_size * -board_size_x, y_pos),
                             (mid_pos_x + grid_size * board_size_x, y_pos), 2)

    for i in range(-board_size_x, board_size_x + 1):
        x_pos = mid_pos_x + grid_size * i
        if 0 <= x_pos <= WIDTH:
            pygame.draw.line(screen, second_color, (x_pos, mid_pos_y - grid_size * -board_size_y),
                             (x_pos, mid_pos_y - grid_size * board_size_y), 2)
    pos_x = 0
    # if grid_size > 400:
    #     if mid_pos_x > WIDTH:
    #         pos_x = mid_pos_x/grid_size-4
    #     print(mid_pos_x/grid_size - pos_x)
    #     for i in range(mid_pos_x/grid_size - pos_x):
    #     pass

    draw_line(RED, 0, -board_size_y, 0, board_size_y, 3, True)  # вертикальная линия
    draw_line(RED, -board_size_x, 0, board_size_x, 0, 3, True)  # горизонтальная линия
    # границы
    draw_line(RED, board_size_x, -board_size_y, board_size_x, board_size_y, 3, True)
    draw_line(RED, -board_size_x, board_size_y, -board_size_x, -board_size_y, 3, True)
    draw_line(RED, -board_size_x, board_size_y, board_size_x, board_size_y, 3, True)
    draw_line(RED, board_size_x, -board_size_y, -board_size_x, -board_size_y, 3, True)
    font = pygame.font.Font(None, 36)
    text_fps = font.render(str(int(clock.get_fps())), True, (255, 255, 255))
    screen.blit(text_fps, (20, 20))
    text_func = font.render(functions[current_index].funk, True, (255, 255, 255))
    screen.blit(text_func, (60, 20))
    if dev_mod:
        text_speed = font.render(f'speed: {str(5 * multiplier)}', True, (255, 255, 255))
        screen.blit(text_speed, (20, 45))
        text_multiplier = font.render(f'multiplier: {str(multiplier)}', True, (255, 255, 255))
        screen.blit(text_multiplier, (20, 70))
        text_grid_size = font.render(f'grid size: {str(grid_size)}', True, (255, 255, 255))
        screen.blit(text_grid_size, (20, 95))
        text_mid_pos = font.render(f'x: {str(mid_pos_x - WIDTH / 2)}, y: {str(mid_pos_y - HEIGHT / 2)}', True,
                                   (255, 255, 255))
        screen.blit(text_mid_pos, (20, 120))
        text_size = font.render(f'size: {str(size)}', True, (255, 255, 255))
        screen.blit(text_size, (20, 150))

grid_draw(screen, grid_size, mid_pos_x, mid_pos_y)


# functions = []
# while True:
#     try:
#         col = int(input('введите кол-во функций, которые хотите нарисовать '))
#         break
#     except ValueError:
#         print('ошибка ввода')
# for i in range(col):
#     functions.append(Funk(input('введите формулу y = '), (255, 0, 0)))

def function():
    for func in functions:
        func.draw()


# main game
while running:
    if clock.get_fps() != 0:
        frame_time = FPS / clock.get_fps()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_start_x, mouse_start_y = pygame.mouse.get_pos()
            mid_x = mid_pos_x
            mid_y = mid_pos_y
            mouse_act = True
            if OS == 'linux':
                if button_plus_rect.collidepoint(event.pos):
                    button_plus_pressed = True
                if button_minus_rect.collidepoint(event.pos):
                    button_minus_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_act = False
            button_plus_pressed = False
            button_minus_pressed = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_F5:
                dev_mod = not dev_mod
                act = True
            if event.key == pygame.K_UP:
                k_up = True
                act = True
            if event.key == pygame.K_DOWN:
                k_down = True
                act = True
            if event.key == pygame.K_LEFT:
                k_left = True
                act = True
            if event.key == pygame.K_RIGHT:
                k_right = True
                act = True
            if event.key == pygame.K_SPACE:
                mid_pos_x = WIDTH / 2
                mid_pos_y = HEIGHT / 2
                act = True
            if event.key == pygame.K_1:
                if event.key == pygame.K_1:
                    show_all = not show_all  # Переключаем
                    for func in functions:
                        func.show = show_all  # Применяем ко всем
                    act = True
            if event.key == pygame.K_2:
                for func in functions:
                    func.show = False

                current_index = (current_index + 1) % len(functions)
                functions[current_index].show = True
                act = True
            if dev_mod:
                if event.key == pygame.K_F1:
                    multiplier += 2
                    act = True
                if event.key == pygame.K_F2:
                    multiplier -= 2
                    act = True
                if event.key == pygame.K_F3:
                    size += 1
                    act = True
                if event.key == pygame.K_F4:
                    size -= 1
                    act = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                k_up = False
            if event.key == pygame.K_DOWN:
                k_down = False
            if event.key == pygame.K_LEFT:
                k_left = False
            if event.key == pygame.K_RIGHT:
                k_right = False
        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                grid_size += 4 * multiplier
                multiplier += 0.05
                act = True
            elif event.y < 0:
                if grid_size > 5:
                    grid_size -= 4 * multiplier
                    multiplier -= 0.05
                    act = True

    # Обработка зажатых кнопок
    if button_plus_pressed:
        grid_size += 1 + multiplier
        act = True
    if button_minus_pressed and grid_size > 5:
        grid_size -= 1 + multiplier
        act = True
    if mouse_act:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mid_pos_x = mouse_x - mouse_start_x + mid_x
        mid_pos_y = mouse_y - mouse_start_y + mid_y
        act = True
    if k_up:
        mid_pos_y += 5 * multiplier * frame_time
        act = True
    if k_down:
        mid_pos_y -= 5 * multiplier * frame_time
        act = True
    if k_left:
        mid_pos_x += 5 * multiplier * frame_time
        act = True
    if k_right:
        mid_pos_x -= 5 * multiplier * frame_time
        act = True
    if act:
        grid_draw(screen, grid_size, mid_pos_x, mid_pos_y)
        for func in functions:
            func.draw()
        act = False
    if OS == 'linux':
        android_UI()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()