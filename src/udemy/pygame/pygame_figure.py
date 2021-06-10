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

    # 円
    circ_sur = pygame.Surface((60, 60))  # 60x60の画像を作成
    pygame.draw.circle(circ_sur, (255, 255, 255), (30, 30), 30)  # 半径30の円を白色で描画

    # 長方形
    rect_sur = pygame.Surface((100, 60))
    pygame.draw.rect(rect_sur, (255, 0, 0), (0, 0, 100, 60))

    # 線
    line_sur = pygame.Surface((100, 50))
    pygame.draw.line(line_sur, (0, 255, 0), (0, 0), (100, 50))

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

        # 描画するものと描画開始位置の指定
        screen.blit(circ_sur, (0, 0))
        screen.blit(rect_sur, (150, 150))
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
