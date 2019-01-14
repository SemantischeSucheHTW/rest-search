from flask import Flask
from flask import jsonify
from flask import request
from pyspark import SparkConf, SparkContext
import os
import logging

from indexupdater.indexdao.ortsIndexdao import OrtsIndexDao
from indexupdater.indexdao.zeitIndexdao import ZeitIndexDao
from textprocessor.textdao.mongodbdao import MongoDBTextDao
from textprocessor.indexdao.mongodbwortindexdao import MongoDBWortIndexDao

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

config_textindex = {}
config_textindex['host'] = "abteilung6.com"
config_textindex['port'] = 27017  # mongodb default port
config_textindex['db'] = 'semantische'  # which database
config_textindex['pagedetails_collection'] = 'pagedetails'  # which collection

config_wortindex = {}
config_wortindex['host'] = "abteilung6.com"
config_wortindex['port'] = 27017  # mongodb default port
config_wortindex['db'] = 'semantische'  # which database
config_wortindex['wordindex_collection'] = 'wortindexe'  # which collection

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

ortdao = OrtsIndexDao(config_ortindex)
zeitdao = ZeitIndexDao(config_zeitindex)
textdao = MongoDBTextDao(config_textindex)
wortdao = MongoDBWortIndexDao(config_wortindex)

os.environ['HADOOP_HOME'] = "C:\\hadoop"

conf = (SparkConf()
        .setMaster("local")
        .setAppName("My app")
        .set("spark.executor.memory", "1g"))

sc = SparkContext(conf=conf)


@app.route('/reports', methods=['GET'])
def search():
    time_urls = []
    location_urls = []
    word_urls = []

    args = request.args.to_dict()
    logger.info("New Request with Arguments: " + str(args))

    '''
    title_args = args.pop('title', None)
    if title_args is not None:
        pass
    '''

    location_args = args.pop('locations', None)

    if location_args is not None:
        location_list = [word.strip() for word in location_args.split(',')]
        for location in location_list:
            urls, weight = ortdao.getUrlfromKey(location)
            logger.info("Location URLs found: " + str(urls))
            for url in urls:
                location_urls.append((url[0], url[0]))
                logger.info("Append URL " + str(url) + " for Location " + location)

    from_args = args.pop('from', None)
    to_args = args.pop('to', None)

    if from_args is not None and to_args is not None:
        from_list = [word.strip() for word in from_args.split(',')]
        to_list = [word.strip() for word in to_args.split(',')]
        urls, weight = zeitdao.getUrlfromKey(from_list[0], to_list[0])
        logger.info("FROM_TO URLs found: " + str(urls))
        for url in urls:
            logger.info("Append URL " + str(urls) + " for FROM_TO " + from_list[0] + " - " + to_list[0])
            time_urls.append((url[0], url[0]))

    elif from_args is not None and to_args is None:
        from_list = [word.strip() for word in from_args.split(',')]
        for from_date in from_list:
            urls, weight = zeitdao.getUrlfromKey(from_date)
            logger.info("TO URLs found: " + str(urls))
            for url in urls:
                logger.info("Append URL " + str(url) + " for FROM " + from_date)
                time_urls.append((url[0], url[0]))


    word_args = args.pop('words', None)
    if word_args is not None:
        word_list = [word.strip() for word in word_args.split(',')]
        for word in word_list:
            urls, weight = wortdao.getUrlsAndCountsfromKey(word)
            logger.info("word URLs found: " + str(urls))
            for url in urls:
                logger.info("Append URL " + str(url) + " for word " + word)
                word_urls.append((url[0], url[0]))


    rdd_locations = sc.parallelize(location_urls)
    rdd_time = sc.parallelize(time_urls)
    rdd_intersect = rdd_locations.intersection(rdd_time).collect()
    logger.info("Response " + str(rdd_intersect))

    return jsonify(rdd_intersect)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
