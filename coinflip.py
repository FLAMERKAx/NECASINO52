import random
import sqlite3
import sys

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
BLACK = (179, 167, 240)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BASE_COEFF = 1.75
MAX_COEFF = 2.95

GRAVITY = 0.5
screen_rect = pygame.Rect(-50, -50, WIDTH + 50, HEIGHT + 50)
all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def load_image(filename):
    try:
        image = pygame.image.load(filename)
        return image.convert_alpha()
    except pygame.error as e:
        print(f"Unable to load image: {filename}")
        raise SystemExit(e)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Particle(pygame.sprite.Sprite):
    def __init__(self, groups, pos, dx, dy):
        super().__init__(groups)
        self.image = pygame.image.load(r"coinflip\smallcoin.png")
        self.rect = self.image.get_rect(center=pos)
        self.velocity = [dx, dy]
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position, group, particle):
    particle_count = particle
    numbers = range(-30, 30)
    for _ in range(particle_count):
        Particle(group, position, random.choice(numbers), random.choice(numbers))


class CoinFlipGame:
    def __init__(self, money, id):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CoinFlip")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        pygame.mixer.init()

        self.user_id = id
        self.balance = money
        self.history = []
        self.current_bet = 0
        self.selected_side = None
        self.result = None
        self.streak = 0
        self.coeff = BASE_COEFF
        self.current_result = None

        self.background_img = pygame.image.load(r'coinflip\background.png')
        self.play_sound(r"coinflip\background.mp3", loop=True, volume=0.4)
        self.all_sprites = pygame.sprite.Group()

        self.coin_img = pygame.image.load(r'coinflip\coin.png').convert_alpha()
        self.coin_heads_img = pygame.image.load(r"coinflip\coinHeads.png").convert_alpha()
        self.coin_tails_img = pygame.image.load(r"coinflip\coinTails.png").convert_alpha()
        self.heads_img = pygame.image.load(r'coinflip\heads.png').convert_alpha()
        self.tails_img = pygame.image.load(r'coinflip\tails.png').convert_alpha()

        self.tailsbtn_img = pygame.image.load(r'coinflip\tailsbtn.png').convert_alpha()
        self.headsbtn_img = pygame.image.load(r'coinflip\headsbtn.png').convert_alpha()

        self.tailsbtnsel_img = pygame.image.load(r'coinflip\tailsbtnsel.png').convert_alpha()
        self.headsbtnsel_img = pygame.image.load(r'coinflip\headsbtnsel.png').convert_alpha()

        self.inputbox_img = pygame.image.load(r'coinflip\inputbox.png').convert_alpha()
        self.playbtn_img = pygame.image.load(r'coinflip\playbtn.png').convert_alpha()

        self.bigwin_img = pygame.image.load(r'coinflip\bigwin.png').convert_alpha()
        self.biglose_img = pygame.image.load(r'coinflip\biglose.png').convert_alpha()

        self.input_rect = pygame.Rect(205, 530, 200, 40)
        self.input_text = ''

    def calculate_coeff(self):
        if len(self.history) >= 2:
            if self.history[-1] == self.history[-2]:
                self.streak += 1
            else:
                self.streak = 0
        else:
            self.streak = 0
        self.coeff = min(BASE_COEFF + self.streak * 0.3, MAX_COEFF)
        if len(self.history) == 0:
            self.coeff = BASE_COEFF

    def play_sound(self, path, volume=0.5, loop=False):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        sound.play(loops=-1 if loop else 0)
        return sound

    def run(self):
        dragon = AnimatedSprite(load_image(r"coinflip\coin_sheet5x4v2.png"), 5, 4, 317, 233)
        running = True

        while running:
            self.screen.blit(self.background_img, (0, 0))

            # История
            for i, res in enumerate(self.history[-5:]):
                if res == "Heads":
                    self.screen.blit(self.heads_img, (100 + i * 60, 50))
                else:
                    self.screen.blit(self.tails_img, (100 + i * 60, 50))

            # Монета
            self.screen.blit(self.coin_img, (317, 233))

            # Кнопки выбора стороны
            heads_btn = pygame.Rect(200, 424, 150, 50)
            tails_btn = pygame.Rect(433, 424, 150, 50)
            self.screen.blit(self.tailsbtn_img if self.selected_side != 'Tails' else self.tailsbtnsel_img, tails_btn)
            self.screen.blit(self.headsbtn_img if self.selected_side != 'Heads' else self.headsbtnsel_img, heads_btn)

            # Поле ввода
            self.screen.blit(self.inputbox_img, self.input_rect)
            text_surf = self.font.render(self.input_text, True, BLACK)
            self.screen.blit(text_surf, (self.input_rect.x + 10, self.input_rect.y + 10))

            # Кнопка старта
            start_btn = pygame.Rect(413, 496, 210, 75)
            self.screen.blit(self.playbtn_img, start_btn)

            # Коэффицент и баланс
            coeff_text = self.font.render(f'Кэф: x{self.coeff:.2f}', True, BLACK)
            self.screen.blit(coeff_text, (WIDTH - 220, 80))
            balance_text = self.font.render(f'Баланс: ${self.balance}', True, BLACK)
            self.screen.blit(balance_text, (WIDTH - 220, 35))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sqlite_connection = sqlite3.connect('nebd52.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    cursor.execute(f"""UPDATE ludiki SET money = {self.balance}, coin = 1 WHERE id = {self.user_id};""")
                    sqlite_connection.commit()
                    cursor.close()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Определение стороны выбранной пользователем
                    if heads_btn.collidepoint(mouse_pos):
                        self.selected_side = 'Heads'
                    elif tails_btn.collidepoint(mouse_pos):
                        self.selected_side = 'Tails'

                    # Если выбрана сторона и ставка
                    elif start_btn.collidepoint(mouse_pos):
                        if self.selected_side and self.input_text:
                            self.current_bet = int(self.input_text)

                            if self.current_bet <= self.balance:
                                self.balance -= self.current_bet
                                result = random.choice(['Heads', 'Tails'])
                                self.history.append(result)

                                self.play_sound(r"coinflip\coin.mp3", volume=1)
                                for i in range(60):
                                    self.screen.blit(self.background_img, (0, 0))
                                    self.screen.blit(balance_text, (WIDTH - 220, 35))
                                    self.screen.blit(coeff_text, (WIDTH - 220, 80))
                                    self.screen.blit(self.playbtn_img, start_btn)
                                    self.screen.blit(text_surf, (self.input_rect.x + 10, self.input_rect.y + 10))
                                    self.screen.blit(self.inputbox_img, self.input_rect)
                                    self.screen.blit(
                                        self.tailsbtn_img if self.selected_side != 'Tails' else self.tailsbtnsel_img,
                                        tails_btn)
                                    self.screen.blit(
                                        self.headsbtn_img if self.selected_side != 'Heads' else self.headsbtnsel_img,
                                        heads_btn)
                                    for i, res in enumerate(self.history[-5:]):
                                        if res == "Heads":
                                            self.screen.blit(self.heads_img, (100 + i * 60, 50))
                                        else:
                                            self.screen.blit(self.tails_img, (100 + i * 60, 50))
                                    dragon.update()
                                    pygame.time.wait(15)
                                    all_sprites.draw(screen)
                                    pygame.display.flip()
                                self.screen.blit(
                                    self.coin_heads_img if self.selected_side == "Heads" else self.coin_tails_img,
                                    (317, 233))
                                self.play_sound(r"coinflip\coin_finish.mp3", volume=2)
                                pygame.time.wait(600)

                                # Отображение выигрыша или проигрыша
                                if (self.current_bet * self.coeff) < 2000:
                                    # Выигрыш
                                    if result == self.selected_side:
                                        self.balance += int(self.current_bet * self.coeff)
                                        result_text = self.font.render('Победа!', True, GREEN)
                                        self.screen.blit(result_text, (350, 150))
                                    # Проигрыш
                                    else:
                                        result_text = self.font.render('Поражение', True, RED)
                                        self.screen.blit(result_text, (330, 150))
                                # Большой выигрыш или проигрыш
                                else:
                                    # Выигрыш
                                    if result == self.selected_side:
                                        self.balance += int(self.current_bet * self.coeff)
                                        sound = self.play_sound(r"coinflip\bigwin.mp3", loop=True, volume=0.15)
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
                                                result_text = self.font.render(f"{int(self.current_bet * self.coeff)}",
                                                                               True, (243, 241, 41))
                                                self.screen.blit(result_text, (330, 295))
                                                self.font = pygame.font.Font(None, 36)

                                                self.all_sprites.update()
                                                self.all_sprites.draw(self.screen)
                                                pygame.display.flip()
                                        pygame.time.wait(2000)
                                        sound.stop()
                                    # Проигрыш
                                    else:
                                        self.play_sound(r"coinflip\biglose.mp3", volume=0.1)
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

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
