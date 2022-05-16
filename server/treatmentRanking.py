from collections import defaultdict
# from ddi import SeleniumSearch
import pandas as pd



class treatmentRanking:

    def __init__(self):
        pass
        # self.selsearch = SeleniumSearch()

    ######################## fake #########################
    def update(self, anti_dict, drugs_in_use, db):
        pass

    # def update(self, anti_dict, drugs_in_use, db):
    #     """
    #     create initial rank to treatments based on MIC values
    #     future implement - will consider drugs traits and chemoinformatics.
    #     :param mic: all MIC values based on system inputs, dataframe
    #     :return dataframe of possible treatments
    #     """
    #     # s_drug = str(tuple(drugs_in_use)) if len(drugs_in_use) > 1 else str(tuple(drugs_in_use)).replace(',', '')
    #     d = ['Abilify', 'Ativan', 'Advil', 'Lasix', 'Aspirin']
    #     s_drug = str(tuple(d))
    #     q = '''SELECT Antibiotic, SUM(Major), SUM(Moderate), SUM(Minor) FROM DDI
    #         WHERE Drug in ''' + s_drug + '''GROUP BY Antibiotic'''
    #     res = db.select_from_db(q)
    #
    #     for a in res:
    #         r = [anti_dict[a[0]]]
    #         r.extend(a[1:])
    #         anti_dict[a[0]] = r
    #
    #     return anti_dict
        
        # false return
        # dict_initial_ranking = {
        #     'ceftriaxone': ['ceftriaxone', '10mg', 0.6, "2 Times a day with alot of water", 0.2],
        #     'ciprofloxacin': ['ciprofloxacin', '6mg', 0.7, "3 Times a day before meal", 0.7],
        #     'gentamicin': ['gentamicin', '40mg', 0.9, "1 pill before sleeping", 0.5],
        #     'imipenem': ['imipenem', '70mg', 0.8, "Do not take before sleeping", 0.8],
        #     'levofloxacin': ['levofloxacin', '50mg', 0.1, "1 pill after lunch", 0.3],
        #     'tetracycline': ['tetracycline', '100mg', 0.2, "Do not take before sleeping", 0.4],
        #     'tobramycin': ['tobramycin', '5mg', 0.4, "Take every 8 hours", 0.33],
        #     'AB32': ['AB32', '20mg', 0.3, "2 Times a day with alot of water", 0.9],
        #     'AB27': ['AB27', '15mg', 0.5, "Take every 8 hours", 0.1],
        #     'AB8': ['AB8', '15mg', 0.99, "1 pill before sleeping", 0.67],
        # }
        # df = pd.DataFrame.from_dict(dict_initial_ranking, columns=[
        #                             'Drug Name', 'MIC', 'MIC_Confidence', 'Comments', 'Rank'], orient='index')
        # df.sort_values(by='Rank', inplace=True, ascending=False)
