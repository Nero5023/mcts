# coding: utf-8
import Board

def toList(state):
    return list(map(list, state))

def toTuple(state):
    return tuple(map(tuple, state))

class WuziBoard(Board.Board):
    """docstring for WuziBoard"""


    # 1 先动
    def __init__(self, firstMove):
        super(WuziBoard, self).__init__()
        self.currentState = [([0] * 9) for i in range(9)]
        self.rounds = 0
        self.firstMove = firstMove

    def start(self):
        state = [([0] * 9) for i in range(9)]
        x, y = self.firstMove
        # (-1,-1) means not move
        if x >= 0 and y >= 0:
            state[x][y] = 1
        return toTuple(state)

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


    def next_state(self, state, play):
        state = toList(state)
        player = self.current_player(state)
        x, y = play
        state[x][y] = player
        return toTuple(state)

    def legal_plays(self, state_history):
        newestState = state_history[-1]
        length = len(newestState)
        legal = []
        for x in xrange(0, length):
            for y in xrange(0, length):
                if newestState[x][y] == 0:
                    legal.append((x,y))
        return legal

    def checkIsWin(self, state, position):
        x, y = position
        currentValue = state[x][y]
        isFive = True
        if currentValue == 0:
            return 0
        for xi in xrange(x, x+5):
            print xi
            print y
            print state
            if currentValue != state[xi][y]:
                isFive = False
                break
        if isFive:
            return True

        isFive = True
        for yi in xrange(y, y+5):
            print x
            print yi
            print state
            if currentValue != state[x][yi]:
                isFive = False
                break
        if isFive:
            return True

        isFive = True
        for i in xrange(0, 5):
            xi = x+i
            yi = y+i
            print xi
            print yi
            print i
            print state
            if currentValue != state[xi][yi]:
                isFive = False
                break
        if isFive:
            return True

        return False

    def winner(self, state_history):
        newestState = state_history[-1]
        length = len(newestState)
        maxCheckNum = length - 5 + 1
        player = self.current_player(newestState)
        if player == 1:
            player = 2
        else:
            player = 1
        for x in xrange(0, maxCheckNum):
            for y in xrange(0, maxCheckNum):
                if self.checkIsWin(newestState, (x, y)):
                    return player
        return 0
