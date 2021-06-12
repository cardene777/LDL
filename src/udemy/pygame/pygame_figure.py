import sys

import pygame
from pygame.locals import *


def main():
    """
    pygame main
    """

    """
    初期設定
    """

    pygame.init()
    screen = pygame.display.set_mode((600, 400))  # 画面の大きさを指定
    SCREEN = screen.get_rect()
    pygame.display.set_caption("Hello World")

    clock = pygame.time.Clock()  # 時間を管理

    """
    登場する人物/物/背景の作成
    """

    # 円
    # circ_sur = pygame.Surface((60, 60))  # 60x60の画像を作成
    circ_sur = pygame.Surface((20, 20))
    circ_sur.set_colorkey((0, 0, 0))
    circ_rect = circ_sur.get_rect()  # 画像の位置情報と大きさの情報を取得
    circ_rect.topleft = (300, 150)  # 画像の位置を変更
    dx, dy = 5, 4  # 移動速度を変更
    # pygame.draw.circle(circ_sur, (255, 255, 255), (30, 30), 30)  # 半径30の円を白色で描画
    pygame.draw.circle(circ_sur, (255, 255, 255), (10, 10), 10)

    # 長方形
    rect_sur = pygame.Surface((100, 60))
    pygame.draw.rect(rect_sur, (255, 0, 0), (0, 0, 100, 60))

    # 線
    line_sur = pygame.Surface((100, 50))
    line_sur.set_colorkey((0, 0, 0))  # 透過色を指定
    pygame.draw.line(line_sur, (0, 255, 0), (0, 0), (100, 50))

    while True:
        """
        画面(screen)をクリア
        """

        screen.fill((0, 0, 0))  # 画面を黒で塗りつぶす

        """
        登場する人物/物/背景の位置アップデート
        """

        # pressed_keys = pygame.key.get_pressed()  # キーが押されているか判定
        # if pressed_keys[K_LEFT]:
        #     circ_rect.move_ip(-5, 0)  # 左に移動
        # if pressed_keys[K_RIGHT]:
        #     circ_rect.move_ip(5, 0)  # 左に移動
        # if pressed_keys[K_UP]:
        #     circ_rect.move_ip(0, -5)  # 左に移動
        # if pressed_keys[K_DOWN]:
        #     circ_rect.move_ip(0, 5)  # 左に移動

        circ_rect.move_ip(dx, dy)  # キーが押されたら指定文移動する
        # 画面を越えようとした時反転させる。
        if circ_rect.left < SCREEN.left or circ_rect.right > SCREEN.right:
            dx = -dx
        if circ_rect.top < SCREEN.top or circ_rect.bottom > SCREEN.bottom:
            dy = -dy

        circ_rect.clamp_ip(SCREEN)  # スクリーンを飛び出る場合は、スクリーン内に位置情報を修正する。

        """
        画面(screen)上に登場する人/物/背景を描画
        """

        # 描画するものと描画開始位置の指定
        screen.blit(rect_sur, (150, 150))
        screen.blit(circ_sur, circ_rect.topleft)
        screen.blit(line_sur, (250, 250))

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

        """
        描画スピードの調整(FPS)
        """

        clock.tick(60)


if __name__ == '__main__':
    main()
