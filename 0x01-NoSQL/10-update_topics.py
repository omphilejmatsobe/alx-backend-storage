#!/usr/bin/env python3
"""
Changes topic on documents
"""

def update_topics(mongo_collection, name, topics):
    """
    changes topics on documents
    """

    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
