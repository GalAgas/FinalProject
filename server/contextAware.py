import pandas as pd


class contextAware:
    def __init__(self):
        pass

    def rank(self, initial_ranking):
        ranked_treatments = initial_ranking.to_dict(orient='records')

        return ranked_treatments
