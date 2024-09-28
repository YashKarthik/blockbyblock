from flask import Flask, redirect, request, session, url_for
import requests
import os
from flask_cors import CORS
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import json

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
    return '<a href="/client">Connect client with Uber</a>'

@app.route('/client')
def client():
    # Define the token URL
    token_url = "https://sandbox-login.uber.com/oauth/v2/token"

    # Define the payload
    data = {
        'client_id': 'VHEl92pE02m_Pg-CxxMm36YwhiKopdPV',
        'client_secret': 'NOPPLy-6H2t50FvLGyuyA3xAi0g0fA-PTZAQ79Ao',
        'grant_type': 'client_credentials',
        'scope': 'support.3p.ticket.read support.3p.ticket.write'
    }

    # Make the POST request
    response = requests.post(token_url, data=data)
    # Parse and print the response
    token_data = response.json()
    print(token_data)
    session['access_token'] = token_data['access_token']
    return redirect(url_for('api'))
@app.route('/api')
def api():
    # uber_session = Session(server_token=session['access_token'])
    # client = UberRidesClient(uber_session)
    # response = client.get_products(37.77, -122.41)
    # products = response.json.get('products')
    # print(pr)
    # Define the API endpoint and parameters
    # url = "https://test-api.uber.com/v1.2/products"
    # headers = {
    #     "Authorization": f'Bearer {session["access_token"]}'# Replace <ACCESS_TOKEN> with your actual token
    # }

    # # Define the query parameters
    # params = {
    #     "latitude": 37.7759792,
    #     "longitude": -122.41823
    # }

    # # Make the GET request
    # response = requests.get(url, headers=headers, params=params)


    # Define the API endpoint
    # url = "https://api.uber.com/v1.2/requests/estimate"

    # # Define the headers, including the Authorization Bearer token
    # headers = {
    #     "Authorization": f'Bearer {session["access_token"]}',# Replace <ACCESS_TOKEN> with your actual token
    #     "Content-Type": "application/json"
    # }

    # # Define the data payload (request body)
    # data = {
    #     "product_id": "821415d8-3bd5-4e27-9604-194e4359a449",
    #     "start_latitude": "37.775232",
    #     "start_longitude": "-122.4197513",
    #     "end_latitude": "37.7899886",
    #     "end_longitude": "-122.4021253",
    #     "seat_count": "2",
    # }

    # # Make the POST request
    # response = requests.post(url, headers=headers, data=json.dumps(data))

    # print(response.text)
    # print(response.json())
    # Parse and print the response
    return(session['access_token'])

if __name__ == '__main__':
    app.run(debug=True)

