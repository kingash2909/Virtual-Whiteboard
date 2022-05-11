import os

from flask import Flask, request, jsonify, render_template
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def textdata():
    text_from_notepad = request.form['text']
    with open('workfile.txt', 'w') as f:
        f.write(text_from_notepad)
    path_to_store_txt = "workfile.txt"
    return send_file(path_to_store_txt, as_attachment=True)




@app.route('/token')
def generate_token():
    # get credentials from environment variables
    TWILIO_ACCOUNT_SID = 'AC404f7bbb2a8b4f40f282c957c5f8c477'
    TWILIO_SYNC_SERVICE_SID = 'IS3c04777aafcbc96ab285ed09e6d608fd'
    TWILIO_API_KEY = 'SKd132e020fbda4257b06f91f1a6abd9d6'
    TWILIO_API_SECRET = 'nhid4oItz2C1KeiubAJ5Dj9dRjIEL1FN'
    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant)
    return jsonify(identity=username, token=token.to_jwt().decode())
