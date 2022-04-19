import pandas as pd
from db import Database

class contextAware:
    def __init__(self):
        self.db = None

    def close_db(self):
        self.db.close_connection()

    def open_db(self):
        self.db = Database()

    def rank(self, initial_ranking):
        """
        future implement - will consider patient record data and medical center data.
        :param initial_ranking: inital ranking of treatments, dataframe
        :return dataframe of possible treatments
        """
        ranked_treatments = initial_ranking.to_dict(orient='records')

        return ranked_treatments

    def calculate_GFR(self, serum_cr, age, female):
        res = 175 * (serum_cr**(-1.154)) * (age**(-0.203))
        if female:
            res *= 0.742
        return res

    def sort_by_coverage(self, drugs_dict):
        pass