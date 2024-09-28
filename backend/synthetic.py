from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from dotenv import load_dotenv
import os
load_dotenv()

client_token = os.getenv('client_token')
session = Session(server_token=client_token)
client = UberRidesClient(session)

response = client.get_price_estimates(
    start_latitude=37.770,
    start_longitude=-122.411,
    end_latitude=37.791,
    end_longitude=-122.405,
    seat_count=2
)

estimate = response.json.get('prices')

https://sandbox-login.uber.com/oauth/v2/authorize?client_id=VHEl92pE02m_Pg-CxxMm36YwhiKopdPV&response_type=code&redirect_uri=http://localhost:8000/callback