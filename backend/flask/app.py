from flask import Flask, jsonify, request
from flask_cors import CORS
from map import generate_geoJSON
app = Flask(__name__)
CORS(app) 


# Allow CORS for communication with the Next.js app
# Example route to serve data
@app.route('/api', methods=['POST'])
def get_map():
    try:
        # Get the JSON data from the request
        data = request.json
        startCoords = data.get("start")
        destCoords = data.get("dest")
        start_lat = startCoords[1]
        start_lon = startCoords[0]
        end_lat = destCoords[1]
        end_lon = destCoords[0]
        geoJson = generate_geoJSON(start_lat, start_lon, end_lat, end_lon)
        return jsonify(geoJson), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
