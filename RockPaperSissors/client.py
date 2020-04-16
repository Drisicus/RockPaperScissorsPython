import pygame
from RockPaperSissors.network import Network
import pickle
pygame.font.init()

width = 750
height = 700

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


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


def redrawWindow(windowPygame, game, player):
    windowPygame.fill((128, 128, 128))
    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 90)
        text = font.render("Waiting for player...", 1, (255, 0, 0), True)
        window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        window.blit(text, (80, 200))

        text = font.render("Opponent Move", 1, (0, 255, 255))
        window.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and player == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and player == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if player == 0:
            window.blit(text1, (100, 350))
            window.blit(text2, (400, 350))
        else:
            window.blit(text2, (100, 350))
            window.blit(text1, (400, 350))

    for button in buttons:
        button.draw(window)

    pygame.display.update()


buttons = [Button("Rock", 50, 500, (0, 0, 0)), Button("Scissors", 250, 500, (255, 0, 0)), Button("Paper", 450, 500, (0, 255, 0))]
def main():
    gameInProgress = True
    clock = pygame.time.Clock()

    networkManager = Network()
    player = int(networkManager.getPlayer())
    print("You are player ", player)

    while gameInProgress:
        clock.tick(60)

        try:
            game = networkManager.send("get")
        except:
            gameInProgress = gameOver()

        if game.bothWent():
            redrawWindow(window, game, player)
            pygame.time.delay(500)
            try:
                game = networkManager.send("reset")
            except:
                gameInProgress = gameOver()

            font = pygame.font.SysFont("comicsans", 90)
            if game.winner() == player:
                text = font.render("You Won!", 1, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 0, 0))
            else:
                text = font.render("You Lost!", 1, (255, 0, 0))

            window.blit(text, (width/2 - text.get_width() / 2, height/2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameInProgress = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(mousePosition) and game.connected():
                        if player == 0: # we are player 1
                            if not game.p1Went:
                                networkManager.send(button.text)
                        else: # we are player 2
                            if not game.p2Went:
                                networkManager.send(button.text)
        redrawWindow(window, game, player)

def gameOver():
    print("Error getting the game")
    return False

def menu_screen():
    menuRunning = True
    clock = pygame.time.Clock()

    while menuRunning:
        clock.tick(60)
        window.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0))
        window.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                menuRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                menuRunning = False
    main()


while True:
    menu_screen()