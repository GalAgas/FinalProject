import pandas as pd


class contextAware:
    def __init__(self):
        pass

    def rank(self, initial_ranking):
        """
        future implement - will consider patient record data and medical center data.
        :param initial_ranking: inital ranking of treatments, dataframe
        :return dataframe of possible treatments
        """
        ranked_treatments = initial_ranking.to_dict(orient='records')

        return ranked_treatments
