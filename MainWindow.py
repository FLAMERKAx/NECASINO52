import sys

import pygame

pygame.init()

WIDTH, HEIGHT = 1080, 720
BLACK = (179, 167, 240)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
INITIAL_BALANCE = 1000
BASE_COEFF = 1.75
MAX_COEFF = 2.95

GRAVITY = 0.5
screen_rect = pygame.Rect(-50, -50, WIDTH + 50, HEIGHT + 50)
all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class CoinFlipGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CoinFlip")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        pygame.mixer.init()

        self.background_img = pygame.image.load('background.png')

        self.background_img = pygame.image.load('char_idle.png').convert_alpha()
        self.background_img = pygame.image.load('char_walk_left_1.png').convert_alpha()
        self.background_img = pygame.image.load('char_walk_left_2.png').convert_alpha()
        self.background_img = pygame.image.load('char_walk_right_1.png').convert_alpha()
        self.background_img = pygame.image.load('char_walk_right_2.png').convert_alpha()

        self.background_img = pygame.image.load('chair_top.png').convert_alpha()
        self.background_img = pygame.image.load('chair_left.png').convert_alpha()
        self.background_img = pygame.image.load('chair_left_top.png').convert_alpha()
        self.background_img = pygame.image.load('chair_right.png').convert_alpha()
        self.background_img = pygame.image.load('chair_right_top.png').convert_alpha()

        self.background_img = pygame.image.load('not_enough_money.png').convert_alpha()
        self.background_img = pygame.image.load('end_screen.png').convert_alpha()
        self.background_img = pygame.image.load('end_game_button.png').convert_alpha()
        self.background_img = pygame.image.load('exit_button.png').convert_alpha()

        # self.play_sound("background.mp3", loop=True, volume=0.4)

        self.input_rect = pygame.Rect(205, 530, 200, 40)
        self.input_text = ''

    def play_sound(self, path, volume=0.5, loop=False):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        sound.play(loops=-1 if loop else 0)
        return sound

    def run(self):


        running = True

        while running:

            self.screen.blit(self.background_img, (0, 0))

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
                        for _ in range(2):
                            self.screen.blit(self.background_img, (0, 0))
                            pygame.time.wait(200)
                            all_sprites.draw(screen)
                            pygame.display.flip()
                            char.update()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = CoinFlipGame()
    game.run()
