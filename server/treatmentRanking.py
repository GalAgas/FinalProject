from collections import defaultdict

import pandas as pd


class treatmentRanking:
    def __init__(self):
        pass

    def rank(self, mic):
        # false return
        dict_initial_ranking = {
            'AB1': ['AB1', '10mg', "I'm a comment", 0.8],
            'AB5': ['AB5', '6mg', "I'm a comment too", 0.6],
            'AB2': ['AB2', '455mg', "I'm a comment three", 0.3],
            'AB18': ['AB18', '70mg', "I'm a comment for you", 0.5]
        }
        df = pd.DataFrame.from_dict(dict_initial_ranking, columns=['Drug Name', 'MIC', 'Comments', 'Rank'], orient='index')
        df.sort_values(by='Rank', inplace=True, ascending=False)
        return df

