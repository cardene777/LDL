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
    pygame.display.set_caption("Hello World")

    clock = pygame.time.Clock()  # 時間を管理

    """
    登場する人物/物/背景の作成
    """

    while True:
        """
        画面(screen)をクリア
        """

        screen.fill((0, 0, 0))  # 画面を黒で塗りつぶす

        """
        登場する人物/物/背景の位置アップデート
        """

        """
        画面(screen)上に登場する人/物/背景を描画
        """

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
