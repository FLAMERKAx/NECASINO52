import sys
import sqlite3
import pygame

pygame.init()

SMALL_FONT = pygame.font.SysFont("Comic Sans", 40)
LARGE_FONT = pygame.font.SysFont("Comic Sans", 100)

WHITE = (203, 195, 217)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
LIGHT_GREY = (200, 200, 200)
RED = (115, 51, 220)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 1080, 720
game_zone_rect = pygame.Rect(205, 270, 640, 280)


class TextInputBox:
    def __init__(self, x, y, w, h, text='', font=SMALL_FONT):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = LIGHT_GREY
        self.text = text
        self.font = font
        self.txt_surface = font.render(text, True, WHITE)
        self.active = False
        self.greeting = 'NECASINO52'

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
    error_msg = LARGE_FONT.render(message, True, color)
    rect = error_msg.get_rect(center=(WIDTH // 2, 300))
    screen.blit(error_msg, rect)


def main():
    registered_flag = False
    background_img = pygame.image.load('reg_background.png')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Регистрация")
    clock = pygame.time.Clock()


    # Поля ввода
    username_input = TextInputBox(587, 285, 0, 88)
    password_input = TextInputBox(587, 482, 11, 88)

    register_button = pygame.Rect(65, 345, 480, 100)
    register_img = pygame.image.load('signup_button.png').convert_alpha()
    login_button = pygame.Rect(65, 555, 480, 100)
    login_img = pygame.image.load('signin_button.png').convert_alpha()

    # Флаг для показа сообщения об ошибке
    show_error = False
    error_message = ""

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT and registered_flag:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if register_button.collidepoint(event.pos):
                    # Проверка заполненности полей
                    if len(username_input.text) == 0 or len(password_input.text) == 0:
                        show_error = True
                        error_message = "Пожалуйста, заполните все поля!"
                    else:
                        # Логика регистрации
                        print(f"Имя пользователя: {username_input.text}")
                        print(f"Пароль: {password_input.text}")
                        sqlite_connection = sqlite3.connect('nebd52.db')
                        cursor = sqlite_connection.cursor()
                        print("Подключен к SQLite")

                        sqlite_insert_with_param = """INSERT INTO ludiki
                                                                  (username, password)
                                                                  VALUES (?, ?);"""

                        data_tuple = (username_input.text, password_input.text)
                        cursor.execute(sqlite_insert_with_param, data_tuple)
                        sqlite_connection.commit()
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

class CoinFlipGame:
    def __init__(self):
        main()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CoinFlip")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        pygame.mixer.init()

        self.background_img = pygame.image.load('background.png')
        self.game_zone_img = pygame.image.load("game_zone.png")

        self.char_idle_img = pygame.image.load('char_idle.png').convert_alpha()
        self.char_walk_left_1_img = pygame.image.load('char_walk_left_1.png').convert_alpha()
        self.char_walk_left_2_img = pygame.image.load('char_walk_left_2.png').convert_alpha()
        self.char_walk_right_1_img = pygame.image.load('char_walk_right_1.png').convert_alpha()
        self.char_walk_right_2_img = pygame.image.load('char_walk_right_2.png').convert_alpha()

        self.chair_top_img = pygame.image.load('chair_top.png').convert_alpha()
        self.chair_left_img = pygame.image.load('chair_left.png').convert_alpha()
        self.chair_left_top_img = pygame.image.load('chair_left_top.png').convert_alpha()
        self.chair_right_img = pygame.image.load('chair_right.png').convert_alpha()
        self.chair_right_top_img = pygame.image.load('chair_right_top.png').convert_alpha()

        self.not_enough_money_img = pygame.image.load('not_enough_money.png').convert_alpha()
        self.end_screen_img = pygame.image.load('end_screen.png').convert_alpha()
        self.end_game_button_img = pygame.image.load('end_game_button.png').convert_alpha()
        self.exit_button_img = pygame.image.load('exit_button.png').convert_alpha()

        # self.play_sound("background.mp3", loop=True, volume=0.4)

        self.char_rect = pygame.Rect(485, 370, 40, 88)

    def play_sound(self, path, volume=0.5, loop=False):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        sound.play(loops=-1 if loop else 0)
        return sound

    def run(self):


        running = True

        while running:

            self.screen.blit(self.background_img, (0, 0))
            self.screen.blit(self.char_idle_img, self.char_rect)
            self.screen.blit(self.game_zone_img, game_zone_rect)

            #
            # tails_btn = pygame.Rect(433, 424, 150, 50)
            # self.screen.blit(self.tailsbtn_img if self.selected_side != 'Tails' else self.tailsbtnsel_img, tails_btn)
            #
            # coeff_text = self.font.render(f'Кэф: x{self.coeff:.2f}', True, BLACK)
            # self.screen.blit(coeff_text, (WIDTH - 220, 80))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                #     # Определение стороны выбранной пользователем
                #     if heads_btn.collidepoint(mouse_pos):
                #         self.selected_side = 'Heads'
                #     elif tails_btn.collidepoint(mouse_pos):
                #         self.selected_side = 'Tails'
                #
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if game_zone_rect.collidepoint(self.char_rect[0], self.char_rect[1]):
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0], self.char_rect[1] - 40
                        else:
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0], self.char_rect[1] + 80
                        for _ in range(2):
                            self.screen.blit(self.background_img, (0, 0))
                            self.screen.blit(self.char_idle_img, self.char_rect)
                            pygame.display.flip()
                            pygame.time.wait(50)
                            pygame.display.flip()
                    if event.key == pygame.K_d:
                        if game_zone_rect.collidepoint(self.char_rect[0], self.char_rect[1]):
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0] + 40, self.char_rect[1]
                        else:
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0] - 80, self.char_rect[1]
                        for _ in range(2):
                            self.screen.blit(self.background_img, (0, 0))
                            self.screen.blit(self.char_walk_right_1_img, self.char_rect)
                            pygame.display.flip()
                            pygame.time.wait(25)
                            print(self.char_rect[0], self.char_rect[1])
                            self.screen.blit(self.background_img, (0, 0))
                            self.screen.blit(self.char_walk_right_2_img, self.char_rect)
                            pygame.display.flip()
                            pygame.time.wait(25)
                    if event.key == pygame.K_a:
                        if game_zone_rect.collidepoint(self.char_rect[0], self.char_rect[1]):
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0] - 40, self.char_rect[1]
                        else:
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0] + 80, self.char_rect[1]
                        for _ in range(2):
                            self.screen.blit(self.background_img, (0, 0))
                            self.screen.blit(self.char_walk_left_1_img, self.char_rect)
                            pygame.display.flip()
                            pygame.time.wait(25)
                            self.screen.blit(self.background_img, (0, 0))
                            self.screen.blit(self.char_walk_left_2_img, self.char_rect)
                            pygame.display.flip()
                            pygame.time.wait(25)
                    if event.key == pygame.K_s:
                        if game_zone_rect.collidepoint(self.char_rect[0], self.char_rect[1]):
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0], self.char_rect[1] + 20
                        else:
                            self.char_rect[0], self.char_rect[1] = self.char_rect[0], self.char_rect[1] - 80
                        for _ in range(2):
                            self.screen.blit(self.background_img, (0, 0))
                            self.screen.blit(self.char_idle_img, self.char_rect)
                            pygame.display.flip()
                            pygame.time.wait(50)
                            pygame.display.flip()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = CoinFlipGame()
    game.run()
