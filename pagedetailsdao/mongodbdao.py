import datetime

from pymongo import MongoClient

from PageDetails import PageDetails
from pagedetailsdao.pagedetailsdao import PageDetailsDao


class MongoDBPageDetailsDao(PageDetailsDao):
    def __init__(self, config):
        conf_copy = dict(config)
        db = conf_copy.pop("db")
        pagedetails_collection_name = conf_copy.pop("pagedetails_collection")

        self.client = MongoClient(**conf_copy)
        self.db = self.client[db]
        self.pagedetails_collection = self.db[pagedetails_collection_name]

    def getPageDetails(self, url):
        doc = self.pagedetails_collection.find_one({"_id": url})

        return PageDetails(
            url=doc["url"],
            title=doc["title"],
            location=doc["location"],
            date=datetime.datetime.fromisoformat(doc["date"]),
            nr=doc["nr"],
            text=doc["text"]
        )
