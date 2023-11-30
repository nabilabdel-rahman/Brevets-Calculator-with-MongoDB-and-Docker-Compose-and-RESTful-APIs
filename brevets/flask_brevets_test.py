from pymongo import MongoClient
import os
# Set up MongoDB connection
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

# Use database "brevets"
db = client.brevets

# Use collection "lists" in the databse
collection = db.lists


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