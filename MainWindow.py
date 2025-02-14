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


class CoinFlipGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CoinFlip")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        pygame.mixer.init()

        self.background_img = pygame.image.load('background.png')
        # self.play_sound("background.mp3", loop=True, volume=0.4)

        self.input_rect = pygame.Rect(205, 530, 200, 40)
        self.input_text = ''

    def play_sound(self, path, volume=0.5, loop=False):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        sound.play(loops=-1 if loop else 0)
        return sound

    def run(self):

        char = AnimatedSprite(load_image("char.png").convert_alpha(), 3, 4, 317, 233)

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
                        char.cur_frame = 0
                        for _ in range(2):
                            print(char.cur_frame)
                            self.screen.blit(self.background_img, (0, 0))
                            pygame.time.wait(200)
                            all_sprites.draw(screen)
                            pygame.display.flip()
                            char.update()
                        char.cur_frame = 0
                    if event.key == pygame.K_d:
                        char.cur_frame = 3
                        for _ in range(2):
                            print(char.cur_frame)
                            self.screen.blit(self.background_img, (0, 0))
                            pygame.time.wait(200)
                            all_sprites.draw(screen)
                            pygame.display.flip()
                            char.update()
                        char.cur_frame = 3
                    if event.key == pygame.K_a:
                        char.cur_frame = 6
                        for _ in range(2):
                            print(char.cur_frame)
                            self.screen.blit(self.background_img, (0, 0))
                            pygame.time.wait(200)
                            all_sprites.draw(screen)
                            pygame.display.flip()
                            char.update()
                        char.cur_frame = 6
                    if event.key == pygame.K_s:
                        char.cur_frame = 9
                        for _ in range(2):
                            print(char.cur_frame)
                            self.screen.blit(self.background_img, (0, 0))
                            pygame.time.wait(200)
                            all_sprites.draw(screen)
                            pygame.display.flip()
                            char.update()
                        char.cur_frame = 9

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = CoinFlipGame()
    game.run()
