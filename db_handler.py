import psycopg2
import sys
import time

def update_table_fold_moment(vector):
    try:
        conn = psycopg2.connect("dbname='poker' user='oscar' host='localhost' password='oscar'")
        cur = conn.cursor()

        cur.execute("SELECT * FROM players_fold_moment WHERE player_name=%s",(vector[0],))
        player_in_db = cur.fetchone()
        if(len(player_in_db) == 0):
            cur.execute("""INSERT INTO players_fold_moment (player_name, before_flop, at_flop, at_turn, at_river, 
            no_fold) VALUES (%s,%s,%s,%s,%s,%s);""",(vector[0], vector[2], vector[3], vector[4], vector[5], vector[6],))
        else:
            cur.execute("""UPDATE players_fold_moment SET before_flop=%s, at_flop=%s, at_turn=%s, at_river=%s, 
            no_fold=%s WHERE player_name=%s;""",(vector[2]+player_in_db[1], vector[3]+player_in_db[2],
            vector[4]+player_in_db[3], vector[5]+player_in_db[4], vector[6]+player_in_db[5], vector[0]))

        conn.commit()
        cur.close()
        conn.close()
    except ValueError:
        print("ValueError")


