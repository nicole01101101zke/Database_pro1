from pymongo import MongoClient

HOST = 'localhost'
PORT = 27017
DATABASE_NAME = 'diyiban'

class Mongo:

    def __init__(self, host=None, port=None, db_name=None):
        self.host = host or HOST or '127.0.0.1'
        self.port = port or PORT or '27017'
        self.db_name = db_name or DATABASE_NAME or 'diyiban'

    def connect(self):
        try:
            myclient = MongoClient(self.host, self.port)
            mydb = myclient[self.db_name]
            return mydb
        except Exception as e:
            print(e)
            return None
        else:
            return mydb


