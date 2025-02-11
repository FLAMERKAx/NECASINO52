import sys
import random
import math
import pygame

# Настройки окна
WIDTH = 800
HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Начальная скорость роста коэффициента
BASE_COEFFICIENT_GROWTH_RATE = 0.01


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Lucky Jet")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Игровые параметры
        self.started = False
        self.crash_time = None
        self.current_coefficient = 1.0
        self.base_coefficient_growth_rate = BASE_COEFFICIENT_GROWTH_RATE
        self.coefficient_growth_rate = self.base_coefficient_growth_rate
        self.balance = 1000
        self.bet_amount = 10
        self.winnings = 0

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.started:
                    self.start_game()
                elif event.key == pygame.K_ESCAPE:
                    self.reset_game()

    def start_game(self):
        self.started = True
        self.crash_time = random.randint(20, 50)

    def update(self):
        if self.started:
            current_time = pygame.time.get_ticks() // 1000
            if current_time >= self.crash_time:
                self.crash()
            else:
                self.current_coefficient += self.coefficient_growth_rate
                self.coefficient_growth_rate *= 1.05

    def crash(self):
        self.started = False
        self.winnings = 0
        print(f"You lost! The coefficient was {self.current_coefficient:.2f}")

    def fix_winnings(self):
        self.winnings = self.bet_amount * self.current_coefficient
        self.balance += self.winnings
        self.reset_game()

    def reset_game(self):
        self.started = False
        self.crash_time = None
        self.current_coefficient = 1.0
        self.coefficient_growth_rate = self.base_coefficient_growth_rate

    def run(self):
        while True:
            self.handle_events()
            self.update()

            self.screen.fill(BLACK)

            # Отображение баланса
            self.draw_text(f"Balance: {self.balance}", WHITE, WIDTH // 2, 30)

            # Отображение текущей ставки
            self.draw_text(f"Bet Amount: {self.bet_amount}", WHITE, WIDTH // 2, 70)

            # Отображение текущего коэффициента
            self.draw_text(f"Current Coefficient: {self.current_coefficient:.2f}", YELLOW, WIDTH // 2, 110)

            # Кнопка для начала игры
            if not self.started:
                button_x = WIDTH // 2
                button_y = HEIGHT // 2
                button_width = 200
                button_height = 50
                pygame.draw.rect(self.screen, GREEN, (
                button_x - button_width // 2, button_y - button_height // 2, button_width, button_height))
                self.draw_text("Start Game", BLACK, button_x, button_y)

            # Кнопка для фиксации выигрыша
            if self.started:
                button_x = WIDTH // 4
                button_y = HEIGHT // 2
                button_width = 150
                button_height = 40
                pygame.draw.rect(self.screen, BLUE, (
                button_x - button_width // 2, button_y - button_height // 2, button_width, button_height))
                self.draw_text("Fix Winnings", WHITE, button_x, button_y)
                if self.winnings > 0:
                    self.draw_text(f"Winnigs: {self.winnings:.2f}", WHITE, WIDTH // 2, 150)

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()