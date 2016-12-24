from WuziBoard import *
from MonteCarlo import *

if __name__ == '__main__':
    # (-1,-1) means not move
    board1 = WuziBoard((-1,-1)) 
    ai1 = MonteCarlo(board1)
    move = ai1.get_play()
    ai1.update(move)
    board2 = WuziBoard(move)
    ai2 = MonteCarlo(board2)
    player = 0
    iteration = 1
    print iteration
    print '--------------------'
    while True:
        if player == 0:
            move = ai2.get_play()
            print move
            ai1.update(move)
            ai2.update(move)
        if player == 1:
            move = ai1.get_play()
            ai1.update(move)
            ai2.update(move)
        iteration += 1
        print iteration
        print '--------------------'
        player = (player + 1)%2
        winner = ai1.winner()
        if winner:
            print "Winn, Winner:", winner
            break
