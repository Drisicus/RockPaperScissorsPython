import pygame
from RockPaperSissors.network import Network
from RockPaperSissors.player import Player
pygame.font.init()


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        window.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, position):
        x1 = position[0]
        y1 = position[1]
        return self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height

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