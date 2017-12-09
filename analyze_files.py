import os
import time
from hand_data_extractor import *
from db_handler import *
from data_analyzer import *

FILE_ANALYZE_DIR = "./to_analyze_files"


def extract_hand(raw_data):
    """
        :parameter  raw_data:   table containing all the lines of the readed file
        :return:    a list of hands stored as a list of sub-lists. Each sub-list contains the
                    lines of one specific hand
    """
    hands = []  # list of raw hands
    current_hand = []
    new_hand = False

    for line in raw_data:
        if line == "\n":  # Start of a new end
            new_hand = True
        else:
            if new_hand:  # Safe the previous hand
                hands.append(current_hand)
                current_hand = [line]
                new_hand = False
            else:
                current_hand.append(line)  # Build the new hand

    hands.append(current_hand)

    return hands


def analyze_one(file_path):
    """
    :param file_path: path to text file to analyze
    """

    raw_data = []
    with open(file_path, 'r') as f:
        for line in f:
            raw_data.append(line)
        f.close()

    raw_hands = extract_hand(raw_data)  # Raw hands
    table_size = extract_table_size(raw_hands[0])  # Table size

    analyzed_hands = []

    for raw_hand in raw_hands:  # Extract useful data from raw_hand
        players = extract_players(raw_hand, table_size)
        fold_moments = extract_fold_moment(raw_hand, table_size)

        analyzed_hands.append(Hand(players, fold_moments))

    dic = fold_moment_data(analyzed_hands)
    for player in dic:
        tab = dic[player]
        tab.insert(0, player)
        update_table_fold_moment(tab)


def analyze_all():
    """
        For each file in the "to analyse directory" call analyze_one.
    """
    list_files = os.listdir(FILE_ANALYZE_DIR)

    for file in list_files:
        file_path = FILE_ANALYZE_DIR+"/%s" % file
        analyze_one(file_path)


if __name__ == '__main__':
    analyze_all()
