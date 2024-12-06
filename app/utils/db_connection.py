import sqlite3


def get_connection():
    #return sqlite3.connect('../../../data/tour_agent.db3')
    return sqlite3.connect('data/tour_agent.db3')