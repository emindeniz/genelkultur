# Python standard libraries
import json
import os
import datetime
import sqlite3
import traceback
import random

# Third-party libraries
from flask import Flask, redirect, request, url_for, render_template, jsonify
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_caching import Cache
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from user import User
from question import Question

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_PROVIDER_AUTHENTICATION_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# Configure the app to use Flask-Caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    if current_user.is_authenticated:
        print("Rendering template for logout")
        return render_template('index.html', logged_in=True)
    else:
        print("Rendering template for login")
        return render_template('index.html', logged_in=False)
    
@app.route("/play")
@login_required
def play():
    question = Question().get_random()
    current_user.increment_asked()
    return render_template('play.html', question_text = question.question_text,
                           question_id = question.id,
                           question_score = question.score,
                           question_num_letters = len(question.answer))

@app.route("/stats")
@login_required
def stats():
    user = current_user.get_user_with_stats()

    # Create a dictionary with the variables
    template_variables = {
        'user_pic': user.profile_pic,
        'user_name': user.name,
        'user_email': user.email,
        'questions_asked': user.questions_asked,
        'questions_correct': user.questions_correct,
        'questions_incorrect': user.questions_incorrect
    }

    # Render the template with the variables
    return render_template('stats.html', **template_variables)


@app.route('/check_answer', methods=['POST'])
def check_answer():
    print('Checking Answer')
    data_from_js = request.get_json()
    # Process data and return a response
    question_id = data_from_js.get('question_id')
    user_answer = data_from_js.get('userAnswer')
    question = get_question(question_id=question_id)
    print(question_id,user_answer)
    if user_answer.lower()==question.answer.lower():
        current_user.increment_correct()
        result = {'isAnswerCorrect': 'True'}
    else:
        current_user.increment_incorrect()
        result = {'isAnswerCorrect': 'False'}
    return jsonify(result)

@app.route('/getRandomLetter', methods=['POST'])
def getRandomLetter():
    print('getting random letter')
    data_from_js = request.get_json()
    # Process data and return a response
    question_id = data_from_js.get('question_id')
    numbersArray = data_from_js.get('numbersArray')
    question = get_question(question_id=question_id)
    print(question_id,numbersArray)
    not_returned_yet = [i for i in range(len(question.answer)) if i not in numbersArray]
    random_idx = random.choice(not_returned_yet)
    result = {'letter':question.answer[random_idx],'letterIndex':random_idx}
    return jsonify(result)

@cache.memoize(timeout=120)
def get_question(question_id):
    question = Question().get_question(question_id=question_id)
    return question

    
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri="https://genelkultur.azurewebsites.net/login/callback", # request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    print(f'Got the code ')
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url.replace('http:','https:'),
        redirect_url=request.base_url.replace('http:','https:'),
        code=code
    )
    print(f'redirect uri {request.base_url}')
    print('Created token request code')
    print(f'token_url:{token_url}')
    print(f'headers:{headers}')
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    print('Got the response')

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    print('Got the user info')
    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    print('Started creating the db entry')
    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
    # app.run(ssl_context="adhoc")
