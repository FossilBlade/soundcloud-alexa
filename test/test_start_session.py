from src.skill import app,start_playlist

import pytest, json
from datetime import datetime

@pytest.fixture
def client():
    app.config['ASK_VERIFY_REQUESTS']=False
    with app.test_client() as client:
        yield client

def get_request_json(request_type):

    with open('test/requests/{}.json'.format(request_type)) as json_file:
        request = json.load(json_file)

    return request


def test_start_session_new_user(client):
    req = get_request_json('start_session')

    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")

    req['session']['user']['userId'] = 'New User '+timestampStr
    rs = client.post('/raush', json=req)
    assert rs.status_code == 200

    res_json=rs.get_data().decode('utf-8')
    json_data = json.loads(res_json)
    print(res_json)
    assert 'playing the latest podcast' in json_data['response']['outputSpeech']['text'].lower()


def test_next(client):
    rs = client.post('/raush', json=get_request_json('next'))
    assert rs.status_code == 200

    res_json=rs.get_data().decode('utf-8')
    json_data = json.loads(res_json)
    print(res_json)
    assert 'playing next' in json_data['response']['outputSpeech']['text'].lower()


def test_previous(client):
    rs = client.post('/raush', json=get_request_json('previous'))
    assert rs.status_code == 200

    res_json=rs.get_data().decode('utf-8')
    json_data = json.loads(res_json)
    print(res_json)
    assert 'playing previous' in json_data['response']['outputSpeech']['text'].lower()