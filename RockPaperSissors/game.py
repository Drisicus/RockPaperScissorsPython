""" Moved -> player chooses between rock, paper, sissors """
class Game:
    def __init__(self, id):
        self.p1Moved = False
        self.p2Moved = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0


    def get_player_move(self, p):
        return self.moves[p]

    def player(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Moved = True
        else:
            self.p2Moved = True

    def connected(self):
        return self.ready


    def bothWent(self):
        return self.p1Moved and self.p2Moved

    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p2 == "R" and p1 == "S":
            winner = 1
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p2 == "R" and p1 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 0
        elif p2 == "P" and p1 == "S":
            winner = 1
        return winner

    def resetWent(self):
        self.p1Moved = False
        self.p2Moved = False