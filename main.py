import pygame
import sys
from config import WIDTH, HEIGHT
from ui import UIManager


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PONG 2D")

    try:
        icon = pygame.image.load("icon.png")
        pygame.display.set_icon(icon)
    except:
        pass

    ui = UIManager(screen)

    try:
        pygame.mixer.music.load("sounds/music.mp3")
        pygame.mixer.music.set_volume(ui.music_volume)
        pygame.mixer.music.play(-1)
    except:
        pass

    ui.show_main_menu()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()