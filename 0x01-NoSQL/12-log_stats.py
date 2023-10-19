#!/usr/bin/env python3
"""Module 12-log_stats provides some stats about Nginx logs."""
from pymongo import MongoClient


def process_logs(mongo_collection):
    """provides some stats about Nginx logs"""
    print("{} logs".format(mongo_collection.count_documents({})))
    print("Methods")

    methods = {"GET": 0, "POST": 0, "PUT": 0, "PATCH": 0, "DELETE": 0}
    agg = mongo_collection.aggregate([{'$group': {'_id': '$method', 'count': {'$sum': 1}}}])

    for doc in agg:
        if doc['_id'] in methods.keys():
            methods[doc['_id']] = doc['count']
    for k, v in methods.items():
        print("\tmethod {}: {}".format(k, v))

    print("{} status check".format(mongo_collection.count_documents({'method': 'GET', 'path': '/status'})))


if __name__ == "__main__":
    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx_collection = client.logs.nginx
    process_logs(nginx_collection)
