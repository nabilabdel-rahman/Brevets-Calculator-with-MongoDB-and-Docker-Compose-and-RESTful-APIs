"""
Nose tests for flask_brevets.py

Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

import os
from pymongo import MongoClient

# Set up MongoDB connection
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

# Use database "brevets"
db = client.brevets

# Use collection "lists" in the databse
collection = db.lists

# from flask_brevets import submit_brevets, get_bevets
from flask_brevets_test import get_brevets, submit_brevets

def test_submit_data():
    _id = None

    date = "2023-11-17T12:34"
    brevet = 1000
    items = [{"km": 0, "open": "2023-11-17T12:34", "close": "2023-11-17T13:34"},
        {"km": 100, "open": "2023-11-17T15:34", "close": "2023-11-17T19:14"},
        {"km": 1000, "open": "2023-11-18T21:39", "close": "2023-11-20T15:34"}]

    _id = submit_brevets(date, brevet, items)

    assert _id != None
    # assert 0==0

def test_get_brevets():
    date = "2023-11-17T12:34"
    brevet = 1000
    items = [{"km": 0, "open": "2023-11-17T12:34", "close": "2023-11-17T13:34"},
        {"km": 100, "open": "2023-11-17T15:34", "close": "2023-11-17T19:14"},
        {"km": 1000, "open": "2023-11-18T21:39", "close": "2023-11-20T15:34"}]
    
    submit_brevets(date, brevet, items)

    fetched_date, fetched_brevet, fetched_items = get_brevets()
    
    assert date == fetched_date
    assert brevet == fetched_brevet
    assert items == fetched_items
    #assert 1==1