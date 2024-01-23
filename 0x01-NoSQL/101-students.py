#!/usr/bin/ env python3
"""Python function that returns all students
sorted by average score
"""

from pymongo import MongoClient

def top_students(mongo_collection):
    """Return all students sorted by average score."""
    students = mongo_collection.aggregate([
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "scores": 1,
                "averageScore": {
                    "$avg": "$scores.score"
                }
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ])

    return students
