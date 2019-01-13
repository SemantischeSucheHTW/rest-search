from flask import Flask
from flask import jsonify
from flask import request

from indexdao.ortsIndexdao import OrtsIndexDao
from indexdao.zeitIndexdao import ZeitIndexDao

config_ortindex = {}
config_ortindex['host'] = "abteilung6.com"
config_ortindex['port'] = 27017
config_ortindex['db'] = 'semantische'
config_ortindex['ortsindex_collection'] = 'ortsindexe'

config_zeitindex = {}
config_zeitindex['host'] = "abteilung6.com"
config_zeitindex['port'] = 27017  # mongodb default port
config_zeitindex['db'] = 'semantische'  # which database
config_zeitindex['zeitindex_collection'] = 'zeitindexe'  # which collection

app = Flask(__name__)

ortdao = None
zeitDao = None


@app.route('/search', methods=['GET'])
def search():
    args = request.args.to_dict()
    print(args)

    title_args = args.pop('title', None)
    if title_args is not None:
        pass

    location_args = args.pop('location', None)

    if location_args is not None:
        location_urls = []
        location_list = [word.strip() for word in location_args.split(',')]
        for location in location_list:
            urls, weight = ortdao.getUrlfromKey('Pankow')
            for url in urls:
                location_urls.append(url)
        return str(location_urls)

    from_args = args.pop('from', None)
    to_args = args.pop('to', None)

    if from_args is not None and to_args is not None:
        from_to_urls = []
        from_list = [word.strip() for word in from_args.split(',')]
        to_list = [word.strip() for word in to_args.split(',')]
        urls, weight = zeitdao.getUrlfromKey(from_list[0], to_list[0])
        for url in urls:
            from_to_urls.append(url)
        return str(from_to_urls)

    elif from_args is not None and to_args is None:
        from_urls = []
        from_list = [word.strip() for word in from_args.split(',')]

        for from_date in from_list:
            urls, weight = zeitdao.getUrlfromKey(from_date)
            for url in urls:
                from_urls.append(url)
        return str(from_urls)

    text_args = args.pop('text', None)
    if text_args is not None:
        pass

    return ""


if __name__ == '__main__':
    ortdao = OrtsIndexDao(config_ortindex)
    zeitdao = ZeitIndexDao(config_zeitindex)
    app.run(host='0.0.0.0', port=5000)
