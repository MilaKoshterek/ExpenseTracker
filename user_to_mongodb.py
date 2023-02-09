import pymongo
import certifi
import pandas as pd


client = pymongo.MongoClient(
    "mongodb+srv://Alejandra:ZVMrff3p5nBaTgU@tracker.v3pj7t7.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where())
db = client["MoneyTracker"]
col = db["UserData"]
col_transactions = db["user_transactions"]

df_Joey = pd.read_csv("Joey.csv")
#print(df)
data_Joey = df_Joey.to_dict(orient="records")
#print(data)

user_id_Joey = '1a9c7d4d26f74afa8f19ee81f9d860d3'
user_joey = col_transactions.find_one({'_id': user_id_Joey})
user_joey['transactions'] = data_Joey
# col_transactions.update_one({'_id': user_id_Joey}, {'$set': user_joey})

df_Phoebe = pd.read_csv("Phoebe.csv")
# print(df_Phoebe)
data_Phoebe = df_Phoebe.to_dict(orient="records")
# print(data_Phoebe)
base_Phoebe_dict = {"_id": "0f713b53857241a5a273bc87ab665c21", "transactions":data_Phoebe}
print(base_Phoebe_dict)
# col_transactions.insert_one(base_Phoebe_dict)


df_Chandler = pd.read_csv("Chandler.csv")
data_Chandler = df_Chandler.to_dict(orient="records")
base_Chandler_dict = {"_id": "adeecd19663041b288dfad0dd859c7d3", "transactions": data_Chandler}
print(base_Chandler_dict)
# col_transactions.insert_one(base_Chandler_dict)



