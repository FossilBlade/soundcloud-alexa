from src.skill import app



if __name__ == '__main__':

    import json

    # alexa_request_payload = json.loads('test/requests/start_session.json')

    app.config['ASK_VERIFY_REQUESTS']=False
    app.run(host='0.0.0.0')