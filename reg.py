import pygame
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Размеры окна
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
LIGHT_GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Шрифты
SMALL_FONT = pygame.font.SysFont("Comic Sans", 16)
LARGE_FONT = pygame.font.SysFont("Comic Sans", 24)

# Класс для текстового поля ввода
class TextInputBox:
    def __init__(self, x, y, w, h, text='', font=SMALL_FONT):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = LIGHT_GREY
        self.text = text
        self.font = font
        self.txt_surface = font.render(text, True, BLACK)
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
            self.color = GREEN if self.active else LIGHT_GREY
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
                self.txt_surface = self.font.render(self.text, True, BLACK)

    def update(self):
        # Ограничиваем ширину текста
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Рисуем прямоугольник вокруг поля ввода
        pygame.draw.rect(screen, self.color, self.rect, 2)
        # Выводим текст поверх прямоугольника
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))


# Функция для отображения сообщения об ошибке
def show_error_message(screen, message, color=RED):
    error_msg = LARGE_FONT.render(message, True, color)
    rect = error_msg.get_rect(center=(SCREEN_WIDTH // 2, 300))
    screen.blit(error_msg, rect)

# Основная функция
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Регистрация")
    clock = pygame.time.Clock()

    # Поля ввода
    username_input = TextInputBox(225, 120, 140, 32)
    password_input = TextInputBox(225, 170, 140, 32)

    # Кнопка "Зарегистрироваться"
    register_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, 230, 150, 40)

    # Флаг для показа сообщения об ошибке
    show_error = False
    error_message = ""

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
                        # Тут можно добавить сохранение данных в файл или базу данных
                        done = True
            username_input.handle_event(event)
            password_input.handle_event(event)

        screen.fill(WHITE)

        # Отображаем заголовок
        title_text = LARGE_FONT.render("Регистрация", True, BLACK)
        screen.blit(title_text, (160, 60))

        # Отображаем текстовые поля
        username_label = SMALL_FONT.render("Имя пользователя:", True, BLACK)
        screen.blit(username_label, (80, 125))
        username_input.update()
        username_input.draw(screen)

        password_label = SMALL_FONT.render("Пароль:", True, BLACK)
        screen.blit(password_label, (160, 175))
        password_input.update()
        password_input.draw(screen)

        # Отображаем кнопку
        pygame.draw.rect(screen, GREY, register_button)
        button_text = SMALL_FONT.render("Зарегистрироваться", True, WHITE)
        screen.blit(button_text, (register_button.centerx - button_text.get_width() // 2,
                                  register_button.centery - button_text.get_height() // 2))

        # Показываем сообщение об ошибке, если необходимо
        if show_error:
            show_error_message(screen, error_message)



        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()