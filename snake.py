import pygame
import sys
import random

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.speed = 15
        self.frame_size_x = 1380
        self.frame_size_y = 840
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))
        pygame.display.set_caption("Snake Game")
        self.fps_controller = pygame.time.Clock()
        self.square_size = 60
        self.colors = {
            'black': pygame.Color(0, 0, 0),
            'white': pygame.Color(255, 255, 255),
            'red': pygame.Color(255, 0, 0),
            'green': pygame.Color(0, 255, 0),
            'blue': pygame.Color(0, 0, 255),
        }
        self.reset()

    def reset(self):
        self.direction = 'RIGHT'
        self.head_pos = [120, 60]
        self.snake_body = [[120, 60]]
        self.food_pos = [random.randrange(1, (self.frame_size_x // self.square_size)) * self.square_size,
                         random.randrange(1, (self.frame_size_y // self.square_size)) * self.square_size]
        self.food_spawn = True
        self.score = 0

    def show_score(self, position, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render(f'Score: {self.score}', True, color)
        score_rect = score_surface.get_rect()
        if position == 'top':
            score_rect.midtop = (self.frame_size_x / 10, 15)
        else:
            score_rect.midtop = (self.frame_size_x / 2, self.frame_size_y / 1.25)
        self.game_window.blit(score_surface, score_rect)

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.change_direction(event.key)

            self.move_snake()
            self.check_food_collision()
            self.render_graphics()
            self.check_self_collision()
            self.show_score('top', self.colors['white'], 'consolas', 20)
            pygame.display.update()
            self.fps_controller.tick(self.speed)

    def change_direction(self, key):
        if key in [pygame.K_UP, ord('w')] and self.direction != 'DOWN':
            self.direction = 'UP'
        elif key in [pygame.K_DOWN, ord('s')] and self.direction != 'UP':
            self.direction = 'DOWN'
        elif key in [pygame.K_LEFT, ord('a')] and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif key in [pygame.K_RIGHT, ord('d')] and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def move_snake(self):
        if self.direction == 'UP':
            self.head_pos[1] -= self.square_size
        elif self.direction == 'DOWN':
            self.head_pos[1] += self.square_size
        elif self.direction == 'LEFT':
            self.head_pos[0] -= self.square_size
        elif self.direction == 'RIGHT':
            self.head_pos[0] += self.square_size

        self.head_pos[0] %= self.frame_size_x
        self.head_pos[1] %= self.frame_size_y

        self.snake_body.insert(0, list(self.head_pos))
        if not self.food_spawn:
            self.snake_body.pop()
        else:
            self.food_spawn = False

    def check_food_collision(self):
        if self.head_pos == self.food_pos:
            self.score += 1
            self.food_spawn = True
            self.food_pos = [random.randrange(1, (self.frame_size_x // self.square_size)) * self.square_size,
                             random.randrange(1, (self.frame_size_y // self.square_size)) * self.square_size]

    def render_graphics(self):
        self.game_window.fill(self.colors['black'])
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, self.colors['green'], pygame.Rect(pos[0], pos[1], self.square_size, self.square_size))
        pygame.draw.rect(self.game_window, self.colors['red'], pygame.Rect(self.food_pos[0], self.food_pos[1], self.square_size, self.square_size))

    def check_self_collision(self):
        if self.head_pos in self.snake_body[1:]:
            self.reset()

if __name__ == '__main__':
    game = SnakeGame()
    game.game_loop()


