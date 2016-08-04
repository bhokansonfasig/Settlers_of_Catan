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

    def phase_index(self):
        phases = ["prelim","player selection","setup",
            "first placements","second placements",
            "roll dice","discard","place robber","make decisions",
            "build settlement","build road","build city","end game"]
        return phases.index(self.turn_phase.lower())
