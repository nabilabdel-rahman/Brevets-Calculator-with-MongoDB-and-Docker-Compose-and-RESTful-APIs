"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import os
import logging

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

from pymongo import MongoClient

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()


# Set up MongoDB connection
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

# Use database "brevets"
db = client.brevets

# Use collection "lists" in the databse
collection = db.lists

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


def get_brevets():
    """
    Obtains the newest document in the "lists" collection in database "todo".

    Returns title (string) and items (list of dictionaries) as a tuple.
    """
    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.

    lists = collection.find().sort("_id", -1).limit(1)

    # lists is a PyMongo cursor, which acts like a pointer.
    # We need to iterate through it, even if we know it has only one entry:
    for todo_list in lists:
        # We store all of our lists as documents with two fields:
        ## title: string # title of our to-do list
        ## items: list   # list of items:

        ### every item has three fields:
        #### date: string   # date
        #### brevet: int  #brevet
        #### items: list  #km, open, and close
        return todo_list["date"], todo_list["brevet"], todo_list["items"]


def submit_brevets(date, brevet, items):
    """
    Inserts a new to-do list into the database "todo", under the collection "lists".
    
    Inputs a title (string) and items (list of dictionaries)

    Returns the unique ID assigned to the document by mongo (primary key.)
    """
    output = collection.insert_one({
        "date": date,
        "brevet": brevet,
        "items": items})
    _id = output.inserted_id # this is how you obtain the primary key (_id) mongo assigns to your inserted document.
    return str(_id)


@app.route("/submit", methods=["POST"])
def insert():
    """
    /submit : inserts brevets into the database.

    Accepts POST requests ONLY!

    JSON interface: gets JSON, responds with JSON
    """
    try:
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!
        
        # Because input_json is a dictionary, we can do this:
        date = input_json["date"] # Should be a string
        brevet = input_json["brevet"]
        items = input_json["items"] # Should be a list of dictionaries

        brevets_id = submit_brevets(date, brevet, items)

        return flask.jsonify(result={},
                        message="Inserted!", 
                        status=1, # This is defined by you. You just read this value in your javascript.
                        mongo_id=brevets_id)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                        message="Oh no! Server error!", 
                        status=0, 
                        mongo_id='None')


@app.route("/display")
def display():
    """
    /fetch : fetches the newest brevet from the database.

    Accepts GET requests ONLY!

    JSON interface: gets JSON, responds with JSON
    """
    try:
        date, brevet, items = get_brevets()
        return flask.jsonify(
                result={"date": date, "brevet": brevet, "items": items}, 
                status=1,
                message="Successfully displayed brevets!")
    except:
        return flask.jsonify(
                result={}, 
                status=0,
                message="Something went wrong, couldn't display any brevets!")


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!

    brevet = request.args.get('brevet', type=float)
    date = request.args.get('date', type=str)
    begin = arrow.get(date, 'YYYY-MM-DDTHH:mm')
    
    open_time = acp_times.open_time(km, brevet, begin).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet, begin).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
