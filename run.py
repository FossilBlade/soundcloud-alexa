from src.skill import app



if __name__ == '__main__':
    app.config['ASK_VERIFY_REQUESTS']=False
    app.run(host='0.0.0.0')