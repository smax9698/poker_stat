from analyze_files import *


def fold_moment_data(hands):
    dict_moment = {}
    for hand in hands:
        for (player, fold_moment) in hand.get_associated_player_fold():
            if player != DEFAULT_PLAYER:
                if player not in dict_moment:
                    dict_moment.update({player: [0 for _ in range(6)]})
                dict_moment[player][fold_moment + 1] += 1

    return dict_moment
