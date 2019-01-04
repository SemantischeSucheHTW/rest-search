from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

index_title = {}
index_location = {}
index_time = {}
index_text = {}


@app.route('/search', methods=['GET'])
def search():
    args = request.args.to_dict()
    print(args)

    title_args = args.pop('title', None)
    if title_args is not None:
        pass

    location_args = args.pop('location', None)
    if location_args is not None:
        pass

    from_args = args.pop('from', None)
    if from_args is not None:
        pass

    to_args = args.pop('to', None)
    if to_args is not None:
        pass

    text_args = args.pop('text', None)
    if text_args is not None:
        pass

    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
