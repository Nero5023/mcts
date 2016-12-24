from __future__ import division
import datetime
from random import choice
from math import sqrt, log

class MonteCarlo(object):
    """docstring for MonteCarlo"""
    def __init__(self, board, **kwargs):
        # super(MonteCarlo, self).__init__()
        # self.board = board
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        
        self.board = board
        # self.states = []
        self.states = [board.start()]
        seconds = kwargs.get('time', 30)
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.max_moves = kwargs.get('max_moves', 100)

        self.wins = {}
        self.plays = {}

        self.C = kwargs.get('C', 1.4)


    def update(self, move):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        lastState = self.states[-1]
        state = self.board.next_state(lastState, move)
        print state
        self.states.append(state)

    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        plays, wins = self.plays, self.wins


        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        player = self.board.current_player(state)

        expend = True

        for t in xrange(self.max_moves):
            legal = self.board.legal_plays(states_copy)
            
            move_states = [(p, self.board.next_state(state, p)) for p in legal]
            # print move_states
            # print "----------"
            if all(plays.get((player, S)) for p, S in move_states):
                log_total = log(sum(plays[(player, S)] for p, S in move_states))
                value, move, state = max(
                        ((wins[player, S]/plays[player, S]) +
                            self.C * sqrt(log_total / plays[player, S]), p, S)
                        for p, S in move_states
                    )
            else:
                # Otherwise, just make an arbitrary decision.
                move, state = choice(move_states)

            # play = choice(legal)
            # state = self.board.next_state(state, play)
            states_copy.append(state)

            if expend and (player, state) not in self.plays:
                expend = False
                self.plays[(player, state)] = 0
                self.wins[(player, state)] = 0

                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, state))

            player = self.board.current_player(state)
            winner = self.board.winner(states_copy)
            
            if winner:
                break

        for player, state in visited_states:
            if (player, state) not in self.plays:
                continue
            self.plays[(player, state)] += 1
            if player == winner:
                self.wins[(player, state)] += 1

    def winner(self):
        return self.board.winner(self.states)

    def get_play(self):

        self.max_depth = 0
        state = self.states[-1]
        player = self.board.current_player(state)
        legal = self.board.legal_plays(self.states[:])

        # Bail out early if there is no real choice to be made.
        if not legal:
            return None
        if len(legal) == 1:
            return legal[0]

        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        move_states = [(p, self.board.next_state(state, p)) for p in legal]

        # Display the number of calls of `run_simulation` and the
        # time elapsed.
        print games, datetime.datetime.utcnow() - begin

        # Pick the move with the highest percentage of wins.
        percent_wins, move = max(
            (self.wins.get((player, S), 0) /
             self.plays.get((player, S), 1),
             p)
            for p, S in move_states
        )

         # Display the stats for each possible play.
        for x in sorted(
            ((100 * self.wins.get((player, S), 0) /
              self.plays.get((player, S), 1),
              self.wins.get((player, S), 0),
              self.plays.get((player, S), 0), p)
             for p, S in move_states),
            reverse=True
        ):
            print "{3}: {0:.2f}% ({1} / {2})".format(*x)

        print "Maximum depth searched:", self.max_depth

        return move