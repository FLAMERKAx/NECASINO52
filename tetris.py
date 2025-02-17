import random
import sqlite3

import numpy as np
import pygame


class TetrisGame:
    def __init__(self, money, user_id):
        pygame.init()
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 500, 601
        self.GRID_WIDTH, self.GRID_HEIGHT = 300, 600
        self.TILE_SIZE = 30
        self.colors = [
            (200, 200, 200),
            (215, 133, 133),
            (30, 145, 255),
            (0, 170, 0),
            (180, 0, 140),
            (200, 200, 0)
        ]

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")

        self.balance = money
        self.user_id = user_id
        self.blocks = []
        self.current_block = None
        self.next_block = None
        self.score = 0
        self.grid = [[0] * 10 for _ in range(20)]
        self.game_over = False
        self.paused = False
        self.game_started = False  # Новое состояние игры

        self.block_shapes = [
            [[1, 1], [1, 1]],  # Square
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1], [1], [1], [1]],  # Line
            [[1, 1], [1, 0], [1, 0]],  # L
            [[0, 1], [1, 1], [1, 0]]  # Z
        ]

    def init_game(self):
        self.current_block = self.create_new_block()
        self.next_block = self.create_new_block()
        self.score = 0
        self.grid = [[0] * 10 for _ in range(20)]
        self.game_over = False
        self.game_started = True  # Игра начата

    def create_new_block(self):
        shape = random.choice(self.block_shapes)
        color = random.choice(self.colors)
        return {
            'struct': np.array(shape),
            'color': color,
            'x': 4,
            'y': 0,
            'rotation': 0
        }

    def draw_block(self, block, offset_x=0, offset_y=0):
        for y, row in enumerate(block['struct']):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        (block['x'] + x + offset_x) * self.TILE_SIZE,
                        (block['y'] + y + offset_y) * self.TILE_SIZE,
                        self.TILE_SIZE - 2,
                        self.TILE_SIZE - 2
                    )
                    pygame.draw.rect(self.screen, block['color'], rect)

    def check_collision(self, block, dx=0, dy=0):
        for y, row in enumerate(block['struct']):
            for x, cell in enumerate(row):
                if cell:
                    new_x = block['x'] + x + dx
                    new_y = block['y'] + y + dy
                    if new_x < 0 or new_x >= 10 or new_y >= 20:
                        return True
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return True
        return False

    def rotate_block(self, block):
        struct = np.rot90(block['struct'])
        if not self.check_collision({'struct': struct, 'x': block['x'], 'y': block['y']}):
            block['struct'] = struct

    def merge_block(self, block):
        for y, row in enumerate(block['struct']):
            for x, cell in enumerate(row):
                if cell:
                    if block['y'] + y < 0:
                        self.game_over = True
                        return
                    self.grid[block['y'] + y][block['x'] + x] = block['color']

    def clear_lines(self):
        full_lines = []
        for i, row in enumerate(self.grid):
            if all(row):
                full_lines.append(i)

        for i in full_lines:
            del self.grid[i]
            self.grid.insert(0, [0] * 10)
            self.balance += 100
            self.score += 100

    def move_down(self):
        if not self.check_collision(self.current_block, dy=1):
            self.current_block['y'] += 1
            return True
        self.merge_block(self.current_block)
        self.clear_lines()
        self.current_block = self.next_block
        self.next_block = self.create_new_block()
        return False

    def move_side(self, dx):
        if not self.check_collision(self.current_block, dx=dx):
            self.current_block['x'] += dx

    def handle_input(self, key):
        if key == pygame.K_LEFT:
            self.move_side(-1)
        elif key == pygame.K_RIGHT:
            self.move_side(1)
        elif key == pygame.K_DOWN:
            self.move_down()
        elif key == pygame.K_UP:
            self.rotate_block(self.current_block)
        elif key == pygame.K_p:
            self.paused = not self.paused

    def draw_grid(self):
        for x in range(11):
            pygame.draw.line(self.screen, (50, 50, 50),
                             (x * self.TILE_SIZE, 0), (x * self.TILE_SIZE, self.GRID_HEIGHT))
        for y in range(21):
            pygame.draw.line(self.screen, (50, 50, 50),
                             (0, y * self.TILE_SIZE), (self.GRID_WIDTH, y * self.TILE_SIZE))

    def draw_sidebar(self):
        font = pygame.font.SysFont('Arial', 24)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (320, 100))
        text = font.render(f"Balance: {self.balance}", True, (255, 255, 255))
        self.screen.blit(text, (320, 150))

        # Превью следующей фигуры
        if self.game_started:
            preview_x, preview_y = 320, 200
            for y, row in enumerate(self.next_block['struct']):
                for x, cell in enumerate(row):
                    if cell:
                        rect = pygame.Rect(
                            preview_x + x * self.TILE_SIZE,
                            preview_y + y * self.TILE_SIZE,
                            self.TILE_SIZE - 2,
                            self.TILE_SIZE - 2
                        )
                        pygame.draw.rect(self.screen, self.next_block['color'], rect)

    def draw_buttons(self):
        # Кнопка "Играть"
        self.play_button_rect = pygame.Rect(320, 400, 150, 40)
        pygame.draw.rect(self.screen, (0, 255, 0), self.play_button_rect)
        font = pygame.font.SysFont('Arial', 24)
        text = font.render("Играть", True, (0, 0, 0))
        self.screen.blit(text, (self.play_button_rect.x + 50, self.play_button_rect.y + 10))

        # Кнопка "Закончить Игру"
        self.quit_button_rect = pygame.Rect(320, 450, 150, 40)
        pygame.draw.rect(self.screen, (255, 0, 0), self.quit_button_rect)
        text = font.render("Закончить", True, (0, 0, 0))
        self.screen.blit(text, (self.quit_button_rect.x + 30, self.quit_button_rect.y + 10))

    def run(self):
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 1000

        while True:
            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_sidebar()
            self.draw_buttons()

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sqlite_connection = sqlite3.connect('nebd52.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    cursor.execute(
                        f"""UPDATE ludiki SET money = {self.balance}, tetris = 1 WHERE id = {self.user_id};""")
                    sqlite_connection.commit()
                    cursor.close()
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    self.handle_input(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.play_button_rect.collidepoint(mouse_x, mouse_y):
                        if not self.game_started or self.game_over:
                            self.init_game()
                    elif self.quit_button_rect.collidepoint(mouse_x, mouse_y):
                        self.game_started = False
                        self.game_over = True

            # Логика игры
            if self.game_started and not self.game_over and not self.paused:
                fall_time += clock.get_rawtime()
                if fall_time >= fall_speed:
                    if not self.move_down():
                        fall_time = 0
                    else:
                        fall_time = fall_speed - 100

            # Отрисовка блоков
            if self.game_started:
                self.draw_block(self.current_block)

            # Отрисовка сетки
            for y, row in enumerate(self.grid):
                for x, color in enumerate(row):
                    if color:
                        rect = pygame.Rect(
                            x * self.TILE_SIZE + 1,
                            y * self.TILE_SIZE + 1,
                            self.TILE_SIZE - 2,
                            self.TILE_SIZE - 2
                        )
                        pygame.draw.rect(self.screen, color, rect)

            # Сообщение о конце игры
            if self.game_over:
                font = pygame.font.SysFont('Arial', 48)
                text = font.render("GAME OVER", True, (255, 0, 0))
                self.screen.blit(text, (50, 300))
                font = pygame.font.SysFont('Arial', 20)
                text = font.render(f"Вы выиграли {self.score}", True, (0, 255, 0))
                self.screen.blit(text, (70, 400))

            pygame.display.flip()
            clock.tick(30)


if __name__ == "__main__":
    game = TetrisGame()
    game.run()
