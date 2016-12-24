class Board(object):

    def srart():
        # Returns a representation of the starting state of the game.
          pass  

    def current_player(self, state):
        # Takes the game state and returns the current player's number
        pass

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Return the new game state
        pass

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        pass

    def winner(self, state_history):
        # Takes a sequences of game state representing thr full
        # game history. If the game is now won, return the player 
        # number. If the game is still ongoing, return zero. If 
        # the game is tied, return a different distinct value, e.g. -1.
        pass


import Board

class WuziBoard(Board.Board):
    """docstring for WuziBoard"""

    # 1 先动
    def __init__(self):
        super(WuziBoard, self).__init__()
        self.currentState = [([0] * 9) for i in range(9)]
        self.rounds = 0

    def current_player(self, state):
        player1 = map((lambda innerlist: 
                    sum(map((lambda x: x==1) , innerlist))
                    ), state)
        player1 = sum(player1)
        player2 = map((lambda innerlist: 
                    sum(map((lambda x: x==2) , innerlist))
                    ), state)
        player2 = sum(player2)
        if player1 == player2:
            return 1
        else:
            return 2