from collections import defaultdict

import pandas as pd


class treatmentRanking:
    def __init__(self):
        pass

    def rank(self, mic):
        # false return
        dict_initial_ranking = {
            'AB1': ['AB1', '10mg', "I'm a comment"],
            'AB5': ['AB5', '6mg', "I'm a comment too"],
            'AB2': ['AB2', '455mg', "I'm a comment three"],
            'AB18': ['AB18', '70mg', "I'm a comment for you"]
        }
        df = pd.DataFrame.from_dict(dict_initial_ranking, columns=['Drug Name', 'MIC', 'Comments'], orient='index')
        return df

