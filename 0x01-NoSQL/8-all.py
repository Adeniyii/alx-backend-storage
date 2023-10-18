#!/usr/bin/env python3
"""8-all defines a function `list_all` which lists all records in a given collection"""


def list_all(mongo_collection):
    """fetch all records in mongo_collection."""
    out = []

    for doc in mongo_collection.find():
        out.append(doc)

    return out
