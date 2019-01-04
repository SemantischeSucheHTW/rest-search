from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def get_all_reports():
    filter_params = {}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
