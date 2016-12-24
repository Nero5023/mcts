import datetime

class MonteCarlo(object):
    """docstring for MonteCarlo"""
    def __init__(self, board, **kwargs):
        # super(MonteCarlo, self).__init__()
        # self.board = board
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.
        
        self.board = board
        self.states = []
        seconds = kwargs.get('time', 30)
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.max_moves = kwargs.get('max_moves', 100)

        self.wins = {}
        self.plays = {}

        self.C = kwargs.get('C', 1.4)


    def update(self, state):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        self.states.append(state)

    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        player = self.board.current_player(state)

        expend = True

        for t in xrange(self.max_moves):
            legal = self.board.legal_plays(states_copy)
            
            play = choice(legal)
            state = self.board.next_state(state, play)
            states_copy.append(state)

            if expend and (player, state) not in self.plays:
                expend = False
                self.plays[(player, state)] = 0
                self.wins[(player, state)] = 0

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
                    self.wins[(player, states)] += 1

    def get_play(self):
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
