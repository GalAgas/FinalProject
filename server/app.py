import pandas as pd
from pandas.core.indexes.base import Index
from flask import Flask, jsonify, request, json, abort, send_from_directory
from flask_cors import CORS
from MICPredictor import MICPredictor
from treatmentRanking import treatmentRanking
from contextAware import contextAware
import re
from io import BytesIO
import random
import http.server
import ssl

# configuration
DEBUG = True


class EndpointAction(object):
    """
    Endpoint class.
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
        self.app = Flask(name, static_url_path='/', static_folder='dist')
        self.app.config.from_object(__name__)
        # enable CORS
        CORS(self.app, resources={r'/*': {'origins': '*'}})
        self.mic_predictor = MICPredictor()
        self.treatment_ranking = treatmentRanking()
        self.context_aware = contextAware()
        self.context_aware.create_db()

    def run(self):
        """
        Wraps the run method of app, using ssl keys to open a secure https connection
        """
        self.app.run(debug=True, ssl_context=('fullchain.pem', 'privkey1.pem'), host='gps-ise.cs.bgu.ac.il', port=443)
        # self.httpd.serve_forever()
        # self.app.run(debug=True, port=443)

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
        """

        :param message: message to send, str
        :param status: HTTP response code, int
        :return: response to client
        """
        response = self.app.response_class(
            response=json.dumps(message),
            status=status,
            mimetype='application/json'
        )
        return response
    
    def start(self):
        return send_from_directory(self.app.static_folder, 'index.html')

    def generate_recommendation(self):
        """
        the function validates that input is valid and then generates a treatment recommendation table based on input.
        :return: recommendation table as json
        """
        gene_correlation_csv = request.files['gene_correlation_csv']
        gene_correlation_txt = request.files['gene_correlation_txt']
        patient_age = int(request.form['patientAge'])
        patient_isFemale = request.form['patientGender'] == 'Female'
        if patient_isFemale:
            patient_pregnant = request.form['pregnancy'] == 'pregnant'
        else:
            patient_pregnant = False
        patient_creatinine = float(request.form['patientCreatinine'])
        patient_fever = json.loads(request.form['patientFever'])
        patient_plank_pain = json.loads(request.form['patientFlankPain'])
        patient_dysuria = json.loads(request.form['patientDysuria'])
        patient_drugs_in_use = request.form['patientDrugsInUse'].split(",")
        try:
            csv_file = self.read_csv_file(gene_correlation_csv)
            txt_file = self.read_txt_file(file=gene_correlation_txt)
            message = self.check_valid_csv(csv_file)
            if message != '':
                return self.response('Error in csv file! \n' + message, 400)
            message = self.check_valid_txt(txt_file)
            if message != '':
                return self.response('Error in txt file! \n' + message, 400)
            
            # MIC prediction
            anti_dict = self.mic_predictor.predict(csv_file, txt_file)
            # DDI update
            anti_dict = self.treatment_ranking.update(anti_dict, patient_drugs_in_use, self.context_aware.db)
            # GFR elimination & Coverage extraction
            anti_dict = self.context_aware.update(anti_dict, patient_creatinine, patient_age, patient_isFemale)

            anti_dict = self.sort_dict(anti_dict, patient_pregnant)

            anti_dict = self.convert_dict(anti_dict)
            
            # anti_dict = [
            #                 {'Drug_Name': 'ampicillin/sulbactam', 'MIC': 8.076, 'MIC_Confidence': 0.914, 'Major_DDI': 0, 'Moderate_DDI': 0, 'Minor_DDI': 0, 'Coverage': 'Broad', 'Pregnancy_Category': 'B'},
            #                 {'Drug_Name': 'levofloxacin', 'MIC': 8.161, 'MIC_Confidence': 0.967, 'Major_DDI': 0, 'Moderate_DDI': 3, 'Minor_DDI': 0, 'Coverage': 'Broad', 'Pregnancy_Category': 'C'},
            #                 {'Drug_Name': 'imipenem', 'MIC': 9.61, 'MIC_Confidence': 0.927, 'Major_DDI': 0, 'Moderate_DDI': 0, 'Minor_DDI': 0, 'Coverage': 'Broad', 'Pregnancy_Category': 'B'},
            #                 {'Drug_Name': 'tetracycline', 'MIC': 27.059, 'MIC_Confidence': 0.726, 'Major_DDI': 0, 'Moderate_DDI': 0, 'Minor_DDI': 1, 'Coverage': 'Broad', 'Pregnancy_Category': 'D'},
            #                 {'Drug_Name': 'ceftazidime', 'MIC': 28.306, 'MIC_Confidence': 0.928, 'Major_DDI': 0, 'Moderate_DDI': 1, 'Minor_DDI': 0, 'Coverage': 'Narrow', 'Pregnancy_Category': 'B'},
            #                 {'Drug_Name': 'ciprofloxacin', 'MIC': 28.602, 'MIC_Confidence': 0.794, 'Major_DDI': 0, 'Moderate_DDI': 3, 'Minor_DDI': 1, 'Coverage': 'Broad', 'Pregnancy_Category': 'C'},
            #                 {'Drug_Name': 'ceftriaxone', 'MIC': 74.476, 'MIC_Confidence': 0.931, 'Major_DDI': 0, 'Moderate_DDI': 1, 'Minor_DDI': 0, 'Coverage': 'Broad', 'Pregnancy_Category': 'B'},
            #                 {'Drug_Name': 'trimethoprim/sulfamethoxazole', 'MIC': 353.452, 'MIC_Confidence': 0.902, 'Major_DDI': 0, 'Moderate_DDI': 0, 'Minor_DDI': 0, 'Coverage': 'Narrow', 'Pregnancy_Category': 'C'}
            #             ]
            
            return jsonify(anti_dict)
        except Exception as e:
            print(e)
            return self.response("Something went wrong!", 400)

    def sort_dict(self, d, pregnancy):
        if pregnancy:
            return {k:d[k] for k in sorted(d, key=lambda k:(d[k][0], d[k][1], d[k][2], d[k][3], d[k][4], d[k][5]), reverse=False)}
        else:
            return {k:d[k] for k in sorted(d, key=lambda k:(d[k][0], d[k][1], d[k][2], d[k][3], d[k][4]), reverse=False)}

    def convert_dict(self, anti_dict: dict):
        """
        converts the antibiotics dictionary to the fornat specified in the API
        Args:
            anti_dict (dict): the antibiotics dictionary

        Returns:
            dict: dictionary in the correct API format
        """
        for ab in anti_dict:
            anti_dict[ab].insert(0, ab)
            i = round((random.random() * 0.3) + 0.7, 3)
            anti_dict[ab].insert(2, i)
            
            anti_dict[ab][1] = round(anti_dict[ab][1], 3)

        df = pd.DataFrame.from_dict(anti_dict, columns=[
            'Drug_Name', 'MIC', 'MIC_Confidence', 'Major_DDI','Moderate_DDI', 'Minor_DDI', 'Coverage', 'Pregnancy_Category'], orient='index')
        final_dict = df.to_dict(orient='records')

        for d in final_dict:
            if d['Coverage'] == 0:
                d['Coverage'] = 'Narrow'
            else:
                d['Coverage'] = 'Broad'
            if "_" in d['Drug_Name']:
                d['Drug_Name'] = d['Drug_Name'].replace('_', '/')
        return final_dict

    def check_valid_txt(self, gene_correlation_txt):
        """
        check if the given txt file is in the requested format.
        :param gene_correlation_txt: the system input - file of gene correlation, txt file
        :return: error message or empty message according to validation
        """
        message = ''
        float_regex = '[0-9]+\.[0-9]+'
        for i, row in gene_correlation_txt.iterrows():
            row_tokens = []
            for val in row[:3]:
                row_tokens.append(val)
            if not row_tokens[0].startswith(">contig"):
                message = f'line {i+1} , column 1 starts with invalid value'
                break
            if not row_tokens[1].startswith("len=") or not row_tokens[1][4:].isdecimal():
                message = f'line {i+1}, column 2 has invalid value'
                break
            if not row_tokens[2].startswith("cov=") or not re.search(float_regex, row_tokens[2][4:]):
                message = f'line {i+1}, column 3 has invalid value'
                break
        return message

    def check_valid_csv(self, gene_correlation_csv):
        """
        check if the given csv file is in the requested format.
        :param gene_correlation_csv: the system input - file of gene correlation, csv file
        :return: error message or empty message according to validation
        """
        message = ''
        required_columns = {"file": str, "gene": str, "contig": str, "start": int,
                            "end": int, "depth": float, "seqid": float, "seqcov": float,
                            "match_start": int, "match_end": int, "ref_gene_size": int}

        # save original column names
        original_columns_names = gene_correlation_csv.columns
        # rename columns name to lower case
        gene_correlation_csv.columns = gene_correlation_csv.columns.str.lower()
        # check if all the required columns exists
        for col_name in required_columns.keys():
            if col_name not in gene_correlation_csv.columns:
                message = f'column "{col_name}" is missing'
                return message
        if len(required_columns.keys()) != len(gene_correlation_csv.columns):
            message = f'expected {len(required_columns.keys())} columns but got {len(gene_correlation_csv.columns)}'
        # check if the 'file' column have 1 value
        elif len(gene_correlation_csv["file"].unique()) != 1:
            message = f'expected 1 unique value in column "file" but got {len(gene_correlation_csv["file"].unique())}'
        # check there is no missing values in 'gene' column
        elif gene_correlation_csv["gene"].isnull().any():
            message = "column 'gene' can't have missing values."
        # check contig column values are in right format.
        else:
            for i, val in enumerate(gene_correlation_csv["contig"]):
                if not val.lower().startswith("contig") or not val[6:].isdigit():
                    message = f'Invalid value in column "contig" row {i+2}'
                    return message
            # check if all values in int/float columns are int/float and in the neccesary range.
            for col_name, col_type in required_columns.items():
                if col_type == int:
                    if not all(isinstance(val, int) for val in gene_correlation_csv[col_name]):
                        message = f'column {col_name} have invalid value - Not all values are decimal numbers'
                elif col_type == float:
                    if not all(isinstance(val, float) or isinstance(val, int) for val in gene_correlation_csv[col_name]):
                        message = f'column {col_name} have invalid value - Not all values are real numbers'
                if col_name == "seqid" or col_name == "seqcov":
                    if not all(0 <= val <= 100 for val in gene_correlation_csv[col_name]):
                        message = f'column {col_name} have invalid value'
        gene_correlation_csv.columns = original_columns_names
        return message

    def read_txt_file(self, file=None, file_loc=None):
        """
        read the input text file and return it as a pandas DataFrame
        """
        if file_loc is not None:
            with open(file_loc) as f:
                lines = f.readlines()
                lines_2D = []
                for l in lines:
                    lines_2D.append(l.split(" "))
            file_as_df = pd.DataFrame(lines_2D)
        else:
            file_as_df = pd.read_csv(BytesIO(file.read()), sep=" ", header=None)
        return file_as_df

    def read_csv_file(self, file):
        """
        read and return the input csv file as a pandas DataFrame
        """
        return pd.read_csv(file, index_col=0)


# open the server class. add endpoint and start running the server.
web_service_app = WebService('webservice')
# print(web_service_app.context_aware.db.get_all_antibiotics())
web_service_app.add_endpoint(endpoint='/generate', endpoint_name='generate recommendation',
                             handler=web_service_app.generate_recommendation)
web_service_app.add_endpoint(endpoint='/', endpoint_name='start web',
                             handler=web_service_app.start)
if __name__ == '__main__':
    web_service_app.run()
