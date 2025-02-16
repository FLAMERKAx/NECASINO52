import pygame
import os
import sys
import random
import playsound3
import sqlite3


WIDTH = 800
HEIGHT = 600
PLAY = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
BAD_OBJECT = ['background.png', 'equl.png', 'up.png', 'down.png']
game_win_lose = []
list_rect = []




class HiloGame:
    def __init__(self, money, user_id):
        playsound3.playsound(r'hilo\background_music.mp3', False)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("HILO")
        self.balance = money
        self.user_id = user_id
        self.bet_amount = 10

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('PerfectDOSVGA437', 36)
        self.running = True

        self.name = random.choice(os.listdir(r'hilo\data'))
        while self.name in BAD_OBJECT:
            self.name = random.choice(os.listdir(r'hilo\data'))

        self.card = self.load_image(self.name)
        self.name = self.name.split('_')[1].split('.')[0]

        high = (len(PLAY[PLAY.index(self.name) + 1:]) * 4 / 52)
        self.coeff_plus = str(round(1 / high, 2)) if high > 0 else '0'
        low = (len(PLAY[:PLAY.index(self.name)]) * 4 / 52)
        self.coeff_minus = str(round(1 / low, 2)) if low > 0 else '0'
        self.coeff_equl = str(round(1 / (4 / 52), 2))

        self.DICT_COEFF = {0: self.coeff_plus, 1: self.coeff_minus, 2: self.coeff_equl}

        self.font = pygame.font.SysFont('Comic Sans', 46, bold=True)
        up = self.load_image(r'up.png')
        list_rect.append(pygame.Rect(250, 494, 102, 102))
        down = self.load_image(r'down.png')
        list_rect.append(pygame.Rect(450, 494, 102, 102))
        eq = self.load_image(r'equl.png')
        list_rect.append(pygame.Rect(350, 494, 102, 102))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sqlite_connection = sqlite3.connect('nebd52.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    cursor.execute(f"""UPDATE ludiki SET money = {self.balance}, hilo = 1 WHERE id = {self.user_id};""")
                    sqlite_connection.commit()
                    cursor.close()
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for el in list_rect:
                        if el.collidepoint(event.pos):
                            last_name = self.name
                            self.cards_swap()
                            if list_rect.index(el) == 0 and PLAY[PLAY.index(last_name)] > PLAY[PLAY.index(self.name)]:
                                game_win_lose.append('win')
                                self.balance += int(self.bet_amount * float(self.coeff_plus))
                            elif list_rect.index(el) == 1 and PLAY[PLAY.index(last_name)] < PLAY[PLAY.index(self.name)]:
                                game_win_lose.append('win')
                                self.balance += int(self.bet_amount * float(self.coeff_minus))
                            elif list_rect.index(el) == 2 and PLAY[PLAY.index(last_name)] == PLAY[PLAY.index(self.name)]:
                                game_win_lose.append('win')
                                self.balance += int(self.bet_amount * float(self.coeff_equl))
                            else:
                                game_win_lose.append('lose')
                                self.balance -= int(self.bet_amount * float(self.DICT_COEFF[list_rect.index(el)]))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(str(self.bet_amount)) > 1:
                            self.bet_amount = int(str(self.bet_amount)[:-1])
                        else:
                            self.bet_amount = 0
                    else:
                        try:
                            new_char = int(event.unicode)
                            if new_char >= 0 and self.balance >= self.bet_amount * 10 + new_char:
                                self.bet_amount *= 10
                                self.bet_amount += new_char
                        except ValueError:
                            pass

            self.BackGround()
            self.bet_input_field()
            self.draw_text('><=', (0, 0, 0), 110, 420)
            self.draw_text(self.coeff_plus, (0, 0, 0), 110, 470)
            self.draw_text(self.coeff_minus, (0, 0, 0), 110, 520)
            self.draw_text(self.coeff_equl, (0, 0, 0), 110, 570)

            self.draw_text('NECASINO52', (0, 0, 0), 350, 55)
            self.draw_text('NECASINO52', (255, 255, 0), 350, 50)

            self.draw_text(f'cash:', (0, 0, 0), 625, 325)
            self.draw_text(f'{self.balance}', (0, 0, 0), 625, 380)
            self.draw_text(f'{self.balance}', (0, 255, 255), 625, 375)

            self.screen.blit(pygame.transform.scale(up, (up.get_width() / 5, up.get_height() / 5)), (250, 494))

            self.screen.blit(pygame.transform.scale(down, (down.get_width() / 5, down.get_height() / 5)), (450, 494))

            self.screen.blit(pygame.transform.scale(eq, (down.get_width() / 5, down.get_height() / 5)), (350, 494))
            self.screen.blit(self.card, (280, 150))
            pygame.display.flip()
            self.clock.tick(30)
            if self.balance < 0:
                os.startfile(r'hilo\end.mp4')
                break

    def load_image(self, name, images=False):
        if images:
            fullname = os.path.join(r'hilo\images.png', name)
        else:
            fullname = os.path.join(r'hilo\data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    def BackGround(self):
        back = self.load_image(r'background.png')
        self.screen.blit(back, (0, 0))
        T1, T2 = self.load_image(r'39.png', images=True), self.load_image(r'52.png', images=True)
        T1 = pygame.transform.rotate(T1, 30)
        T2 = pygame.transform.rotate(T2, 35)

        many_f = self.load_image(r'многа фишек.png', images=True)
        many_f = pygame.transform.scale(many_f, (many_f.get_width() * 1.5, many_f.get_height() * 1.5))

        deck_of_card = self.load_image(r'карты.png', images=True)
        deck_of_card = pygame.transform.scale(deck_of_card, (deck_of_card.get_width() * 2, deck_of_card.get_height() * 2))

        rol = self.load_image(r'roulet.png', images=True)

        hand = self.load_image(r'hand.png', images=True)
        hand = pygame.transform.scale(hand, (hand.get_width() * 1.5, hand.get_height() * 1.5))

        phone = self.load_image(r'phone.png', images=True)
        phone = pygame.transform.scale(phone, (phone.get_width() / 2, phone.get_height() / 2))

        self.screen.blit(hand, (0, 250))
        self.screen.blit(rol, (500, -200))
        self.screen.blit(deck_of_card, (250, 250))
        self.screen.blit(T1, (700, 430))
        self.screen.blit(T2, (700, 400))
        self.screen.blit(many_f, (600, 520))
        self.screen.blit(many_f, (670, 520))
        self.screen.blit(phone, (535, 200))

    def cards_swap(self):
        k = random.choice(os.listdir(r'hilo\data'))
        while k in BAD_OBJECT:
            k = random.choice(os.listdir(r'hilo\data'))
        self.name = k
        self.card = self.load_image(k)
        self.name = self.name.split('_')[1].split('.')[0]
        high = (len(PLAY[PLAY.index(self.name) + 1:]) * 4 / 52)
        self.coeff_plus = str(round(1 / high, 2)) if high > 0 else '0'
        low = (len(PLAY[:PLAY.index(self.name)]) * 4 / 52)
        self.coeff_minus = str(round(1 / low, 2)) if low > 0 else '0'
        self.coeff_equl = str(round(1 / (4 / 52), 2))

    def draw_text(self, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def bet_input_field(self):
        input_rect = pygame.Rect(333, 110, 140, 32)
        pygame.draw.rect(self.screen, (230, 230, 230), input_rect)
        font = pygame.font.SysFont('Comic Sans', 16)
        bet_text = font.render(str(self.bet_amount), True, (0, 0, 0))
        self.screen.blit(bet_text, (input_rect.x + 5, input_rect.y + 8))
        pygame.draw.rect(self.screen, (0, 0, 0), input_rect, 2)


if __name__ == "__main__":
    game = HiloGame()