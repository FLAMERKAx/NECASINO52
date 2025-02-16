import pygame
import sys
import random
import sqlite3


# Класс игры
class DoubleGame():
    def __init__(self, money, id):
        # Инициализация Pygame
        pygame.init()
        pygame.mixer.init()
        # Создание окна
        self.screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Double Game")

        # Основные параметры
        self.user_id = id

        self.bg_color = (101, 53, 155)
        self.num_fields = 50
        self.field_width = 50
        self.field_height = 50
        self.scroll_speed = 7  # Скорость прокрутки
        self.offset_x = 0  # Смещение по оси X

        # Список для генерации рулетки
        self.lst = []  # Начальный пустой список

        # Переменная для отслеживания состояния вращения
        self.is_spinning = False

        self.clck = 0

        # Часы для управления частотой кадров
        self.clock = pygame.time.Clock()

        # Флаги для управления паузами и выбором цвета
        self.paused = False
        self.color_selected = None

        # Переменная для счета кликов
        self.click_count = 0

        self.win = None

        # Баланс игрока
        self.balance = money

        # Текущая ставка
        self.current_bet = 0

        # Переменная для текста предупреждения
        self.warning_text = None

        self.background = pygame.image.load(r"double\background.png").convert_alpha()
        self.spin_button_img = pygame.image.load(r"double\spin_button.png").convert_alpha()
        self.spin_button_inactive_img = pygame.image.load(r"double\spin_button_inactive.png").convert_alpha()

        self.red_button_clicked_img = pygame.image.load(r"double\red_button_clicked.png").convert_alpha()
        self.red_button_inactive_img = pygame.image.load(r"double\red_button.png").convert_alpha()

        self.black_button_clicked_img = pygame.image.load(r"double\black_button_clicked.png").convert_alpha()
        self.black_button_inactive_img = pygame.image.load(r"double\black_button.png").convert_alpha()

    def play_sound(self, path, volume=0.5, loop=False):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        sound.play(loops=-1 if loop else 0)
        return sound

    # Функция создания массива с 1 и 0 для отображения красных и черных полей
    def generate_roulette(self):
        self.a = random.randint(10, 45)
        self.lst = []
        for i in range(self.num_fields):
            if i % 2 == 0:
                self.lst.append(0)
            else:
                self.lst.append(1)

    # Отображение рулетки
    def draw_roulette(self):
        x_pos = self.offset_x
        y_pos = 200  # начальная позиция по вертикали
        pygame.draw.rect(self.screen, "grey", (1, 175, self.screen.get_width(), 100), 0)
        points = [(300, 250), (275, 300), (325, 300)]
        pygame.draw.polygon(self.screen, (0, 128, 255), points)
        font = pygame.font.SysFont('Comic sans', 32, bold=True)
        for index, value in enumerate(self.lst):
            color = "red" if value == 0 else "black"
            rect = pygame.Rect(x_pos, y_pos, self.field_width, self.field_height)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, 'white', rect, 1)
            x_pos += self.field_width + 11

    # Обновление смещения
    def update_offset(self):
        if hasattr(self, 'lst') and len(self.lst) > 0:
            if self.offset_x <= -(self.field_width + 10) * (len(self.lst) - self.a):
                self.offset_x = -(self.field_width + 10) * (len(self.lst) - self.a)
                self.is_spinning = False

                # Определяем последний видимый индекс
                last_visible_index = int(-self.offset_x // (self.field_width + 11)) % len(self.lst)

                # Получаем значение (0 или 1) для определения цвета
                result_value = self.lst[last_visible_index]

                # Проверяем результат
                if result_value == self.color_selected:
                    self.win = True
                    self.balance += self.current_bet  # Увеличиваем баланс при выигрыше
                else:
                    self.win = False
                    self.balance -= self.current_bet  # Уменьшаем баланс при проигрыше

                print(int(result_value), int(self.color_selected))

            else:
                self.offset_x -= self.scroll_speed

    # Отображение кнопки Spin
    def draw_button_spin(self):
        button_rect = pygame.Rect(210, 320, 150, 50)

        # Меняем цвет кнопки в зависимости от состояния is_spinning
        if self.is_spinning:
            self.screen.blit(self.spin_button_inactive_img, button_rect)
        else:
            self.screen.blit(self.spin_button_img, button_rect)


    def draw_color_buttons(self):
        black_rect = pygame.Rect(35, 320, 150, 50)
        red_rect = pygame.Rect(385, 320, 150, 50)
        if self.color_selected == 0:
            self.screen.blit(self.black_button_clicked_img, black_rect)
            self.screen.blit(self.red_button_inactive_img, red_rect)
        elif self.color_selected == 1:
            self.screen.blit(self.red_button_clicked_img, red_rect)
            self.screen.blit(self.black_button_inactive_img, black_rect)
        else:
            self.screen.blit(self.black_button_inactive_img, black_rect)
            self.screen.blit(self.red_button_inactive_img, red_rect)

    # Проверка клика по кнопкам выбора цвета
    def check_color_button_click(self, pos, size_x, size_y):
        button_rect = pygame.Rect(size_x, size_y, 150, 50)
        if not self.is_spinning and button_rect.collidepoint(pos):
            return True

    # Проверка клика по кнопке Spin
    def check_button_click(self, pos, size_x, size_y):
        button_rect = pygame.Rect(size_x, size_y, 150, 50)
        if not self.is_spinning and button_rect.collidepoint(pos):
            return True

    # Отображает текущий баланс
    def display_balance(self):
        font = pygame.font.SysFont('Arial', 24)
        balance_text = f"{self.balance}"
        text_surface = font.render(balance_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (120, 24))

    # Поле ввода для ставки
    def bet_input_field(self):
        input_rect = pygame.Rect(348, 27, 140, 34)
        pygame.draw.rect(self.screen, (230, 230, 230), input_rect)
        font = pygame.font.SysFont('Arial', 16)
        bet_text = font.render(str(self.current_bet), True, (0, 0, 0))
        self.screen.blit(bet_text, (input_rect.x + 5, input_rect.y + 8))
        pygame.draw.rect(self.screen, (0, 0, 0), input_rect, 2)

    # Основной игровой цикл
    def run_game(self):
        # Флаг для управления главным циклом
        running = True

        # Главный игровой цикл
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sqlite_connection = sqlite3.connect('nebd52.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    cursor.execute(f"""UPDATE ludiki SET money = {self.balance}, roulette = 1 WHERE id = {self.user_id};""")
                    sqlite_connection.commit()
                    cursor.close()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.check_color_button_click(mouse_pos, 75, 325):
                        self.color_selected = 0
                    elif self.check_color_button_click(mouse_pos, 375, 325):
                        self.color_selected = 1
                    elif not self.is_spinning and self.check_button_click(mouse_pos, 225, 325):
                        self.clck += 1
                        self.warning_text = None  # Сбрасываем предупреждение перед проверкой
                        if self.color_selected is not None:
                            if self.balance >= self.current_bet > 0:
                                self.generate_roulette()  # Генерируем новую рулетку
                                self.is_spinning = True
                                self.play_sound(r"double\roulette.mp3", volume=0.5)
                                self.offset_x = 0
                                self.click_count += 1
                            else:
                                self.warning_text = "Ставка должна быть больше нуля и не превышать ваш баланс."
                        else:
                            self.warning_text = "Ставка на цвет не сделана"
                elif event.type == pygame.KEYDOWN:
                    # Игнорируем ввод ставки во время спина
                    if not self.is_spinning:
                        if event.key == pygame.K_BACKSPACE:
                            if len(str(self.current_bet)) > 1:
                                self.current_bet = int(str(self.current_bet)[:-1])
                            else:
                                self.current_bet = 0
                        else:
                            try:
                                new_char = int(event.unicode)
                                if new_char >= 0:
                                    self.current_bet *= 10  # Умножаем текущую ставку на 10
                                    self.current_bet += new_char  # Добавляем новую цифру
                            except ValueError:
                                pass

            # Ограничиваем частоту кадров
            self.clock.tick(60)
            # Очистка экрана перед каждой итерацией игрового цикла
            self.screen.blit(self.background, (0, 0))
            # self.screen.fill(self.bg_color)

            # Отображение сообщений о результате
            font = pygame.font.SysFont('Comic sans', 22, bold=True)
            if self.clck > 0:
                if self.win:
                    text = font.render("Поздравляю! Вы победили", True, ('green'))
                    self.screen.blit(text, (155, 140))
                elif self.win == None:
                    pass
                else:
                    text = font.render("Поражение, в следующий раз повезет", True, ('red'))
                    self.screen.blit(text, (80, 140))

            # Отображение рулетки
            if self.lst and self.is_spinning:
                self.update_offset()
                self.draw_roulette()

            # Отображение кнопок
            if self.lst:
                self.draw_roulette()

            self.draw_color_buttons()
            self.draw_button_spin()
            self.bet_input_field()
            self.display_balance()

            # Отображение предупреждения
            if self.warning_text:
                x_cord = 0
                if len(self.warning_text) == 25:
                    x_cord = 180
                else:
                    x_cord = 20
                pygame.draw.rect(self.screen, (101, 53, 155), (1, 115, self.screen.get_width(), 200), 0)
                # Если есть предупреждение, отображаем его
                font = pygame.font.SysFont('Arial', 18, bold=True)
                text_surface = font.render(self.warning_text, True, 'red')
                self.screen.blit(text_surface, (x_cord, 200))

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = DoubleGame()
    game.run_game()