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
        self.knight_leftover_cards = 0 # Knight leftover_cardss
        self.victory_point_leftover_cards = 0 # VP leftover_cardss
        self.road_building_leftover_cards = 0 # Road building leftover_cardss
        self.monopoly_leftover_cards = 0 # Monopoly leftover_cardss
        self.year_of_plenty_leftover_cards = 0 # Year of plenty cards

    def phase_index(self):
        phases = ["prelim","player selection","setup",
            "first placements","second placements",
            "roll dice","discard","place robber","make decisions",
            "build settlement","build road","build city","end game"]
        return phases.index(self.turn_phase.lower())
