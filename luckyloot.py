import random
import sqlite3
import pygame
import pygame_gui


class LuckyLootGame():
    def __init__(self, money, user_id):
        main_number = random.randint(5, 50)
        self.user_number = 0
        point_number = 1000
        self.balance = money
        self.user_id = user_id

        pygame.init()
        pygame.display.set_caption('Start')
        window_surface = pygame.display.set_mode((800, 600))

        background = pygame.Surface((800, 600))
        color = 'white'
        background.fill(pygame.Color(color))
        manager = pygame_gui.UIManager((800, 600))

        switch = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 270), (100, 50)),
            text='ФОН'
        )
        plus = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((120, 475), (100, 50)),
            text='прибавить'
        )
        skip = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 475), (100, 50)),
            text='пропуск'
        )
        user_number_label = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100, 100), (100, 250)),
            text='0',
            manager=manager
        )
        user_number_label2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((600, 100), (100, 250)),
            text=str(main_number),
            manager=manager
        )
        user_number_label3 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((275, 100), (250, 100)),
            text=str(point_number),
            manager=manager
        )

        clock = pygame.time.Clock()
        run = True

        while run:

            time_delta = clock.tick(60) / 1000
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False
                    sqlite_connection = sqlite3.connect('nebd52.db')
                    cursor = sqlite_connection.cursor()
                    print("Подключен к SQLite")
                    cursor.execute(f"""UPDATE ludiki SET money = {self.balance}, luckyloot = 1 WHERE id = {self.user_id};""")
                    sqlite_connection.commit()
                    cursor.close()
                    pygame.quit()
                    confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((250, 200), (300, 200)),
                        manager=manager,
                        window_title='Подтверждение',
                        action_long_desc='Вы уверены, что хотите выйти?',
                        action_short_name='ОК',
                        blocking=True
                    )
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        run = False
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == switch:
                            if color == 'grey':
                                color = 'white'
                            else:
                                color = 'grey'
                            background.fill(pygame.Color(color))

                        if event.ui_element == skip:
                            if point_number > 1000:
                                confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                                    rect=pygame.Rect((250, 200), (400, 400)),
                                    manager=manager,
                                    window_title='Подтверждение',
                                    action_long_desc='ВЫ ВЫЙГРАЛИ',
                                    action_short_name='ОК',
                                    blocking=True
                                )
                            if point_number < 1000:
                                confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                                    rect=pygame.Rect((250, 200), (400, 400)),
                                    manager=manager,
                                    window_title='Подтверждение',
                                    action_long_desc='ВЫ ПРОИГРАЛИ',
                                    action_short_name='ОК',
                                    blocking=True
                                )

                        if event.ui_element == plus:
                            self.add_user_number()
                            user_number_label.set_text(str(self.user_number))
                            if self.user_number < 20:
                                point_number = 500
                                user_number_label3.set_text(str(point_number))
                            if self.user_number > 20:
                                point_number = 1250
                                user_number_label3.set_text(str(point_number))
                            if self.user_number > main_number:

                                confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                                    rect=pygame.Rect((250, 200), (400, 400)),
                                    manager=manager,
                                    window_title='Подтверждение',
                                    action_long_desc='ВЫ ПРОИГРАЛИ',
                                    action_short_name='ОК',
                                    blocking=True
                                )

                manager.process_events(event)
            manager.update(time_delta)
            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)
            pygame.display.update()

    def add_user_number(self):
        self.user_number += random.randint(0, 6)
