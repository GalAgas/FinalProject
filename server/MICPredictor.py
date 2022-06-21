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

