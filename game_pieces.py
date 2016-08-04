class Pieces():
    def __init__(self):
        self.players = []
        self.tiles = []

        self.all_points = []
        self.all_roads = []

        self.loop_index = -1
        self.turn_index = -1
        self.all_computers = True

        self.die = (0,0)

        self.log_file_name = "catan_game_log.txt"
        self.log_file = None
