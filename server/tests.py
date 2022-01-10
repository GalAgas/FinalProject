from app import WebService
import pandas as pd


def check_valid_id():
    ws = WebService('webservice')
    assert ws.check_valid_id(123)


def check_read_text_file():
    ws = WebService('webservice')
    with open('DRR148121.contigs.length.txt') as f:
        lines = f.readlines()
    assert ws.read_text_file(f) == lines


def check_read_csv_file():
    ws = WebService('webservice')
    with open('DRR148121.abricate.card.1.1.gene.depth.csv') as correct:
        df = pd.read_csv(correct)
        assert ws.read_text_file(correct) == df


def check_valid_text():
    ws = WebService('webservice')
    with open('DRR148121.contigs.length.txt') as correct:
        assert ws.check_valid_txt(ws.read_text_file(correct)) == ''

    with open('other_file.txt') as incorrect:
        assert ws.check_valid_txt(ws.read_text_file(incorrect)) != ''


def check_valid_csv():
    ws = WebService('webservice')
    with open('DRR148121.abricate.card.1.1.gene.depth.csv') as correct:
        assert ws.check_valid_csv(ws.read_csv_file(correct)) == ''

    with open('other_file.csv') as incorrect:
        assert ws.check_valid_txt(ws.read_csv_file(incorrect)) != ''


def check_response():
    ws = WebService('webservice')
    assert ws.response('message', 200) == True


# def check_generate_recommendation():
#     ws = WebService('webservice')
