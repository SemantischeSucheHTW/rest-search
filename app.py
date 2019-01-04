from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

index_title = {}
index_location = {}
index_time = {}
index_text = {}


@app.route('/search', methods=['GET'])
def get_all_reports():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
