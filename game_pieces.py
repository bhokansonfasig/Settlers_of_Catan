class Pieces():
    def __init__(self):
        self.players = []
        self.tiles = []

        self.all_points = []
        self.all_roads = []

        self.all_computers = True

        self.loop_index = -1
        self.turn_index = -1
        self.active_index = -1
        self.turn_phase = "prelim"

        self.dice = (0,0)

        self.log_file_name = "catan_game_log.txt"
        self.log_file = None

        #Development cards
        self.development_cards = ['knight']*14 + ['victory point']*5 + ['road building']*2 + ['monopoly']*2 + ['year of plenty']*2

    def phase_index(self):
        phases = ["prelim","player selection","setup",
            "first placements","second placements","change turns",
            "roll dice","discard","trade","place robber","make decisions",
            "build settlement","build road","build city","end game"]
        return phases.index(self.turn_phase.lower())
