#
#   fold_moments :
#
#   -1  :   player eliminated or not at table anymore
#   0   :   fold before flop
#   1   :   fold at flop
#   2   :   fold at turn
#   3   :   fold at river
#   4   :   doesn't fold

FOLD_MOMENT = {-1: "player eliminated or not at table anymore", 0: "fold before flop", 1: "fold at flop",
               2: "fold at turn", 3: "fold at river", 4: "doesn't fold"}

TABLE_SIZE_SPLIT_LEFT = "' "
TABLE_SIZE_SPLIT_RIGHT = "-max"
SEAT_NUMBER_SPLIT_LEFT = "Seat "
SEAT_NUMBER_SPLIT_RIGHT = ": "

DEFAULT_PLAYER = ""


class Tournament:

    def __init(self, table_size):
        self.table_size = table_size


class Hand:

    def __init__(self, players, fold_moments):
        self.players = players
        self.fold_moments = fold_moments
        self.n = len(players)

    def get_associated_player_fold(self):
        for i in range(self.n):
            yield (self.players[i], self.fold_moments[i])

    def __str__(self):
        str_h = ""
        for i in range(len(self.players)):
            str_h += ("%s %s\n" % (self.players[i], FOLD_MOMENT[self.fold_moments[i]]))
        return str_h


def get_seat_number(line):
    return int(line.split(SEAT_NUMBER_SPLIT_LEFT)[1].split(SEAT_NUMBER_SPLIT_RIGHT)[0])


def extract_table_size(hand):
    table_size = int(hand[1].split(TABLE_SIZE_SPLIT_LEFT)[1].split(TABLE_SIZE_SPLIT_RIGHT)[0])
    return table_size


def extract_players(raw_hand, n_player):
    """
    :param raw_hand:    a hand stored as a list of lines
    :param n_player:    maximum number of player at table
    :return: return the list of players playing this hand
    """
    players = [DEFAULT_PLAYER for _ in range(n_player)]
    for line in raw_hand:

        if line.find("*** HOLE CARDS ***") == 0:
            break

        if line.find("Seat") == 0:
            seat_number = get_seat_number(line)
            delete_seat = line.split(": ")
            isolate_name = delete_seat[1].split(" (")
            players[seat_number-1] = isolate_name[0]

    return players


def extract_fold_moment(raw_hand, n_player):
    """
    :param raw_hand:    a hand stored as a list of lines
    :param n_player:    maximum number of player at table
    :return: return the list of moment when the players folded
    """

    fold_moment = [-1 for _ in range(n_player)]

    summary = False
    for line in raw_hand:

        if line.find("*** SUMMARY ***") == 0:  # Begin analysis when summary reached
            summary = True

        if summary and line.find("Seat") == 0:

            seat_number = get_seat_number(line)

            if line.find("folded before Flop") >= 0:
                fold_moment[seat_number-1] = 0
            elif line.find("folded on the Flop") >= 0:
                fold_moment[seat_number - 1] = 1
            elif line.find("folded on the Turn") >= 0:
                fold_moment[seat_number-1] = 2
            elif line.find("folded on the River") >= 0:
                fold_moment[seat_number-1] = 3
            else:
                fold_moment[seat_number-1] = 4

    return fold_moment
