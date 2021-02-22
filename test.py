import pymongo

myclient = pymongo.MongoClient("mongodb://admin:EPQcnb07382@node9140-advweb-02.app.ruk-com.cloud:11167")
mydb = myclient["stock"]
mycol = mydb["product"]

for x in mycol.find():
  print(x)