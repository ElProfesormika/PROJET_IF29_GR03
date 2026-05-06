from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://localhost:27017/")
db = client.database_local

cursor = db.users_aggregated.find({}, {"_id": 0})
df = pd.DataFrame(list(cursor))

df.to_csv("users_aggregated.csv", index=False)
