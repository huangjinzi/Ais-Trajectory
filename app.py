from flask import Flask, jsonify
from flask_cors import CORS
from services import get_cleaned_ais_data

app = Flask(__name__)
CORS(app)

@app.route('/api/ais-data', methods=['GET'])
def ais_data():
    data = get_cleaned_ais_data()
    return data

if __name__ == '__main__':
    app.run(debug=True)
