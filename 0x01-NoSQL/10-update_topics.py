#!/usr/bin/env python3
"""Change school topics"""


def update_topics(mongo_collection, name, topics):
    """Update topics of a school document based on the name."""
    result = mongo_coll.updates({"name": name}, {"$set": {"topics": topics}})
    return result.modified_count
