import pandas as pd
from db import Database

class contextAware:
    def __init__(self):
        self.db = None

    def close_db(self):
        self.db.close_connection()

    def open_db(self):
        self.db = Database()

    def update(self, anti_dict):
        """
        udpating antiobtics dict with the relevent GFR and coverage data per antibiotic
        :param anti_dict: current data on antibiotics, dict
        :return dict with updated values of GFR and Coverage of possible antibiotics treatments
        """
        # ranked_treatments = initial_ranking.to_dict(orient='records')

        return anti_dict

    def calculate_GFR(self, serum_cr, age, female):
        res = 175 * (serum_cr**(-1.154)) * (age**(-0.203))
        if female:
            res *= 0.742
        return res

    def get_coverage(self, drugs_dict):
        pass