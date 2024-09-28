from flask import Flask, redirect, request, session, url_for
import requests
import os
from flask_cors import CORS
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a random secret key for session management

# Uber OAuth 2.0 credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:5000/callback'  # This must match what you set in Uber Developer Dashboard
# UBER_AUTH_URL = 'https://login.uber.com/oauth/v2/authorize'
UBER_AUTH_URL = 'https://sandbox-login.uber.com/oauth/v2/authorize'
# UBER_TOKEN_URL = 'https://login.uber.com/oauth/v2/token'
UBER_TOKEN_URL = 'https://sandbox-login.uber.com/oauth/v2/token'

# Scopes determine the permissions your app will request
SCOPES = 'profile history ride_widgets'

CORS(app)

@app.route('/')
def index():
    return '<a href="/login">Log in with Uber</a>'

@app.route('/login')
def login():
    # Step 1: Redirect user to Uber's OAuth authorization page
    uber_authorize_url = f"{UBER_AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
    print(uber_authorize_url)
    return redirect(uber_authorize_url)

@app.route('/callback')
def callback():
    # Step 2: Handle Uber's authorization code redirect
    code = request.args.get('code')

    # Step 3: Exchange the authorization code for an access token
    token_response = requests.post(UBER_TOKEN_URL, data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': code
    })

    token_data = token_response.json()
    access_token = token_data['access_token']

    # Step 4: Store access token in session and redirect to profile page
    # print(access_token)
    session['access_token'] = access_token
    print(session['access_token'])
    print(token_data["scope"])
    return redirect(url_for('test'))


@app.route('/test')
def test():
    url = "https://test-api.uber.com/v1.2/products"

# Define the access token
    # access_token = session['access_token']

    # # Define the parameters (latitude and longitude)
    # params = {
    #     'latitude': 37.7759792,
    #     'longitude': -122.41823
    # }

    # # Define the headers, including the authorization
    # headers = {
    #     'Authorization': f'Bearer {access_token}'
    # }

    # # Make the GET request to the Uber API
    # response = requests.get(url, headers=headers, params=params)

    # # Parse the response JSON
    # data = response.json()
    # return data
    return session['access_token']

@app.route('/price')
def price():
    uber_session = Session(server_token=session['access_token'])
    client = UberRidesClient(uber_session)
    response = client.get_price_estimates(
    start_latitude=37.770,
    start_longitude=-122.411,
    end_latitude=37.791,
    end_longitude=-122.405,
    seat_count=2
    )

    estimate = response.json.get('prices')
    return estimate

# @app.route('/profile')
# def profile():
#     # Step 5: Use the access token to fetch user profile from Uber API
#     access_token = session.get('access_token')

#     if not access_token:
#         return redirect(url_for('login'))

#     response = requests.get('https://api.uber.com/v1.2/me', headers={
#         'Authorization': f'Bearer {access_token}'
#     })

#     profile_data = response.json()
#     return f"<h1>Welcome, {profile_data['first_name']}!</h1><pre>{profile_data}</pre>"

if __name__ == '__main__':
    app.run(debug=True)

