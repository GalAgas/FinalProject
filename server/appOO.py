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
        self.patient_id = None
        self.file_path = None
        self.file = None
        self.mic_predictor = MICPredictor(self.file)
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
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=['GET'])

    def validate_details(self):
        details = request.get_json()
        patient_id = details['id']
        file_path = details['ngs_file']
        if not self.check_valid_id(patient_id):
            return self.response("Invalid id", 400)
        if not self.check_valid_file(file_path):
            return self.response("Invalid file", 400)

        return self.response("All good", 200)

    def response(self, message, status):
        response = self.app.response_class(
            response=json.dumps(message),
            status=status,
            mimetype='application/json'
        )
        return response


    def generate_recommendation(self):
        try:
            mic = self.mic_predictor.predict()
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
        self.patient_id = patient_id
        return True


    def check_valid_file(self, file_path):
        self.file_path = file_path
        self.file = self.read_file()
        return True


    def read_file(self):
        # return pd.read_csv(self.file_path)
        return "I'm a file"


web_service_app = WebService('webservice')
web_service_app.add_endpoint(endpoint='/check', endpoint_name='validate details', handler=web_service_app.validate_details)
web_service_app.add_endpoint(endpoint='/generate', endpoint_name='generate recommendation', handler=web_service_app.generate_recommendation)
web_service_app.run()


