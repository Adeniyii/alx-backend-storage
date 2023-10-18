#!/usr/bin/env python3
"""10-update_topics defines a function `update_topics` which updates a record's topics."""


def update_topics(mongo_collection, name, topics):
    """updates all records matching `name` with new topics."""
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
