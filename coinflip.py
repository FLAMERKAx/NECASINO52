import random
import sys

import pygame

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (179, 167, 240)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
SILVER = (242, 244, 248)

# Настройки игры
INITIAL_BALANCE = 2000
BASE_COEFF = 1.75
MAX_COEFF = 2.95

GRAVITY = 0.5
screen_rect = pygame.Rect(-50, -50, WIDTH + 50, HEIGHT + 50)


class Particle(pygame.sprite.Sprite):
    # Загружаем только базовое изображение без масштабирования
    fire = [pygame.image.load("smallcoin.png")]  # Убедитесь что изображение достаточно большое

    def __init__(self, groups, pos, dx, dy):
        super().__init__(groups)
        self.image = self.fire[0]  # Берем всегда оригинальное изображение
        self.rect = self.image.get_rect(center=pos)
        self.velocity = [dx, dy]
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if not self.rect.colliderect(screen_rect):
            self.kill()


# Остальной код остается без изменений
def create_particles(position, group, particle):
    particle_count = particle
    numbers = range(-30, 30)
    for _ in range(particle_count):
        Particle(group, position, random.choice(numbers), random.choice(numbers))

class CoinFlipGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CoinFlip")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        pygame.mixer.init()

        # Состояние игры
        self.balance = INITIAL_BALANCE
        self.history = []
        self.current_bet = 0
        self.selected_side = None
        self.result = None
        self.streak = 0
        self.coeff = BASE_COEFF
        self.current_result = None
        self.background_img = pygame.image.load('background.png')
        self.play_sound("background.mp3", loop=True, volume=0.05)
        self.all_sprites = pygame.sprite.Group()

        # Загрузка изображений
        try:
            self.coin_img = pygame.image.load('coin.png').convert_alpha()
            self.heads_img = pygame.image.load('heads.png').convert_alpha()
            self.tails_img = pygame.image.load('tails.png').convert_alpha()

            self.tailsbtn_img = pygame.image.load('tailsbtn.png').convert_alpha()
            self.headsbtn_img = pygame.image.load('headsbtn.png').convert_alpha()

            self.tailsbtnsel_img = pygame.image.load('tailsbtnsel.png').convert_alpha()
            self.headsbtnsel_img = pygame.image.load('headsbtnsel.png').convert_alpha()

            self.inputbox_img = pygame.image.load('inputbox.png').convert_alpha()
            self.playbtn_img = pygame.image.load('playbtn.png').convert_alpha()

            self.bigwin_img = pygame.image.load('bigwin.png').convert_alpha()
            self.biglose_img = pygame.image.load('biglose.png').convert_alpha()
        except:
            # Заглушки если изображений нет
            self.coin_img = pygame.Surface((100, 100))
            self.coin_img.fill(GOLD)
            self.heads_img = self.coin_img.copy()
            self.tails_img = self.coin_img.copy()

        # Поле ввода ставки
        self.input_rect = pygame.Rect(205, 530, 200, 40)
        self.input_text = ''

    def calculate_coeff(self):
        # Обновляем счетчик серии и коэффициент
        if len(self.history) >= 2:
            if self.history[-1] == self.history[-2]:
                self.streak += 1
            else:
                self.streak = 0
        else:
            self.streak = 0

        # Рассчитываем коэффициент с учетом максимального значения
        self.coeff = min(BASE_COEFF + self.streak * 0.3, MAX_COEFF)

        # Гарантируем что при пустой истории будет базовый коэффициент
        if len(self.history) == 0:
            self.coeff = BASE_COEFF

    def draw_button(self, text, rect, color):
        pygame.draw.rect(self.screen, color, rect)
        text_surf = self.font.render(text, True, BLACK)
        self.screen.blit(text_surf, (rect.x + 10, rect.y + 5))

    def play_sound(self, path, volume=0.5, loop=False):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        sound.play(loops=-1 if loop else 0)
        return sound

    def run(self):
        running = True

        while running:
            self.screen.blit(self.background_img, (0, 0))

            # Рисуем историю
            for i, res in enumerate(self.history[-5:]):
                if res == "Heads":
                    self.screen.blit(self.heads_img, (100 + i * 60, 50))
                else:
                    self.screen.blit(self.tails_img, (100 + i * 60, 50))
                # pygame.draw.circle(self.screen, "red", (100 + i * 60, 50), 20)

            # Рисуем монету
            self.screen.blit(self.coin_img, (317, 233))


            # Кнопки выбора стороны
            heads_btn = pygame.Rect(200, 424, 150, 50)
            tails_btn = pygame.Rect(433, 424, 150, 50)
            self.screen.blit(self.tailsbtn_img if self.selected_side != 'Tails' else self.tailsbtnsel_img, tails_btn)
            self.screen.blit(self.headsbtn_img if self.selected_side != 'Heads' else self.headsbtnsel_img, heads_btn)
            # self.draw_button('Орел', heads_btn, GRAY if self.selected_side != 'Heads' else GREEN)
            # self.draw_button('Решка', tails_btn, GRAY if self.selected_side != 'Tails' else GREEN)

            # Поле ввода ставки
            self.screen.blit(self.inputbox_img, self.input_rect)
            text_surf = self.font.render(self.input_text, True, BLACK)
            self.screen.blit(text_surf, (self.input_rect.x + 10, self.input_rect.y + 10))

            # Кнопка старта
            start_btn = pygame.Rect(413, 496, 210, 75)
            self.screen.blit(self.playbtn_img, start_btn)

            # Отображение коэффициента и баланса
            coeff_text = self.font.render(f'Кэф: x{self.coeff:.2f}', True, BLACK)
            self.screen.blit(coeff_text, (WIDTH - 220, 80))

            balance_text = self.font.render(f'Баланс: ${self.balance}', True, BLACK)
            self.screen.blit(balance_text, (WIDTH - 220, 35))

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if heads_btn.collidepoint(mouse_pos):
                        self.selected_side = 'Heads'
                    elif tails_btn.collidepoint(mouse_pos):
                        self.selected_side = 'Tails'
                    elif start_btn.collidepoint(mouse_pos):
                        if self.selected_side and self.input_text:
                            self.current_bet = int(self.input_text)
                            if self.current_bet <= self.balance:
                                self.balance -= self.current_bet
                                result = random.choice(['Heads', 'Tails'])
                                self.history.append(result)
                                self.play_sound("coin.mp3")
                                pygame.time.wait(700)
                                self.play_sound("coin_finish.mp3")
                                pygame.time.wait(300)
                                if (self.current_bet * self.coeff) < 2000:
                                    if result == self.selected_side:
                                        self.balance += int(self.current_bet * self.coeff)
                                        result_text = self.font.render('Победа!', True, GREEN)
                                        self.screen.blit(result_text, (350, 150))
                                    else:
                                        result_text = self.font.render('Поражение', True, RED)
                                        self.screen.blit(result_text, (330, 150))
                                else:
                                    if result == self.selected_side:
                                        self.balance += int(self.current_bet * self.coeff)
                                        sound = self.play_sound("bigwin.mp3", loop=True)
                                        for _ in range(3):
                                            pygame.time.wait(5)
                                            create_particles((400, -20), self.all_sprites, 50)
                                            create_particles((380, -20), self.all_sprites, 50)
                                            create_particles((420, -20), self.all_sprites, 50)
                                            for _ in range(20):
                                                self.screen.blit(self.bigwin_img, (100, 30))
                                                pygame.time.wait(5)
                                                pygame.time.wait(5)

                                                self.font = pygame.font.Font(None, 100)
                                                result_text = self.font.render(f"{int(self.current_bet * self.coeff)}", True, (243, 241, 41))
                                                self.screen.blit(result_text, (330, 295))
                                                self.font = pygame.font.Font(None, 36)

                                                self.all_sprites.update()
                                                self.all_sprites.draw(self.screen)
                                                pygame.display.flip()
                                        pygame.time.wait(2000)
                                        sound.stop()
                                    else:
                                        self.play_sound("biglose.mp3")
                                        self.screen.blit(self.biglose_img, (30, -50))
                                        pygame.time.wait(5)
                                        pygame.time.wait(5)

                                        self.font = pygame.font.Font(None, 100)
                                        result_text = self.font.render(f"-{int(self.current_bet)}", True,
                                                                       (23, 252, 255))
                                        self.screen.blit(result_text, (330, 295))
                                        self.font = pygame.font.Font(None, 36)

                                        self.all_sprites.update()
                                        self.all_sprites.draw(self.screen)
                                        pygame.display.flip()
                                        pygame.time.wait(2000)
                                self.calculate_coeff()

                                pygame.display.flip()
                                pygame.time.wait(700)
                                self.result = None
                                self.selected_side = None
                                self.input_text = ''

                if event.type == pygame.KEYDOWN and self.input_rect.collidepoint(pygame.mouse.get_pos()):
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if event.unicode.isdigit():
                            self.input_text += event.unicode

            # Отображение результата

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = CoinFlipGame()
    game.run()
