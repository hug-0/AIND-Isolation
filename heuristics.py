"""This file contains a number of heuristic functions that can be applied to the game of isolation.

Sources: General Game Player, Stanford (CS227)
         url: http://logic.stanford.edu/classes/cs227/2015/notes.html

Definitions:
------------
    Mobility: A measure of the number of things a player can do.
        Action mobility: How mobile a given player is in a given game state,
               or n game states ahead of the current state.

        State mobility: The number of unique game states that can be
                        reached from the current game state.

    Focus:
        Action focus: Measures the 'narrowness' of the search space in
                      a given game state and player. Inverse of action mobility.

        State focus: The inverse of state mobility.
"""

import isolation
import game_agent as agent

# The most number of possible actions would be to have access to the entire game board
class Heuristic:
    def __init__(self, game, player):
        """An object that maintains and evaluates heuristics for the game of Isolation.

        Parameters
        ----------
        game : isolation.Board
            An instance of `isolation.Board` encoding the current
            game (e.g., player locations and blocked cells).

        player : object
            A player instance in the current game (i.e., an object corresponding to one of the player objects `game.__player_1__` or `game.__player_2__`.)

        Returns
        ----------
        object
            The heuristic object with the specified parameters for the current player and game state.
        """
        self.game = game
        self.player = player
        #self.BEST_NUM_MOVES = game.width * game.height

    def score(self, state, player, method='action_mobility'):
        """Evaluation function that computes a score for a given player and a given game state.

        Parameters
        ----------
        state : isolation.Board
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        player : object
            A player instance in the current game (i.e., an object corresponding to one of the player objects `game.__player_1__` or `game.__player_2__`.)

        method : string
            Sets which evaluation function form to use to compute the score.
            Default : 'action_mobility'
            Options : 'action_mobility', 'action_focus', 'the_super_duper_hugo_heuristic'

        Returns
        ----------
        float
            The heuristic score of the current game state to the specified player.
        """
        methods = {
            'action_mobility': self.action_mobility,
            'action_focus': self.action_focus,
            'the_super_duper_hugo_heuristic': self.the_super_duper_hugo_heuristic
        }

        if state.is_loser(player):
            return float('-inf')

        if state.is_winner(player):
            return float('inf')

        return methods[method](state)

    def action_mobility(self, state):
        """Compute the current player's relative mobility for a given game state by looking one step ahead.

        Parameters
        ----------
        state : isolation.Board
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        Returns
        ----------
        float
            The mobility heuristic score of the current game state.
        """

        legal_moves = state.get_legal_moves()
        states_one_step_ahead = [state.forecast_move(move) for move in legal_moves]
        best_moves_ahead = 0
        for future_state in states_one_step_ahead:
            # Player changes after move, so we need to select the moves from the player in the current state
            num_new_moves = len(future_state.get_legal_moves(future_state.inactive_player))
            best_moves_ahead = max(best_moves_ahead, num_new_moves)

        return float(best_moves_ahead/len(legal_moves))

    def the_super_duper_hugo_heuristic(self, state, weight=2.5):
        """A custom heuristic not found in literature. It augments the common heuristic (player_moves - opponent_moves) and weights opponent's moves higher, and scales the resulting value by the number of filled spaces.

        Parameters
        ----------
        state : isolation.Board
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        weight: int
            The weight with which to penalize the current player based on the number of moves the opponent has.

        Returns
        ----------
        float
            The heuristic score of the current game state.
        """
        filled_spaces = (state.width * state.height) - len(state.get_blank_spaces())
        player_moves = len(state.get_legal_moves())
        opponent_moves = len(state.get_legal_moves(state.get_opponent(state.inactive_player)))

        return float((player_moves - weight * opponent_moves) * filled_spaces)

    def action_focus(self, state):
        return 1. - self.action_mobility(state)

    def state_focus(self, state):
        # TODO
        pass
