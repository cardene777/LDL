import pygame
import pygame.mixer
from pygame.locals import *
import sys
import os

SCREEN = Rect((0, 0, 640, 480))


def load_image(fname, size=None):
    tmp = pygame.image.load("picture/" + fname)
    return tmp if size == None else pygame.transform.scale(tmp, size)


def load_sound(sound):
    return pygame.mixer.Sound("music/" + sound)


'''登場する人物/物/背景のクラス定義'''


class Background:
    '''背景'''

    def __init__(self, majo):
        self.majo = majo
        self.sky_image = load_image("bg_natural_sky.jpeg", SCREEN.size)
        self.mount_image = load_image("bg_natural_mount_800x800.png")
        self.mount_rect = self.mount_image.get_rect()
        self.ground_image = pygame.Surface((SCREEN.width, 20))
        self.ground_image.fill((0, 128, 64))
        self.ground_rect = self.ground_image.get_rect()
        self.ground_rect.bottom = SCREEN.bottom

    def update(self):
        self.mount_image_x = (self.mount_rect.width - SCREEN.width) / \
                             SCREEN.width * self.majo.rect.centerx

    def draw(self, screen):
        screen.blit(self.sky_image, SCREEN)
        screen.blit(self.mount_image, (-self.mount_image_x, -118))
        screen.blit(self.ground_image, self.ground_rect)


class Majo(pygame.sprite.Sprite):
    '''魔女'''
    IMAGE_WIDTH, IMAGE_HEIGHT = (32, 32)
    LEFT, RIGHT = (1, 2)
    SPEED = 5
    IMAGE_NUMS = 3

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = load_image("majo.png")
        self.image_dir = Majo.LEFT
        self.image_off = 0
        self.image = self.images.subsurface(
            (0, 0, Majo.IMAGE_WIDTH, Majo.IMAGE_HEIGHT))
        self.rect = Rect((0, 0, Majo.IMAGE_WIDTH, Majo.IMAGE_HEIGHT))
        self.rect.centerx = SCREEN.centerx
        self.rect.bottom = SCREEN.bottom - 20

    def move_left(self):
        self.rect.move_ip(-Majo.SPEED, 0)
        self.image_dir = Majo.LEFT
        self.move()

    def move_right(self):
        self.rect.move_ip(Majo.SPEED, 0)
        self.image_dir = Majo.RIGHT
        self.move()

    def move(self):
        self.rect.clamp_ip(SCREEN)
        self.image_off = (self.image_off + 1) % Majo.IMAGE_NUMS
        self.image = self.images.subsurface(
            (self.image_off * Majo.IMAGE_WIDTH,
             self.image_dir * Majo.IMAGE_HEIGHT,
             Majo.IMAGE_WIDTH,
             Majo.IMAGE_HEIGHT)
        )

    def update(self):
        pass


#	def draw(self, screen):
#		screen.blit(self.image, self.rect)

class Beam(pygame.sprite.Sprite):
    '''魔女のビーム'''
    SPEED = 5
    counter = 0

    def __init__(self, majo):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.majo = majo
        self.rect = self.image.get_rect()
        self.rect.centerx = self.majo.rect.centerx
        self.rect.bottom = self.majo.rect.top
        Beam.counter += 1
        Beam.sound.play()

    def update(self):
        self.rect.top -= Beam.SPEED
        if self.rect.top < SCREEN.top:
            Beam.counter -= 1
            self.kill()


def main():
    '''初期設定'''
	# 画面の初期設定
    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    pygame.display.set_caption('Animation')

    # 時間管理
    clock = pygame.time.Clock()

    '''Sprite登録'''
    group = pygame.sprite.RenderUpdates()
    Majo.containers = group
    Beam.containers = group

    '''登場する人/物/背景の作成'''
    Beam.sound = load_sound("se_maoudamashii_se_ignition01.ogg")
    Beam.image = load_image("majo_beam.png")

    majo = Majo()
    bg_img = Background(majo)

    while True:

        '''画面(screen)をクリア'''
        screen.fill((0, 0, 0))

        '''ゲームに登場する人/物/背景の位置Update'''
        bg_img.update()
        group.update()

        '''画面(screen)上に登場する人/物/背景を描画'''
        bg_img.draw(screen)
        group.draw(screen)

        '''画面(screen)の実表示'''
        pygame.display.update()

        '''イベント処理'''
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if Beam.counter < 2:
                    Beam(majo)

        pressed_keys = pygame.key.get_pressed()
        # 押されているキーに応じて画像を移動
        if pressed_keys[K_LEFT]:
            majo.move_left()
        elif pressed_keys[K_RIGHT]:
            majo.move_right()

        '''描画スピードの調整（FPS)'''
        clock.tick(60)


if __name__ == "__main__":
    main()
        