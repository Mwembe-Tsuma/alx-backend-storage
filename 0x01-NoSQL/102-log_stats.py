#!/usr/bin/env python3
""" 12. Log stats """


from pymongo import MongoClient


def log_stats():
    """ Print statistics about Nginx logs in MongoDB. """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    total_logs = logs_collection.count_documents({})
    print(f"{total_logs} logs")

    methods = {method: logs_collection.count_documents({"method": method})
               for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]}
    print("Methods:")
    for method, count in methods.items():
        print(f"\tmethod {method}: {count}")

    sts = logs_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{sts} status check")

    ip_counts = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    print("IPs:")
    for ip_count in ip_counts:
        print(f"\t{ip_count['_id']}: {ip_count['count']}")


if __name__ == "__main__":
    log_stats()
