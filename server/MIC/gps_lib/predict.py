import os
from tqdm import tqdm
import h2o
import pandas as pd
import numpy as np
from autoxgb.cli.predict import PredictAutoXGBCommand
from MIC.gps_lib.parse_raw_utils import get_isolate_features, get_isolate_features_from_site

MODELS_DIR = 'server\MIC\models'
SAMPLE_PATH_DIR = 'server\MIC\mic_files'

'''
models_dir - models directory path containing all models in the above hirarchy:
    - specie x
        - anti a
            - model
                model files for this combination (h2o format or autoxgb format for now)
            - data_param.csv
            - features.csv
            - model_param.csv
        - anti b
        .....
spceis - species name of the input isolate
sample_path_dir - the path to directory containing the two files describing the isolates genotype information.
'''
def predict_MIC(spceis, sample_path_dir=None, csv_file=None, txt_file=None):
    models_dir = MODELS_DIR
    MIC = {}
    for anti_dir in tqdm(os.listdir(models_dir + '/' + spceis)):
        if '.ipynb' in anti_dir:
            continue
        model, data_param, model_param, features = get_model(models_dir + '/' + spceis + '/' + anti_dir)
        X = parse_sample(sample_path_dir, data_param, features, csv_file, txt_file)
        MIC[anti_dir] = model_predict(X, model, model_param)
    return MIC


def get_model(model_dir):
    model_param = pd.read_csv(model_dir + '/model_param.csv').iloc[0]
    data_param = pd.read_csv(model_dir + '/data_param.csv').iloc[0]
    features = pd.read_csv(model_dir + '/features.csv')['features']
    print(model_param)
    if model_param['model_name'] == 'h2o':
        model = load_h2o_model(model_dir)
    elif model_param['model_name'] == 'autoxgb':
        model = load_autoxgb_model(model_dir)
    else:
        print('Unkown saved model')
        print('at path: {}'.format(model_dir))
    return model, data_param, model_param, features


def load_h2o_model(model_dir):
    h2o.init()
    model_path = os.listdir(model_dir+'/model')[0]
    model = h2o.load_model(model_dir+'/model/'+model_path)
    return model


def load_autoxgb_model(model_dir):
    return model_dir+'/model'


def parse_sample(sample_path_dir, data_param, features,csv_file, txt_file):
    print(data_param)
    
    from_files = False
    if csv_file is not None and txt_file is not None:
        from_files = True
    if sample_path_dir is None:
        sample_path_dir = SAMPLE_PATH_DIR
        
    if from_files:
        X = get_isolate_features_from_site(csv_file, txt_file)    
    else:
        X = get_isolate_features(sample_path_dir)
    X[list(set(features) - set(X.columns.values))] = 0
    sample = X[features]
    return sample


def model_predict(X, model, model_param):
    data_dir = 'tmp'
    sample_path = '{}/sample.csv'.format(data_dir)
    os.makedirs(data_dir, exist_ok=True)
    if model_param['model_name'] == 'h2o':  
        X.to_csv(sample_path)
        sample = h2o.import_file('{}/sample.csv'.format(data_dir))
        preds = model.predict(sample).as_data_frame().iloc[0].iloc[0]
    elif model_param['model_name'] == 'autoxgb':
        X['biosample_id'] = 0
        X.to_csv(sample_path)
        PredictAutoXGBCommand(model, sample_path, '{}/preds.csv'.format(data_dir)).execute()
        preds = pd.read_csv('{}/preds.csv'.format(data_dir)).iloc[0].iloc[1]
    else:
        print('Unkown saved model')
        print('at path: {}'.format(model_dir))
    return np.power(preds, 2)