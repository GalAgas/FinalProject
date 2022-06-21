import pandas as pd
from db import Database

class contextAware:
    def __init__(self):
        self.db = None
        # self.pregnancy_dict = {
        #     'A':0,
        #     'B':1,
        #     'C':2,
        #     'D':3,
        #     'E':4,
        # }

    def open_db(self):
        self.db.open_connection()

    def close_db(self):
        self.db.close_connection()

    def create_db(self):
        self.db = Database()


    def update(self, anti_dict, creatinine, age, isFemale):
        """
        udpating antiobtics dict with the relevent GFR and coverage data per antibiotic
        :param anti_dict: current data on antibiotics, dict
        :return dict with updated values of GFR and Coverage of possible antibiotics treatments
        """
        # ranked_treatments = initial_ranking.to_dict(orient='records')
        self.db.open_connection()
        GFR = self.calculate_GFR(creatinine, age, isFemale)
        # after MIC completed, we can change this function to select from db only the relevant antibiotics.
        antibiotics = self.db.get_all_antibiotics()
        for ab in antibiotics:
            if ab[3] != -1 and ab[3] < GFR and ab[1] in anti_dict:
                del anti_dict[ab[1]]
                continue
            if ab[1] in anti_dict:
                if ab[2] == 'Broad':
                    res = 1
                elif ab[2] == 'Narrow':
                    res = 0
                anti_dict[ab[1]].append(res)
                
            anti_dict[ab[1]].append(ab[4])
            
        self.db.close_connection()
    
        return anti_dict

    def calculate_GFR(self, serum_cr, age, female):
        res = 175 * (serum_cr**(-1.154)) * (age**(-0.203))
        if female:
            res *= 0.742
        return res

    def get_coverage(self, drugs_dict):
        pass

