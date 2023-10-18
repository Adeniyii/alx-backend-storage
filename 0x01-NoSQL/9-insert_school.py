#!/usr/bin/env python3
"""9-insert_school defines a function `insert_school` which inserts
a new record into the school collection.
"""


def insert_school(mongo_collection, **kwargs):
    """insert kwargs into mongo_collection"""
    res = mongo_collection.insert_one(kwargs)
    return res.inserted_id
