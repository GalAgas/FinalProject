import pandas as pd
from db import Database

class contextAware:
    def __init__(self):
        self.db = None

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
        # after MIC completed, we can change this function to select from db only the relevent antibiotics.
        antibiotics = self.db.get_all_antibiotics()
        for ab in antibiotics:
            if ab[3] != -1 and ab[3] < GFR:
                del anti_dict[ab[1]]
            if ab[1] in anti_dict:
                anti_dict[ab[1]].append(ab[2])
        self.db.close_connection()

        final_dict = self.convert_to_list_of_dicts(anti_dict)

        return final_dict

    def calculate_GFR(self, serum_cr, age, female):
        res = 175 * (serum_cr**(-1.154)) * (age**(-0.203))
        if female:
            res *= 0.742
        return res

    def get_coverage(self, drugs_dict):
        pass

    def convert_to_list_of_dicts(self, anti_dict):
        df = pd.DataFrame.from_dict(anti_dict, columns=[
            'Drug_Name', 'MIC', 'MIC_Confidence', 'Comments', 'Rank', 'Coverage'], orient='index')
        final_dict = df.to_dict(orient='records')
        return final_dict
