players = []
class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.nice_dict = {}
        players.append(self)

def get_dict(headers_arr, actual_arr, year):
    dict_for_stuff = {}
    for index, header in enumerate(headers_arr):
        dict_for_stuff[header] = actual_arr[index]
    dict_for_stuff['SEASON'] = year
    return dict_for_stuff

def find_player(id, name):
    for player in players:
        if player.id == id and player.name == name:
            return player
    player = Player(id, name)
    return player
