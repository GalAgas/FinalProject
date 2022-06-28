from collections import defaultdict
import pandas as pd



class treatmentRanking:

    def __init__(self):
        pass

    def update(self, anti_dict, drugs_in_use, db):
        """
        create initial rank to treatments based on MIC values
        future implement - will consider drugs traits and chemoinformatics.
        :param mic: all MIC values based on system inputs, dataframe
        :return dataframe of possible treatments
        """
        s_drug = str(tuple(drugs_in_use)) if len(drugs_in_use) > 1 else str(tuple(drugs_in_use)).replace(',', '')
        # d = ['Abilify', 'Ativan', 'Advil', 'Lasix', 'Aspirin']
        # s_drug = str(tuple(d))
        q = '''SELECT Antibiotic, SUM(Major), SUM(Moderate), SUM(Minor) FROM DDI
            WHERE Drug in ''' + s_drug + '''GROUP BY Antibiotic'''
        res = db.select_from_db(q)

        if res:
            for a in res:
                r = [anti_dict[a[0]]]
                r.extend(a[1:])
                anti_dict[a[0]] = r
        else:
            for ab in anti_dict:
                r = [anti_dict[ab]]
                r.extend([0, 0, 0])
                anti_dict[ab] = r

        return anti_dict
