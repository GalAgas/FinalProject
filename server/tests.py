import flask
from app import WebService
from MICPredictor import MICPredictor
from contextAware import contextAware
from treatmentRanking import treatmentRanking
import pandas as pd
import pytest


# Test 0.1-0.5
def test_init_webservice():
    ws = WebService('webservice')
    assert isinstance(ws, WebService)
    assert isinstance(ws.mic_predictor, MICPredictor)
    assert isinstance(ws.context_aware, contextAware)
    assert isinstance(ws.treatment_ranking, treatmentRanking)
    assert isinstance(ws.app, flask.Flask)


# Test 1.1-1.3
def test_read_txt_file():
    ws = WebService('webservice')
    file_location = '../PossibleInputs/DRR148121.contigs.length.txt'
    with open(file_location) as f:
        lines = f.readlines()
    file_as_df = ws.read_txt_file(file_loc=file_location)
    assert type(file_as_df) == pd.DataFrame
    assert len(file_as_df) == len(lines)
    assert ws.check_valid_txt(file_as_df) == ''


# Test 2.1-2.3
def test_fail_read_txt_file():
    ws = WebService('webservice')
    file_location = '../PossibleInputs/DRR148121.contigs.length - Copy.txt'
    with open(file_location) as f:
        lines = f.readlines()
    file_as_df = ws.read_txt_file(file_loc=file_location)
    assert type(file_as_df) == pd.DataFrame
    assert len(file_as_df) == len(lines)
    assert ws.check_valid_txt(file_as_df) != ''


# Test 3.1-3.3
def test_read_csv_file():
    ws = WebService('webservice')
    file_location = '../PossibleInputs/DRR148121.abricate.card.1.1.gene.depth.csv'
    with open(file_location) as f:
        lines = f.readlines()
    file_as_df = ws.read_csv_file(file_location)
    assert type(file_as_df) == pd.DataFrame
    assert len(file_as_df) == len(lines) - 1  # line of headers
    assert ws.check_valid_csv(file_as_df) == ''


# Test 4.1-4.3
def test_fail_read_csv_file():
    ws = WebService('webservice')
    file_location = '../PossibleInputs/DRR148121.abricate.card.1.1.gene.depth - Copy.csv'
    with open(file_location) as f:
        lines = f.readlines()
    file_as_df = ws.read_csv_file(file_location)
    assert type(file_as_df) == pd.DataFrame
    assert len(file_as_df) == len(lines) - 1  # line of headers
    assert ws.check_valid_csv(file_as_df) != ''


# Test 5.1-5.3
def test_response():
    ws = WebService('webservice')
    my_response = ws.response('message', 200)
    assert type(my_response) == flask.Response
    assert my_response.status == '200 OK'
    assert my_response.mimetype == 'application/json'


# Test 6.1-6.3
def test_sort_dict():
    d = {'drug1': [28, 0, 0, 2, 8, 6],
         'drug5': [30, 1, 0, 7, 5, 2],
         'drug3': [28, 1, 0, 2, 10, 6],
         'drug2': [28, 1, 0, 2, 8, 6],
         'drug4': [30, 1, 0, 2, 10, 6],
         }
    ws = WebService('webservice')
    sorted_dict = ws.sort_dict(d,True)
    assert len(sorted_dict) == len(d)
    for i in range(1, len(sorted_dict)):
        lst1 = sorted_dict['drug'+str(i)]
        lst2 = sorted_dict['drug'+str(i+1)]
        assert len(lst1) == len(lst2)
        idx_gt = -1
        idx_lt = -1
        for j in range(len(lst1)):
            if lst1[j] > lst2[j]:
                idx_gt = j
                break
        for j in range(len(lst1)):
            if lst1[j] < lst2[j]:
                idx_lt = j
                break
        if idx_lt < idx_gt:
            assert True


# Test 7.1-7.4
def test_calculate_GFR():
    ca = contextAware()
    assert round(ca.calculate_GFR(1.2, 25, True), 3) == 54.738
    assert round(ca.calculate_GFR(1.2, 25, False), 3) == 73.770
    assert round(ca.calculate_GFR(1.7, 56, False), 3) == 41.900
    assert round(ca.calculate_GFR(1.4, 76, False), 3) == 49.272


dict_after_mic = {'ampicillin_sulbactam': 8.075956064060623,
                  'ceftazidime': 28.3055452527993,
                  'ceftriaxone': 74.47627086024058,
                  'ciprofloxacin': 28.601612769130078,
                  'gentamicin': 50.41656050093703,
                  'imipenem': 9.610354409383595,
                  'levofloxacin': 8.160683683234287,
                  'tetracycline': 27.058867558883055,
                  'tobramycin': 471.92336817920074,
                  'trimethoprim_sulfamethoxazole': 353.4524013677756,
                }


# Test 8.1-8.3
def test_update_tr():
    ws = WebService('webservice')
    dict_after_update = ws.treatment_ranking.update(dict_after_mic,['Ativan', 'Bunavail'], ws.context_aware.db)
    assert len(dict_after_update) <= len(dict_after_mic)
    for ab in dict_after_update:
        assert type(dict_after_update[ab]) == list
        assert len(dict_after_update[ab]) == 4
        assert type(dict_after_update[ab][2]) == int


dict_after_update_tr = {'ampicillin_sulbactam': [8.075956064060623, 0, 1, 0],
                        'ceftazidime': [28.3055452527993, 1, 0, 0],
                        'ceftriaxone': [74.47627086024058, 0, 0, 1],
                        'ciprofloxacin': [28.601612769130078, 0, 1, 1],
                        'gentamicin': [50.41656050093703, 0, 0, 0],
                        'imipenem': [9.610354409383595, 0, 0, 0],
                        'levofloxacin': [8.160683683234287, 0, 0, 1],
                        'tetracycline': [27.058867558883055, 0, 0, 0],
                        'tobramycin': [471.92336817920074, 1, 0, 0],
                        'trimethoprim_sulfamethoxazole': [353.4524013677756, 0, 0, 0]}


# Test 9.1-9.3
def test_update_ca():
    ws = WebService('webservice')
    dict_after_update = ws.context_aware.update(dict_after_update_tr, 1.5, 25, False)
    assert len(dict_after_update) <= len(dict_after_update_tr)
    for ab in dict_after_update:
        assert type(dict_after_update[ab]) == list
        assert len(dict_after_update[ab]) == 6
        assert type(dict_after_update[ab][5]) == str
