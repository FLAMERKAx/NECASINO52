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
BASE_COEFFICIENT_GROWTH_RATE = 0.001

# Пороговые значения для штрафов и банов
LOW_COEFFICIENT_THRESHOLD = 1.10
MAX_LOW_COEFFICIENTS_ALLOWED = 3
BANNING_DURATION_SECONDS = 5  # 3 минуты

class Game:
    def __init__(self):
        self.lose = None
        self.last_win = None
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sonic")
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
        self.potential_winnings = 0
        self.warning_text = None

        # Переменная для отслеживания времени последнего касания Cash
        self.last_cashout_time = 0

        # История зафиксированных коэффициентов
        self.fixed_coefficients_history = []

        # Время начала бана
        self.ban_start_time = 0

        # Анимация Соника
        self.sonick_images = []
        try:
            # Загрузка изображений Соника (предполагается, что файлы называются sonic1.png, sonic2.png, ...)
            for i in range(1, 5):  # Загружаем 4 кадра анимации
                image = pygame.image.load(f"sonic{i}.png").convert_alpha() # Замените sonic1.png и т.д. на ваши файлы
                self.sonick_images.append(image)
        except FileNotFoundError:
            print("Ошибка")
            pygame.quit()
            sys.exit()
        self.sonick_index = 0  # Текущий кадр анимации
        self.sonick_rect = self.sonick_images[0].get_rect(center=(0, HEIGHT - 275)) # Начальная позиция
        self.sonick_speed = 3 # Скорость анимации
        self.animation_delay = 50 # Задержка между кадрами (мс)
        self.last_update = pygame.time.get_ticks() # Время последнего обновления кадра
        self.greeting = 'NECASINO52'

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.started:
                    if self.is_inside_button(mouse_pos, 'start'):
                        self.start_game()
                elif self.started:
                    if self.is_inside_button(mouse_pos, 'cashout'):
                        self.fix_winnings()

                elif self.lose and self.is_inside_button(mouse_pos, 'start'): # Обработка клика по кнопке после проигрыша
                    self.start_game() # Перезапуск игры

            elif event.type == pygame.KEYDOWN and not self.started:
                if event.key == pygame.K_BACKSPACE:
                    if len(str(self.bet_amount)) > 1:
                        self.bet_amount = int(str(self.bet_amount)[:-1])
                    else:
                        self.bet_amount = 0
                else:
                    try:
                        new_char = int(event.unicode)
                        if new_char >= 0:
                            self.bet_amount *= 10  # Умножаем текущую ставку на 10
                            self.bet_amount += new_char  # Добавляем новую цифру
                    except ValueError:
                        pass

    def bet_input_field(self):
        input_rect = pygame.Rect(415, 55, 140, 32)
        if self.started:
            pygame.draw.rect(self.screen, (128, 128, 128), input_rect)  # Серый цвет для заблокированного поля
        else:
            pygame.draw.rect(self.screen, (230, 230, 230), input_rect)
        font = pygame.font.SysFont('Arial', 16)
        bet_text = font.render(str(self.bet_amount), True, (0, 0, 0))
        self.screen.blit(bet_text, (input_rect.x + 5, input_rect.y + 8))
        pygame.draw.rect(self.screen, (0, 0, 0), input_rect, 2)

    def is_inside_button(self, pos, button_type):
        if button_type == 'start':
            button_x = WIDTH // 2
            button_y = 500
            button_width = 200
            button_height = 50
            return button_x - button_width // 2 <= pos[0] <= button_x + button_width // 2 and \
                   button_y - button_height // 2 <= pos[1] <= button_y + button_height // 2

        elif button_type == 'cashout':
            return WIDTH // 2 - 75 <= pos[0] <= WIDTH // 2 + 75 and \
                500 - 20 <= pos[1] <= 500 + 20

    def start_game(self):
        self.warning_text = None
        self.lose = None

        # Проверка истории коэффициентов и возможного бана
        if self.check_fixed_coefficients_history():
            if self.banned():
                self.warning_text = f"Вам временно запрещено играть. Подождите ещё {int(self.remaining_ban_duration())} секунд."
                return
            else:
                self.apply_penalty()

        if self.bet_amount <= self.balance and self.bet_amount != 0:
            self.started = True
            self.balance -= self.bet_amount
            self.crash_time = pygame.time.get_ticks() + random.randint(600, 15000)  # Время краша от 3 до 12 секунд
            self.sonick_rect.x = 0 # Сброс позиции Соника
            self.sonick_rect.centery = HEIGHT - 275 # Сброс позиции Соника
        else:
            self.warning_text = "Ставка должна быть больше нуля и не превышать ваш баланс."

    def check_fixed_coefficients_history(self):
        low_coefficients_count = sum(1 for coeff in self.fixed_coefficients_history if coeff < LOW_COEFFICIENT_THRESHOLD)
        return low_coefficients_count >= MAX_LOW_COEFFICIENTS_ALLOWED

    def apply_penalty(self):
        # Увеличение продолжительности бана при повторных нарушениях
        if self.ban_start_time > 0:
            self.ban_start_time += BANNING_DURATION_SECONDS * 1000
        else:
            self.ban_start_time = pygame.time.get_ticks() + BANNING_DURATION_SECONDS * 1000

    def banned(self):
        return self.ban_start_time > 0 and pygame.time.get_ticks() < self.ban_start_time + BANNING_DURATION_SECONDS * 1000

    def remaining_ban_duration(self):
        return max(0, (self.ban_start_time + BANNING_DURATION_SECONDS * 1000 - pygame.time.get_ticks()) // 1000)

    def ban_user(self):
        self.ban_start_time = pygame.time.get_ticks()

    def update(self):
        if self.started:
            current_time = pygame.time.get_ticks()
            if current_time >= self.crash_time:
                self.crash()
            else:
                self.current_coefficient += self.coefficient_growth_rate
                self.coefficient_growth_rate *= 1.0001
                self.potential_winnings = self.bet_amount * self.current_coefficient
                self.update_sonick() # Вызываем обновление анимации Соника во время игры
        else:

             self.sonick_rect.center = (0, HEIGHT - 150) # Reset position
             self.sonick_index = 0 # Reset sonick index
             self.last_update = pygame.time.get_ticks() # Reset sonick timer

    def crash(self):
        self.started = False
        self.winnings = 0
        self.lose = f"You lost! The coefficient was {self.current_coefficient:.2f}"
        self.current_coefficient = 1
        self.coefficient_growth_rate = 0.001
        self.sonick_rect.x = 0 # Reset sonick position

    def fix_winnings(self):
        # Проверяем, сколько времени прошло с момента последнего нажатия Cash
        current_time = pygame.time.get_ticks()
        time_since_last_cashout = current_time - self.last_cashout_time

        # Если прошло меньше 100 миллисекунд, уменьшаем коэффициент
        if time_since_last_cashout < 100:
            self.current_coefficient /= 2

        self.winnings = self.potential_winnings
        self.balance += self.winnings
        self.fixed_coefficients_history.append(self.current_coefficient)
        self.reset_game()

        # Обновляем время последнего нажатия Cash
        self.last_cashout_time = current_time

    def reset_game(self):
        self.started = False
        self.crash_time = None
        self.current_coefficient = 1.0
        self.coefficient_growth_rate = self.base_coefficient_growth_rate
        self.potential_winnings = 0
        self.last_win = self.winnings - self.bet_amount

    def update_sonick(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_delay:
            self.sonick_index = (self.sonick_index + 1) % len(self.sonick_images)
            self.last_update = now

        # Горизонтальное перемещение Соника
        if self.started:
            if self.sonick_rect.x < 325:
                self.sonick_rect.x += self.sonick_speed
            else:
                self.sonick_rect.x = 325  # Останавливаем Соника
        else:
            self.sonick_rect.center = (0, HEIGHT - 150) # Reset position

    def draw_sonick(self):
        self.screen.blit(self.sonick_images[self.sonick_index], self.sonick_rect)

    def run(self):
        while True:
            self.handle_events()
            self.update()

            self.screen.fill((101, 53, 155))

            # Отображение баланса
            self.draw_text(f"Balance: {self.balance:.2f}", WHITE, WIDTH // 2, 30)

            # Отображение текущей ставки
            self.draw_text(f"Bet Amount: ", WHITE, 335, 70)

            # Отображение текущего коэффициента
            self.draw_text(f"Current Coefficient: {self.current_coefficient:.2f}", YELLOW, WIDTH // 2, 110)

            if self.lose:
                self.draw_text(self.lose, WHITE, WIDTH // 2, 300)
                button_x = WIDTH // 2
                button_y = 500
                button_width = 200
                button_height = 50
                pygame.draw.rect(self.screen, (255, 165, 0), (
                    button_x - button_width // 2, button_y - button_height // 2, button_width, button_height))
                self.draw_text("Start", BLACK, button_x, button_y)
            elif self.started:
                self.draw_sonick() # Draw Sonic during the game
                button_x = WIDTH // 2
                button_y = 500
                button_width = 150
                button_height = 40
                pygame.draw.rect(self.screen, BLUE, (
                    button_x - button_width // 2, button_y - button_height // 2, button_width, button_height))
                self.draw_text("Cash", WHITE, button_x, button_y)
                self.draw_text(f"Potential Winnings: {self.potential_winnings:.2f}", WHITE, WIDTH // 2, 150)
            else:
                button_x = WIDTH // 2
                button_y = 500
                button_width = 200
                button_height = 50
                pygame.draw.rect(self.screen, (255, 165, 0), (
                    button_x - button_width // 2, button_y - button_height // 2, button_width, button_height))
                self.draw_text("Start", BLACK, button_x, button_y)



            if self.warning_text:
                self.draw_text(self.warning_text, WHITE, WIDTH // 2, 300)

            if self.greeting:
                font = pygame.font.SysFont('Comic Sans', 46, bold=True)
                text = font.render(self.greeting, True, WHITE)
                self.screen.blit(text, (250, 160))

            self.bet_input_field()

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()