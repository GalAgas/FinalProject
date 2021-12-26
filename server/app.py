from flask import Flask, jsonify, request, json
from flask_cors import CORS
from MICPredictor import MICPredictor
from treatmentRanking import treatmentRanking
from contextAware import contextAware


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# global variables for parameters
patient_id = None
file_path = None
file = None
mic_predictor = MICPredictor(file)
treatment_ranking = treatmentRanking()
context_aware = contextAware()

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/generate', methods=['GET'])
def generate_recommendation():
    try:
        mic = mic_predictor.predict()
        initial_ranking = treatment_ranking.rank(mic)
        final_ranking = context_aware.rank(initial_ranking)
        result = final_ranking.to_json(orient='index')
        parsed = json.loads(result)
        return json.dumps(parsed, indent=4)
    except Exception as e:
        print(e)
        return response("Something went worng!", 400)

@app.route('/check', methods=['GET'])
def validate_details():
    details = request.get_json()
    patient_id = details['id']
    file_path = details['ngs_file']
    if not check_valid_id(patient_id):
        return response("Invalid id", 400)
    if not check_valid_file(file_path):
        return response("Invalid file", 400)

    return response("All good", 200)

def response(message, status):
    response = app.response_class(
        response=json.dumps(message),
        status=status,
        mimetype='application/json'
    )
    return response

def check_valid_id(patient_id):
    # check vs file of id's that the id exists in.
    pass


def check_valid_file(file_path):
    file = read_file(file_path)
    pass


def read_file():
    pass

if __name__ == '__main__':
    app.run()