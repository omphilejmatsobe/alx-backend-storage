#!/usr/bin/env python3
"""
inserts a document in a collection
"""

def insert_school(mongo_collection, **kwargs):
    """
    inserts a document in a collection
    """

    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id
