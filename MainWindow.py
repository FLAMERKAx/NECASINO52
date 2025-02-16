import sqlite3
import sys

import pygame

from coinflip import CoinFlipGame
from double import DoubleGame

pygame.init()

SMALL_FONT = pygame.font.SysFont("Comic Sans", 40)
LARGE_FONT = pygame.font.SysFont("Comic Sans", 100)

WHITE = (203, 195, 217)
YELLOW = (255, 172, 80)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
LIGHT_GREY = (200, 200, 200)
RED = (115, 51, 220)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 1080, 720
game_zone_rect = pygame.Rect(190, 250, 660, 300)
current_user = ""
current_money = 0
current_username = ""


class TextInputBox:
    def __init__(self, x, y, w, h, text='', font=SMALL_FONT):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = LIGHT_GREY
        self.text = text
        self.font = font
        self.txt_surface = font.render(text, True, WHITE)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если кликнули по полю ввода
            if self.rect.collidepoint(event.pos):
                # Активируем поле ввода
                self.active = True
            else:
                self.active = False
            # Изменяем цвет поля ввода при активации/деактивации
            self.color = RED if self.active else LIGHT_GREY
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Переопределяем поверхность текста
                self.txt_surface = self.font.render(self.text, True, WHITE)

    def update(self):
        # Ограничиваем ширину текста
        width = max(430, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Рисуем прямоугольник вокруг поля ввода
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # Выводим текст поверх прямоугольника
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


# Функция для отображения сообщения об ошибке
def show_error_message(screen, message, color=RED):
    error_msg = SMALL_FONT.render(message, True, color)
    rect = error_msg.get_rect(center=(WIDTH // 2, 300))
    screen.blit(error_msg, rect)


def main():
    global current_money, current_user, current_username
    registered_flag = False
    background_img = pygame.image.load(r'mainwindow\reg_background.png')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Регистрация")
    clock = pygame.time.Clock()

    # Поля ввода
    username_input = TextInputBox(587, 285, 0, 88)
    password_input = TextInputBox(587, 482, 11, 88)

    register_button = pygame.Rect(65, 345, 480, 100)
    register_img = pygame.image.load(r'mainwindow\signup_button.png').convert_alpha()
    login_button = pygame.Rect(65, 555, 480, 100)
    login_img = pygame.image.load(r'mainwindow\signin_button.png').convert_alpha()

    # Флаг для показа сообщения об ошибке
    show_error = False
    error_message = ""

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT and registered_flag:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.collidepoint(event.pos):
                    # Проверка заполненности полей
                    if len(username_input.text) == 0 or len(password_input.text) == 0:
                        show_error = True
                        error_message = "Пожалуйста, заполните все поля!"
                    else:

                        # Логика регистрации
                        sqlite_connection = sqlite3.connect('nebd52.db')
                        cursor = sqlite_connection.cursor()
                        print("Подключен к SQLite")
                        result = cursor.execute("""SELECT id, login, password, money FROM ludiki""").fetchall()
                        print(result)
                        for i in result:
                            if i[1] == username_input.text and i[2] == password_input.text:
                                current_username = i[1]
                                current_user = i[0]
                                current_money = i[3]
                                print(f"Имя пользователя: {username_input.text}")
                                print(f"Пароль: {password_input.text}")
                                registered_flag = True
                                msg = SMALL_FONT.render("Вы успешно Вошли!", True, GREEN)
                                rect = msg.get_rect(center=(WIDTH // 2, 300))
                                screen.blit(msg, rect)
                                pygame.display.flip()
                                pygame.time.wait(300)
                                break

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if register_button.collidepoint(event.pos):
                        # Проверка заполненности полей
                        if len(username_input.text) == 0 or len(password_input.text) == 0:
                            show_error = True
                            error_message = "Пожалуйста, заполните все поля!"
                        else:
                            # Логика регистрации
                            sqlite_connection = sqlite3.connect('nebd52.db')
                            cursor = sqlite_connection.cursor()
                            print("Подключен к SQLite")
                            result = cursor.execute("""SELECT id, login, money FROM ludiki""").fetchall()
                            print(result)
                            for i in result:
                                if i[1] == username_input.text:
                                    show_error = True
                                    error_message = "Такой пользователь уже зарегистрирован!"
                                    break
                                else:
                                    sqlite_insert_with_param = """INSERT INTO ludiki
                                                                              (login, password)
                                                                              VALUES (?, ?);"""

                                    data_tuple = (username_input.text, password_input.text)
                                    cursor.execute(sqlite_insert_with_param, data_tuple)
                                    sqlite_connection.commit()
                                    result = cursor.execute("""SELECT id, login, money FROM ludiki""").fetchall()
                                    if i[1] == username_input.text:
                                        current_username = i[1]
                                        current_user = i[0]
                                        current_money = i[2]
                                        print(f"Имя пользователя: {username_input.text}")
                                        print(f"Пароль: {password_input.text}")
                                        registered_flag = True
                                        msg = SMALL_FONT.render("Вы успешно Зарегистрировались!", True, GREEN)
                                        rect = msg.get_rect(center=(WIDTH // 2, 300))
                                        screen.blit(msg, rect)
                                        pygame.display.flip()
                                        pygame.time.wait(300)
                                        break

                            for i in result:
                                if i[1] == username_input.text:
                                    pass

                        # Тут можно добавить сохранение данных в файл или базу данных
            username_input.handle_event(event)
            password_input.handle_event(event)

        screen.blit(background_img, (0, 0))

        # Отображаем текстовые поля
        username_input.update()
        username_input.draw(screen)

        password_input.update()
        password_input.draw(screen)

        # Отображаем кнопку
        screen.blit(register_img, register_button)
        screen.blit(login_img, login_button)

        # Показываем сообщение об ошибке, если необходимо
        if show_error:
            show_error_message(screen, error_message)

        font = pygame.font.SysFont('Comic Sans', 24, bold=True)

        pygame.display.flip()
        clock.tick(30)


class MainWindow:
    def __init__(self):
        global current_money, current_user, current_username
        main()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("NECASINO52")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.victory_flag = False

        self.victory_balance_text = ""
        self.allgames_text = ""
        self.millionaire_text = ""

        pygame.mixer.init()

        self.background_img = pygame.image.load(r'mainwindow\background.png')

        self.char_idle_img = pygame.image.load(r'mainwindow\char_idle.png').convert_alpha()
        self.char_walk_left_1_img = pygame.image.load(r'mainwindow\char_walk_left_1.png').convert_alpha()
        self.char_walk_left_2_img = pygame.image.load(r'mainwindow\char_walk_left_2.png').convert_alpha()
        self.char_walk_right_1_img = pygame.image.load(r'mainwindow\char_walk_right_1.png').convert_alpha()
        self.char_walk_right_2_img = pygame.image.load(r'mainwindow\char_walk_right_2.png').convert_alpha()

        self.chair_top_img = pygame.image.load(r'mainwindow\chair_top.png').convert_alpha()
        self.chair_left_img = pygame.image.load(r'mainwindow\chair_left.png').convert_alpha()
        self.chair_left_down_img = pygame.image.load(r'mainwindow\chair_left_down.png').convert_alpha()
        self.chair_left_top_img = pygame.image.load(r'mainwindow\chair_left_top.png').convert_alpha()
        self.chair_right_img = pygame.image.load(r'mainwindow\chair_right.png').convert_alpha()
        self.chair_right_top_img = pygame.image.load(r'mainwindow\chair_right_top.png').convert_alpha()

        self.not_enough_money_img = pygame.image.load(r'mainwindow\not_enough_money.png').convert_alpha()
        self.end_screen_img = pygame.image.load(r'mainwindow\end_screen.png').convert_alpha()
        self.end_game_button_img = pygame.image.load(r'mainwindow\end_game_button.png').convert_alpha()
        self.exit_button_img = pygame.image.load(r'mainwindow\exit_button.png').convert_alpha()

        # self.play_sound("background.mp3", loop=True, volume=0.4)

        self.char_rect = pygame.Rect(485, 370, 40, 88)
        self.char_confirmation_rect = pygame.Rect(505, 390, 1, 1)

        self.chair_left_top_rect = pygame.Rect(290, 280, 58, 82)
        self.chair_top_rect = pygame.Rect(469, 288, 58, 82)
        self.chair_left_rect = pygame.Rect(225, 385, 58, 82)
        self.chair_left_down_rect = pygame.Rect(360, 480, 58, 82)
        self.chair_right_rect = pygame.Rect(772, 380, 58, 82)
        self.chair_right_top_rect = pygame.Rect(713, 300, 58, 82)

        self.not_enough_money_rect = pygame.Rect(445, 512, 58, 82)
        self.end_screen_rect = pygame.Rect(133, 44, 818, 584)
        self.exit_button_rect = pygame.Rect(0, 0, 296, 69)
        self.end_game_button_rect = pygame.Rect(0, 0, 154, 95)

    def draw_all(self):
        global game_zone_rect
        self.screen.blit(self.background_img, (0, 0))

        self.screen.blit(self.chair_left_top_img, self.chair_left_top_rect)
        self.screen.blit(self.chair_top_img, self.chair_top_rect)
        self.screen.blit(self.chair_left_img, self.chair_left_rect)
        self.screen.blit(self.chair_left_down_img, self.chair_left_down_rect)
        self.screen.blit(self.chair_right_img, self.chair_right_rect)
        self.screen.blit(self.chair_right_top_img, self.chair_right_top_rect)
        if current_money < 100000:
            self.screen.blit(self.not_enough_money_img, self.not_enough_money_rect)
        else:
            self.end_game_button_rect = pygame.Rect(460, 620, 154, 95)
            game_zone_rect = pygame.Rect(190, 250, 660, 600)
            self.screen.blit(self.end_game_button_img, self.end_game_button_rect)
        balance_text = self.font.render(f'Баланс: {current_money}', True, YELLOW)
        user_text = self.font.render(f'Пользователь: {current_username}', True, YELLOW)
        self.screen.blit(balance_text, (810, 30))
        self.screen.blit(user_text, (810, 70))

    def victory(self):
        self.screen.blit(self.end_screen_img, self.end_screen_rect)
        self.screen.blit(self.victory_balance_text, (352, 247))
        self.screen.blit(self.allgames_text, (352, 365))
        self.screen.blit(self.millionaire_text, (352, 447))
        self.char_rect = self.char_rect
        pygame.display.flip()

    def play_sound(self, path, volume=0.5, loop=False):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        sound.play(loops=-1 if loop else 0)
        return sound

    def run(self):
        global current_money, current_user
        running = True

        while running:

            self.draw_all()
            self.screen.blit(self.char_idle_img, self.char_rect)
            if self.victory_flag:
                self.screen.blit(self.exit_button_img, self.exit_button_rect)
                self.victory()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.exit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        if self.chair_left_top_rect.collidepoint(self.char_confirmation_rect[0],
                                                                 self.char_confirmation_rect[1]):
                            sqlite_connection = sqlite3.connect('nebd52.db')
                            cursor = sqlite_connection.cursor()
                            print("Подключен к SQLite")
                            result = cursor.execute("""SELECT id, login, password, money FROM ludiki""").fetchall()
                            print(result)
                            for i in result:
                                if i[1] == current_username:
                                    current_money = i[3]
                            coin = CoinFlipGame(current_money, current_user)
                            coin.run()

                        elif self.chair_right_rect.collidepoint(self.char_confirmation_rect[0],
                                                                self.char_confirmation_rect[1]):
                            sqlite_connection = sqlite3.connect('nebd52.db')
                            cursor = sqlite_connection.cursor()
                            print("Подключен к SQLite")
                            result = cursor.execute("""SELECT id, login, password, money FROM ludiki""").fetchall()
                            print(result)
                            for i in result:
                                if i[1] == current_username:
                                    current_money = i[3]
                            double = DoubleGame(current_money, current_user)
                            double.run_game()

                        elif self.end_game_button_rect.collidepoint(self.char_confirmation_rect[0],
                                                                    self.char_confirmation_rect[1]):
                            self.victory_flag = True
                            self.play_sound(r"mainwindow\victory.wav", volume=1)
                            millionaire = False
                            allgames = False
                            sqlite_connection = sqlite3.connect('nebd52.db')
                            cursor = sqlite_connection.cursor()
                            print("Подключен к SQLite")
                            result = cursor.execute(
                                """SELECT id, login, password, money, coin, sonic, roulette, luckyloot, tetris, hilo FROM ludiki""").fetchall()
                            for i in result:
                                if i[1] == current_username:
                                    self.victory_balance_text = self.font.render(f'{i[3]}', True, YELLOW)
                                    if i[3] >= 1000000:
                                        millionaire = True
                                    if i[4] and i[5] and i[6] and i[7] and i[8] and i[9]:
                                        allgames = True
                            if millionaire:
                                self.millionaire_text = self.font.render(f'Да!', True, YELLOW)
                            else:
                                self.millionaire_text = self.font.render(f'Нет...', True, YELLOW)
                            if allgames:
                                self.allgames_text = self.font.render(f'Да!', True, YELLOW)
                            else:
                                self.allgames_text = self.font.render(f'Нет...', True, YELLOW)
                            self.exit_button_rect = pygame.Rect(777, 640, 154, 95)



                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if game_zone_rect.collidepoint(self.char_rect[0], self.char_rect[1]):
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0], self.char_rect[1] - 20
                            self.char_confirmation_rect[0], self.char_confirmation_rect[1] = \
                            self.char_confirmation_rect[0], self.char_confirmation_rect[1] - 20
                        else:
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0], self.char_rect[1] + 40
                            self.char_confirmation_rect[0], self.char_confirmation_rect[1] = \
                            self.char_confirmation_rect[0], self.char_confirmation_rect[1] + 40
                        for _ in range(2):
                            self.draw_all()
                            self.screen.blit(self.char_idle_img, self.char_rect)
                            pygame.display.flip()
                            pygame.time.wait(50)
                            pygame.display.flip()
                    if event.key == pygame.K_d:
                        if game_zone_rect.collidepoint(self.char_rect[0], self.char_rect[1]):
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0] + 40, self.char_rect[1]
                            self.char_confirmation_rect[0], self.char_confirmation_rect[1] = \
                            self.char_confirmation_rect[0] + 40, self.char_confirmation_rect[1]
                        else:
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0] - 60, self.char_rect[1]
                            self.char_confirmation_rect[0], self.char_confirmation_rect[1] = \
                            self.char_confirmation_rect[0] - 60, self.char_confirmation_rect[1]
                        for _ in range(2):
                            self.draw_all()
                            self.screen.blit(self.char_walk_right_1_img, self.char_rect)
                            pygame.display.flip()
                            pygame.time.wait(25)
                            print(self.char_rect[0], self.char_rect[1])
                            self.draw_all()
                            self.screen.blit(self.char_walk_right_2_img, self.char_rect)
                            pygame.display.flip()
                            pygame.time.wait(25)
                    if event.key == pygame.K_a:
                        if game_zone_rect.collidepoint(self.char_rect[0], self.char_rect[1]):
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0] - 40, self.char_rect[1]
                            self.char_confirmation_rect[0], self.char_confirmation_rect[1] = \
                            self.char_confirmation_rect[0] - 40, self.char_confirmation_rect[1]
                        else:
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0] + 60, self.char_rect[1]
                            self.char_confirmation_rect[0], self.char_confirmation_rect[1] = \
                            self.char_confirmation_rect[0] + 60, self.char_confirmation_rect[1]
                        for _ in range(2):
                            self.draw_all()
                            self.screen.blit(self.char_walk_left_1_img, self.char_rect)
                            pygame.display.flip()
                            pygame.time.wait(25)
                            self.draw_all()
                            self.screen.blit(self.char_walk_left_2_img, self.char_rect)
                            pygame.display.flip()
                            pygame.time.wait(25)
                    if event.key == pygame.K_s:
                        if game_zone_rect.collidepoint(self.char_rect[0], self.char_rect[1]):
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0], self.char_rect[1] + 20
                            self.char_confirmation_rect[0], self.char_confirmation_rect[1] = \
                            self.char_confirmation_rect[0], self.char_confirmation_rect[1] + 20
                        else:
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0], self.char_rect[1] - 40
                            self.char_confirmation_rect[0], self.char_confirmation_rect[1] = \
                            self.char_confirmation_rect[0], self.char_confirmation_rect[1] - 40
                        for _ in range(2):
                            self.draw_all()
                            self.screen.blit(self.char_idle_img, self.char_rect)
                            pygame.display.flip()
                            pygame.time.wait(50)
                            pygame.display.flip()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = MainWindow()
    game.run()
