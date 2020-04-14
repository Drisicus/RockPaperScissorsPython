import pygame
from Version2.network import Network
from Version2.player import Player

width = 500
height = 500

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(windowPygame, player, player2):
    windowPygame.fill((255, 255, 255))
    player.draw(windowPygame)
    player2.draw(windowPygame)
    pygame.display.update()

def main():
    gameInProgress = True
    clock = pygame.time.Clock()

    networkManager = Network()
    player1 = networkManager.getPlayer()

    while gameInProgress:
        clock.tick(60)

        player2 = networkManager.send(player1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameInProgress = False
                pygame.quit()

        player1.move()
        redrawWindow(window, player1, player2)

main()