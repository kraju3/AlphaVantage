from pymongo import MongoClient,errors
import logging
import asyncio
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(asctime)s - %(funcName)s - %(message)s')

log = logging.getLogger('av')
class Database:
    def __init__(self,host,port):
        try:
            self.client = MongoClient(host,port)
            self.db = None

            log.info("Connection to the MongoClient Successful")
        except errors.ConnectionFailure:
            log.debug("Connection to MOngoClient Failed")

    def getDB(self,database):
        self.db = self.client[database]
        return self.db

    def insert(self,doc,db,collection):
        try:
            self.db = self.getDB(db)
            collection = self.db[collection]
            collection.insert_many(doc)
            log.info("Inserted to the {0} collection".format(collection))
        except errors.WriteConcernError:
            log.debug("ERROrInserting the Document to the collection")


