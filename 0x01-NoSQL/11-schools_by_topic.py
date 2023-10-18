#!/usr/bin/env python3
"""11-schools_by_topic defines a function `schools_by_topic` which fetches all records
which have the given topic."""


def schools_by_topic(mongo_collection, topic):
    """fetch all records which contains the given topic."""
    res = mongo_collection.find({'topics': {'$all': [topic]}})
    return res
