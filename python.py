import pygame
import random
import sys

pygame.init()

screen_width = 420
screen_height = 420
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('python')

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

snake_size = 10
snake_speed = 15

snake = [[100, 100], [90, 100], [80, 100]]
direction = 'RIGHT'

clock = pygame.time.Clock()

apple_x = random.randrange(0, screen_width, snake_size)
apple_y = random.randrange(0, screen_height, snake_size)

def move_snake(snake, direction):
    if direction == 'UP':
        new_head = [snake[0][0], snake[0][1] - snake_size]
    elif direction == 'DOWN':
        new_head = [snake[0][0], snake[0][1] + snake_size]
    elif direction == 'LEFT':
        new_head = [snake[0][0] - snake_size, snake[0][1]]
    elif direction == 'RIGHT':
        new_head = [snake[0][0] + snake_size, snake[0][1]]
    snake.insert(0, new_head)
    snake.pop()
    return snake

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, BLACK, pygame.Rect(segment[0], segment[1], snake_size, snake_size))

def draw_apple(apple_x, apple_y):
    pygame.draw.rect(screen, RED, pygame.Rect(apple_x, apple_y, snake_size, snake_size))

def game_loop():
    global snake, direction, apple_x, apple_y

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

        snake = move_snake(snake, direction)

        if snake[0][0] < 0 or snake[0][0] >= screen_width or snake[0][1] < 0 or snake[0][1] >= screen_height:
            game_over = True
        for segment in snake[1:]:
            if segment == snake[0]:
                game_over = True

        if snake[0][0] == apple_x and snake[0][1] == apple_y:
            apple_x = random.randrange(0, screen_width, snake_size)
            apple_y = random.randrange(0, screen_height, snake_size)
            snake.append(snake[-1])

        screen.fill(WHITE)
        draw_snake(snake)
        draw_apple(apple_x, apple_y)

        pygame.display.update()

        clock.tick(snake_speed)

    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

game_loop()
