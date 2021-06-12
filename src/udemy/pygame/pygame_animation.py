import random
import sys

import pygame
import pygame.mixer
from pygame.locals import *

SCREEN = Rect((0, 0, 640, 480))


def load_image(fname, size=None):
    tmp = pygame.image.load(f"picture/{fname}")
    return tmp if size == None else pygame.transform.scale(tmp, size)


def load_sound(sound):
    return pygame.mixer.Sound(f"music/{sound}")


class BackGround:
    def __init__(self, majo):
        # 画像ロード
        self.majo = majo
        self.sky_img = load_image("bg_natural_sky.jpeg", SCREEN.size)
        self.mount_img = load_image("bg_natural_mount_800x800.png")
        self.mount_rect = self.mount_img.get_rect()
        self.ground = pygame.Surface((SCREEN.width, 20))
        self.ground.fill((0, 128, 64))
        self.ground_rect = self.ground.get_rect()
        self.ground_rect.bottom = SCREEN.bottom

    def update(self):
        self.mount_img_x = (self.mount_rect.width - SCREEN.width) / SCREEN.width * self.majo.rect.centerx

    def draw(self, screen):
        # 画像の描画
        screen.blit(self.sky_img, SCREEN)
        screen.blit(self.mount_img, (-self.mount_img_x, -118))
        screen.blit(self.ground, self.ground_rect)


class Majo(pygame.sprite.Sprite):
    IMAGE_WIDTH, IMAGE_HEIGHT = (32, 32)
    LEFT, RIGHT = (1, 2)
    SPEED = 5
    IMAGE_NUMS = 3

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = load_image("majo.png")
        self.image_dir = Majo.LEFT
        self.image_off = 0
        self.image = self.images.subsurface((0, 0, Majo.IMAGE_WIDTH, Majo.IMAGE_HEIGHT))
        self.rect = Rect((0, 0, Majo.IMAGE_WIDTH, Majo.IMAGE_HEIGHT))
        self.rect.centerx = SCREEN.centerx
        self.rect.bottom = SCREEN.bottom - 20

    def move_left(self):
        self.rect.move_ip(- Majo.SPEED, 0)
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
            self.image_off * Majo.IMAGE_WIDTH,
            self.image_dir * Majo.IMAGE_HEIGHT,
            Majo.IMAGE_WIDTH, Majo.IMAGE_HEIGHT
        )

    def update(self):
        pass

    # def draw(self, screen):
    #     screen.blit(self.img, self.rect)


class Beam(pygame.sprite.Sprite):
    SPEED = 5
    counter = 0
    EXP_IMAGE_WIDTH, EXP_IMAGE_HEIGHT = 120, 120
    EXP_IMAGE_OFFSET = 5
    EXP_ANIME_COUNT = 5

    def __init__(self, majo, ufo, bomb_g):
        self.majo = majo
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.majo.rect.centerx
        self.rect.bottom = self.majo.rect.top
        self.ufo = ufo
        self.bomb_g = bomb_g
        Beam.counter += 1
        Beam.sound.play()

    def update(self):
        self.rect.top -= Beam.SPEED
        if self.rect.top < SCREEN.top:
            Beam.counter -= 1
            self.kill()  # 描画対象から外す

        # UFOとの衝突判定
        if self.rect.colliderect(self.ufo.rect):
            Explosion(
                Beam.exp_images,
                self.rect.center,
                (Beam.EXP_IMAGE_WIDTH, Beam.EXP_IMAGE_HEIGHT),
                Beam.EXP_IMAGE_OFFSET,
                Beam.EXP_ANIME_COUNT,
                Beam.exp_sound
            )
            if Beam.counter > 0:
                Beam.counter -= 1
            self.kill()
            return
        # 爆弾との衝突判定
        bomb_collided = pygame.sprite.spritecollide(
            self, self.bomb_g, True)
        if bomb_collided:
            Explosion(
                Beam.exp_images,
                bomb_collided[0].rect.center,
                (Beam.EXP_IMAGE_WIDTH, Beam.EXP_IMAGE_HEIGHT),
                Beam.EXP_IMAGE_OFFSET,
                Beam.EXP_ANIME_COUNT,
                Beam.exp_sound
            )
            if Beam.counter > 0:
                Beam.counter -= 1
            self.kill()
            return


class UFO(pygame.sprite.Sprite):
    IMAGE_WIDTH, IMAGE_HEIGHT = (64, 28)
    START = (SCREEN.width / 4, 30)
    SPEED = 5
    LEFT, RIGHT = 0, 1
    BOMB_PROB = 0.01

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = UFO.images.subsurface(UFO.LEFT, 0, UFO.IMAGE_WIDTH, UFO.IMAGE_HEIGHT)
        self.rect = self.image.get_rect()
        self.rect.midtop = UFO.START
        self.speed = UFO.SPEED
        self.dir = UFO.LEFT

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left <= SCREEN.left or self.rect.right >= SCREEN.right:
            self.speed = - self.speed  # 方向転換
        self.rect.clamp_ip(SCREEN)
        self.dir = UFO.LEFT if self.speed > 0 else UFO.RIGHT
        self.image = UFO.images.subsurface(self.dir * UFO.IMAGE_WIDTH, 0, UFO.IMAGE_WIDTH, UFO.IMAGE_HEIGHT)

        # 爆弾を投下
        if random.random() < UFO.BOMB_PROB:
            Bomb(self)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, images, start_pos, image_size, max_offset, max_anime_count, exp_sound):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = images
        self.images_rect = self.images.get_rect()
        self.max_offset = max_offset
        self.offset = 0
        self.max_anime_count = max_anime_count
        self.anime_count = 0
        self.sizex, self.sizey = image_size
        if self.images_rect.width > self.images_rect.height:
            # imagesは横の画像
            self.image = self.images.subsurface(
                (self.offset * self.sizex, 0, self.sizex, self.sizey)
            )
        else:
            # imagesは縦の画像
            self.image = self.images.subsurface(
                (0, self.offset * self.sizey, self.sizex, self.sizey)
            )
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        exp_sound.play()

    def update(self):
        self.anime_count = (self.anime_count + 1) % self.max_anime_count
        if self.anime_count == 0:
            self.offset += 1
            if self.offset == self.max_offset:
                self.offset = 0
                self.kill()
                return
        if self.images_rect.width > self.images_rect.height:
            # imagesは横の画像
            self.image = self.images.subsurface(
                (self.offset * self.sizex, 0, self.sizex, self.sizey)
            )
        else:
            # imagesは縦の画像
            self.image = self.images.subsurface(
                (0, self.offset * self.sizey, self.sizex, self.sizey)
            )


class Bomb(pygame.sprite.Sprite):
    IMAGE_WIDTH, IMAGE_HEIGHT = (64, 112)
    IMAGE_COLORS, IMAGE_OFFSET = 4, 3
    SPEED = 5
    EXP_IMAGE_WIDTH, EXP_IMAGE_HEIGHT = 120, 120
    EXP_IMAGE_OFFSET = 7
    EXP_ANIME_COUNT = 5

    def __init__(self, ufo):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image_color = int(random.random() * Bomb.IMAGE_COLORS)
        self.image_off = 0
        self.image = Bomb.images.subsurface(
            (self.image_off * Bomb.IMAGE_WIDTH,
             self.image_color * Bomb.IMAGE_HEIGHT,
             Bomb.IMAGE_WIDTH, Bomb.IMAGE_HEIGHT
             )
        )
        self.rect = self.image.get_rect()
        self.rect.midtop = ufo.rect.midbottom

    def update(self):
        self.rect.move_ip(0, Bomb.SPEED)
        if self.rect.bottom > SCREEN.bottom:
            Explosion(
                Bomb.exp_images,
                self.rect.center,
                (Bomb.EXP_IMAGE_WIDTH, Bomb.EXP_IMAGE_HEIGHT),
                Bomb.EXP_IMAGE_OFFSET,
                Bomb.EXP_ANIME_COUNT,
                Bomb.exp_sound
            )
            self.kill()
            return
        self.image_off = (self.image_off + 1) % Bomb.IMAGE_OFFSET
        self.image = Bomb.images.subsurface(
            (self.image_off * Bomb.IMAGE_WIDTH,
             self.image_color * Bomb.IMAGE_HEIGHT,
             Bomb.IMAGE_WIDTH, Bomb.IMAGE_HEIGHT
             )
        )


def main():
    """
    pygame main
    """

    """
    初期設定
    """

    pygame.init()
    screen = pygame.display.set_mode(SCREEN.size)
    pygame.display.set_caption("Animation")
    clock = pygame.time.Clock()  # 時間を管理

    """
    Sprite登録
    """

    group = pygame.sprite.RenderUpdates()
    bomb_g = pygame.sprite.Group()
    Majo.containers = group
    Beam.containers = group
    UFO.containers = group
    Bomb.containers = group, bomb_g
    Explosion.containers = group

    """
    登場する人物/物/背景の作成
    """

    Beam.sound = load_sound("se_maoudamashii_se_ignition01.ogg")
    Beam.image = load_image("majo_beam.png")
    UFO.images = load_image("all_ufo3.png", (128, 28))
    Bomb.images = load_image("ufo_bomb.png")
    Bomb.exp_images = load_image("bomb_fire.png")
    Bomb.exp_sound = load_sound("魔王魂  爆発05.ogg")
    Beam.exp_images = load_image("beam_fire.png")
    Beam.exp_sound = load_sound("魔王魂  爆発04.ogg")

    majo = Majo()
    bg_img = BackGround(majo)
    ufo = UFO()

    while True:
        """
        画面(screen)をクリア
        """

        screen.fill((0, 0, 0))

        """
        登場する人物/物/背景の位置アップデート
        """

        bg_img.update()
        group.update()

        """
        画面(screen)上に登場する人/物/背景を描画
        """

        bg_img.draw(screen)
        group.draw(screen)

        """
        画面(screen)の実表示
        """

        pygame.display.update()

        """
        イベント処理
        """

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if Beam.counter < 2:
                    if __name__ == '__main__':
                        Beam(majo, ufo, bomb_g)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            majo.move_left()
        if pressed_keys[K_RIGHT]:
            majo.move_right()
        """
        描画スピードの調整(FPS)
        """

        clock.tick(100)


if __name__ == '__main__':
    main()
