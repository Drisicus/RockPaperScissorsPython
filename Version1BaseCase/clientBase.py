import pygame

from Version1BaseCase.networkBase import Network

width = 500
height = 500

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    # update the rectangle that represents player
    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel
        self.update()


def redrawWindow(window, player, player2):
    window.fill((255,255,255))
    player.draw(window)
    player2.draw(window)
    pygame.display.update()


def readPosition(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def makePosition(tupple):
    return str(tupple[0]) + "," + str(tupple[1])

def main():
    gameInProgress = True
    clock = pygame.time.Clock()

    networkManager = Network()
    startPosition = readPosition(networkManager.getPosition())

    player = Player(startPosition[0], startPosition[1], 100, 100, (0, 255, 0))
    player2 = Player(0, 0, 100, 100, (255, 0, 0))

    while gameInProgress:
        clock.tick(60)

        player2Position = readPosition(networkManager.send(makePosition((player.x, player.y))))
        player2.x = player2Position[0]
        player2.y = player2Position[1]
        player2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameInProgress = False
                pygame.quit()

        player.move()
        redrawWindow(window, player, player2)

main()