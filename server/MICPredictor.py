# need to add confidence
class MICPredictor:
    def __init__(self):
        pass

    def predict(self, csv_file, txt_file):
        return {
            'ceftriaxone': ['ceftriaxone', '10mg', 0.6, "2 Times a day with alot of water", 0.2],
            'ciprofloxacin': ['ciprofloxacin', '6mg', 0.7, "3 Times a day before meal", 0.7],
            'gentamicin': ['gentamicin', '40mg', 0.9, "1 pill before sleeping", 0.5],
            'imipenem': ['imipenem', '70mg', 0.8, "Do not take before sleeping", 0.8],
            'levofloxacin': ['levofloxacin', '50mg', 0.1, "1 pill after lunch", 0.3],
            'tetracycline': ['tetracycline', '100mg', 0.2, "Do not take before sleeping", 0.4],
            'tobramycin': ['tobramycin', '5mg', 0.4, "Take every 8 hours", 0.33],
            'AB32': ['AB32', '20mg', 0.3, "2 Times a day with alot of water", 0.9],
            'AB27': ['AB27', '15mg', 0.5, "Take every 8 hours", 0.1],
            'AB8': ['AB8', '15mg', 0.99, "1 pill before sleeping", 0.67],
        }
