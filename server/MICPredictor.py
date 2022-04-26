from gps_lib import predict as pred

# MIC = pred.predict_MIC('abaumannii', sample_path_dir=None)
# print('\n\n\n------------------------------------------------------------------------')
# print(MIC)
# print('------------------------------------------------------------------------\n\n\n')


# need to add confidence
class MICPredictor:
    def __init__(self):
        pass

    def predict(self, csv_file, txt_file):
        # MIC = pred.predict_MIC('abaumannii', sample_path_dir=None)
        MIC = pred.predict_MIC('abaumannii', csv_file=csv_file, txt_file=txt_file)
        return MIC
        
        # return {
        #     'Ceftriaxone': ['ceftriaxone', '10mg', 0.6, "2 Times a day with alot of water", 0.2],
        #     'Ciprofloxacin': ['ciprofloxacin', '6mg', 0.7, "3 Times a day before meal", 0.7],
        #     'Gentamicin': ['gentamicin', '40mg', 0.9, "1 pill before sleeping", 0.5],
        #     'Imipenem': ['imipenem', '70mg', 0.8, "Do not take before sleeping", 0.8],
        #     'Levofloxacin': ['levofloxacin', '50mg', 0.1, "1 pill after lunch", 0.3],
        #     'Tetracycline': ['tetracycline', '100mg', 0.2, "Do not take before sleeping", 0.4],
        #     'Tobramycin': ['tobramycin', '5mg', 0.4, "Take every 8 hours", 0.33],
        #     'Moxifloxacin': ['Moxifloxacin', '20mg', 0.3, "2 Times a day with alot of water", 0.9],
        #     'Doripenem': ['Doripenem', '15mg', 0.5, "Take every 8 hours", 0.1],
        #     'Ampicillin': ['Ampicillin', '15mg', 0.99, "1 pill before sleeping", 0.67],
        # }
