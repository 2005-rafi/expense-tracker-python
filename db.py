# db.py

import logging
from pymongo import MongoClient
import pymongo
from datetime import datetime

logger = logging.getLogger(__name__)

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "expense_tracker"
MONGO_COLLECTION = "expenses"

# Connect to MongoDB
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    logger.info("Connected to MongoDB successfully")
except pymongo.errors.ConnectionFailure as e:
    logger.error(f"Could not connect to MongoDB: {e}")
    mongo_client = None

# --- In-Memory Fallback Database (For No-Mongo Environments) ---
class InMemoryDB:
    def __init__(self):
        self.expenses = []
        self.counter = 0

    def insert_one(self, data):
        self.counter += 1
        data['_id'] = str(self.counter)
        self.expenses.append(data)
        return type('obj', (object,), {'inserted_id': data['_id']})

    def find(self, query=None, projection=None):
        return self.expenses

    def aggregate(self, pipeline):
        if pipeline and pipeline[0].get('$group'):
            total = sum(expense['amount'] for expense in self.expenses)
            return [{"_id": None, "total": total}]
        return []

    def delete_many(self, query=None):
        self.expenses = []

    def delete_one(self, query):
        _id = query.get("_id")
        if _id:
            initial_len = len(self.expenses)
            self.expenses = [exp for exp in self.expenses if str(exp['_id']) != str(_id)]
            deleted_count = 1 if len(self.expenses) < initial_len else 0
            return type('obj', (object,), {'deleted_count': deleted_count})
        return type('obj', (object,), {'deleted_count': 0})

    def update_one(self, query, update_data):
        # Optional: future support
        return type('obj', (object,), {'matched_count': 0, 'modified_count': 0})

# --- Fallback to In-Memory ---
if not mongo_client:
    logger.warning("MongoDB not available. Using in-memory database.")
    collection = InMemoryDB()
