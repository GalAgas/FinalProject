import pandas as pd
from flask import Flask, jsonify, request, json, abort
from flask_cors import CORS
from MICPredictor import MICPredictor
from treatmentRanking import treatmentRanking
from contextAware import contextAware


# configuration
DEBUG = True


class EndpointAction(object):
    """
    Endpoint class - contains the backend.
    when it called performers the action
    """

    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        return self.action()


class WebService(object):
    """
    Wrapper class for app
    creates and runs the app
    """

    def __init__(self, name):
        self.app = Flask(name)
        self.app.config.from_object(__name__)
        # enable CORS
        CORS(self.app, resources={r'/*': {'origins': '*'}})
        self.mic_predictor = MICPredictor()
        self.treatment_ranking = treatmentRanking()
        self.context_aware = contextAware()

    def run(self):
        self.app.run(debug=True)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        """
        Links between specific endpoint url to a given handler function
        :param endpoint: url, str
        :param endpoint_name: name of operation, str
        :param handler: callable function, called on request
        :return: void, adds the endpoint to the app
        """
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(
            handler), methods=['GET', 'POST'])

    def response(self, message, status):
        response = self.app.response_class(
            response=json.dumps(message),
            status=status,
            mimetype='application/json'
        )
        return response

    def generate_recommendation(self):
        gene_correlation = request.files['gene_correlation_csv']
        gene_correlation_txt = request.files['gene_correlation_txt']
        patient_id = request.form['id']
        try:
            if not self.check_valid_id(patient_id):
                return self.response("Invalid Id", 409)
            csv_file = self.read_csv_file(gene_correlation)
            txt_file = self.read_txt_file(gene_correlation_txt)
            self.check_valid_csv(csv_file)
            self.check_valid_txt(txt_file)
            if not self.check_valid_txt(gene_correlation_txt):
                return self.response("Invalid txt File", 400)

            mic = self.mic_predictor.predict(file)
            initial_ranking = self.treatment_ranking.rank(mic)
            final_ranking = self.context_aware.rank(initial_ranking)
            return jsonify(final_ranking)
        except Exception as e:
            print(e)
            return self.response("Something went worng!", 400)

    def check_valid_id(self, patient_id):
        # check in future public patients DB that patient id exists.
        return True

    def check_valid_txt(self, gene_correlation_txt):
        #  TODO: check who to run on file and read each line

    ## NEED TO CHECK ALL CASES ##
    def check_valid_csv(self, gene_correlation_csv):
        # check if the file is csv/xslx - front!
        required_columns = {"file": str, "gene": str, "contig": str, "start": int,
                            "end": int, "depth": float, "seqid": float, "seqcov": float,
                            "match_start": int, "match_end": int, "ref_gene_size": int}

        # rename columns name to lower case
        gene_correlation_csv.columns = gene_correlation_csv.columns.str.lower()
        # check if all the required columns exists
        if len(required_columns.keys()) != len(gene_correlation_csv):
            return self.response(f'expected {len(required_columns.keys())} columns but got {len(gene_correlation_csv)}', 400)
        for col_name in required_columns.keys():
            if col_name not in gene_correlation_csv:
                return self.response(f'column "{col_name}" missing', 400)
        # check if the 'file' column have 1 value
        if len(gene_correlation_csv["file"].unique()) != 1:
            return self.response(f'expected 1 unique value in column "file" but got {len(gene_correlation_csv["file"].unique())}', 400)
        # check there is no missing values in 'gene' column
        if gene_correlation_csv["gene"].isnull().any():
            return self.response("column 'gene' can't have missing values.")
        # check contig column values are in right format.
        for i, val in enumerate(gene_correlation_csv["contig"]):
            if not val.lower().startswith("contig") or not val[6:].isdigit():
                return self.response(f'Invalid value in column "contig" row {i}', 400)
        # check if all values in int/float columns are int/float.
        for i, col_name, col_type in enumerate(required_columns.items()):
            if col_type == int:
                if not all(isinstance(val,int) for val in gene_correlation_csv[col_name]):
                    return self.response(f'column {col_name} have invalid value in row {i}')
            elif col_type == float:
                if not all(isinstance(val,float) or isinstance(val,int) for val in gene_correlation_csv[col_name]):
                    return self.response(f'column {col_name} have invalid value in row {i}')
            if col_name == "seqid" or col_name == "seqcov":
                if not all(0 < val < 100 for val in gene_correlation_csv[col_name]):
                    return self.response(f'column {col_name} have invalid value in row {i}')

    def read_txt_file(self, path):
        file = open(path,"r")
        return file.read()

    def read_csv_file(self, path):
        return pd.read_csv(path)


web_service_app = WebService('webservice')
web_service_app.add_endpoint(endpoint='/generate', endpoint_name='generate recommendation',
                             handler=web_service_app.generate_recommendation)
web_service_app.run()
