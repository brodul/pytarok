from transitions import Machine
from ulid import ULID


class Session:
    """Game session not the game of tarok itself (see Round)"""

    states = ["waiting_players_to_join", "ready", "playing_round", "finished"]

    def __init__(self):
        self.ulid = ULID()
        self.max_round = 4

        # Context state
        self.current_round = 1
        self.score_board = None

        self.machine = Machine(
            model=self, states=Session.states, initial="waiting_players_to_join"
        )

        # Transitions
        self.machine.add_transition(
            trigger="players_joined", source="waiting_players_to_join", dest="ready"
        )
        self.machine.add_transition("start_round", "ready", "playing_round")
        self.machine.add_transition(
            "round_finished", "playing_round", "ready", after=["increase_round_count"]
        )
        self.machine.add_transition(
            "round_finished", "playing_round", "finished", conditions=["is_last_round"]
        )

    @property
    def is_last_round(self):
        return self.max_round == self.current_round

    def increase_round_count(self):
        self.current_round += 1
