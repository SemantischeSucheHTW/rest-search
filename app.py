from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

import os
import logging

from indexdao.ortsIndexdao import OrtsIndexDao
from indexdao.zeitIndexdao import ZeitIndexDao
from indexdao.mongodbwortindexdao import MongoDBWortIndexDao
from pagedetailsdao.mongodbdao import MongoDBPageDetailsDao

# create logger
logger = logging.getLogger('rest-search')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('rest-search.log')
fh.setLevel(logging.ERROR)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

app = Flask(__name__)
CORS(app)

ortdao = None
zeitdao = None
pagedetailsdao = None
wortdao = None

@app.route('/reports', methods=['GET'])
def search():

    args = request.args.to_dict()
    logger.info("New Request with Arguments: " + str(args))

    '''
    title_args = args.pop('title', None)
    if title_args is not None:
        pass
    '''

    matched_location_urls = None
    matched_zeit_urls = None
    matched_wort_urls = None

    location_args = args.pop('locations', None)

    if location_args is not None:
        location_list = [word.strip() for word in location_args.split(' ')]
        for location in location_list:
            urls, weight = ortdao.getUrlfromKey(location)
            logger.info("Location URLs found: " + str(urls))
            matched_location_urls = set(urls)
            #for url in urls:
            #    matched_urls.add(url)
            #    logger.info("Append URL " + str(url) + " for Location " + location)

    from_args = args.pop('from', None)
    to_args = args.pop('to', None)

    if from_args is not None and to_args is not None:
        from_list = [word.strip() for word in from_args.split(',')]
        to_list = [word.strip() for word in to_args.split(',')]
        urls, weight = zeitdao.getUrlfromKey(from_list[0], to_list[0])
        logger.info("FROM_TO URLs found: " + str(urls))
        matched_zeit_urls = set(urls)
        #for url in urls:
        #    matched_urls.add(url)
        #    logger.info("Append URL " + str(urls) + " for FROM_TO " + from_list[0] + " - " + to_list[0])

    elif from_args is not None and to_args is None:
        from_list = [word.strip() for word in from_args.split(',')]
        for from_date in from_list:
            urls, weight = zeitdao.getUrlfromKey(from_date)
            logger.info("TO URLs found: " + str(urls))
            matched_zeit_urls = set(urls)
            #for url in urls:
            #    matched_urls.add(url)
            #    logger.info("Append URL " + str(url) + " for FROM " + from_date)

    word_args = args.pop('words', None)
    if word_args is not None:
        word_list = [word.strip() for word in word_args.split(' ')]
        for word in word_list:
            urls_counts = wortdao.getUrlsAndCountsfromKey(word)
            logger.info("word URLs found: " + str(urls_counts))
            matched_wort_urls = set([url for url, counts in urls_counts])
            #for url, ignored_count in urls_counts:
            #    matched_urls.add(url)
            #    logger.info("Append URL " + str(url) + " for word " + word)

    url_sets = [url_set for url_set in [
        matched_location_urls,
        matched_zeit_urls,
        matched_wort_urls
    ] if url_set != None]

    matched_urls = set()
    if len(url_set) > 2:
        matched_urls = url_sets[0]
        for url_set in url_sets[1:]:
            matched_urls = matched_urls.intersection(url_set)
    else if len(url_set) == 1:
        matched_urls = url_set[0]

    pagedetails_list = [pagedetailsdao.getPageDetails(url) for url in matched_urls]

    logger.info("Response " + str(pagedetails_list))

    # rdd_url_and_text = rdd_intersect.map(lambda x: (x, pagedetailsdao.getText(x)))

    return jsonify([{
        "link": pagedetails.url,
        "title": pagedetails.title,
        "text": pagedetails.text,
        "date": pagedetails.date,
        "nr": pagedetails.nr,
        "location": pagedetails.location,
    } for pagedetails in pagedetails_list])

def loadDaosWithDefaultConfig():
    ortsIndexdao = OrtsIndexDao({
        'host': "abteilung6.com",
        'port': 27017,
        'db': 'semantische',
        'ortsindex_collection': 'ortsindexe',
    })

    zeitIndexdao = ZeitIndexDao({
        'host': "abteilung6.com",
        'port': 27017,  # mongodb default port,
        'db': 'semantische',  # which database,
        'zeitindex_collection': 'zeitindexe'  # which collection,
    })

    pagedetailsdao = MongoDBTextDao({
        'host': "abteilung6.com",
        'port': 27017,  # mongodb default port,
        'db': 'semantische',  # which database,
        'pagedetails_collection': 'pagedetails'  # which collection,
    })

    wortdao = MongoDBPageDetailsDao({
        'host': "abteilung6.com",
        'port': 27017,  # mongodb default port,
        'db': 'semantische',  # which database,
        'wordindex_collection': 'pagedetails'  # which collection,
    })

if __name__ == '__main__':
    loadDaosWithDefaultConfig()
    app.run(host='0.0.0.0', port=5000)

