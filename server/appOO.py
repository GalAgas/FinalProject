import pandas as pd
from flask import Flask, jsonify, request, json, abort
from flask_cors import CORS
from MICPredictor import MICPredictor
from treatmentRanking import treatmentRanking
from contextAware import contextAware


# configuration
DEBUG = True

# # instantiate the app
# app = Flask(__name__)
# app.config.from_object(__name__)

# # enable CORS
# CORS(app, resources={r'/*': {'origins': '*'}})

# global variables for parameters
# patient_id = None
# file_path = None
# file = None
# mic_predictor = MICPredictor(file)
# treatment_ranking = treatmentRanking()
# context_aware = contextAware()


class EndpointAction(object):
    """
    Endpoint class - contains the backend.
    when it called performers the action
    """

    def __init__(self, action):
        self.action = action
        # self.backend = MyBack()

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
        ngs_file = request.files['ngs_file']
        patient_id = request.form['id']
        try:
            if not self.check_valid_id(patient_id):
                return self.response("Invalid Id", 400)
            if not self.check_valid_file(ngs_file):
                return self.response("Invalid NGS File", 400)
            file = self.read_file(ngs_file)
            mic = self.mic_predictor.predict(file)
            initial_ranking = self.treatment_ranking.rank(mic)
            final_ranking = self.context_aware.rank(initial_ranking)
            result = final_ranking.to_json(orient='index')
            parsed = json.loads(result)
            return json.dumps(parsed, indent=4)
        except Exception as e:
            print(e)
            return self.response("Something went worng!", 400)

    def check_valid_id(self, patient_id):
        # check vs file of id's that the id exists in.
        return True

    def check_valid_file(self, ngs_file):
        return True

    def read_file(self, path):
        return pd.read_csv(path)


web_service_app = WebService('webservice')
web_service_app.add_endpoint(endpoint='/generate', endpoint_name='generate recommendation',
                             handler=web_service_app.generate_recommendation)
web_service_app.run()
