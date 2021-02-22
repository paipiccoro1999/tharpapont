import pymongo
from bson import json_util
from flask import Flask,jsonify,render_template,request
#from flask_pymongo import PyMongo

app = Flask(__name__)


client = pymongo.MongoClient("mongodb://admin:EPQcnb07382@10.100.2.117:27017")

db = client["stock"]


####### index ###############
@app.route("/")
def index():
    texts = "Hello World , Welcome to MongoDB"
    return texts

########## GET ALL #################
@app.route("/product", methods=['GET'])
def get_allproduct():
    char = db.product
    output = char.find()
    return json_util.dumps(output)

# ############## GET ONE ############################
@app.route("/product/<name>", methods=['GET'])
def get_oneproduct(name):
    char = db.product
    output = char.find_one({'Name' : name})
    
    return json_util.dumps(output)


# ######################### INSERT ####################
@app.route('/product', methods=['POST'])
def add_product():
  char = db.product
  name = request.json['Name']
  price = request.json['price']
  color = request.json['color']
  
  char_id = char.insert({'Name': name, 'price': price,
                        'color': color})
  new_char = char.find_one({'_id': char_id })
  output = {'Name' : new_char['Name'], 'price' : new_char['price'],
                        'color' : new_char['color']}
  return jsonify(output)

# ##################### UPDATE ########################
@app.route('/product/<name>', methods=['PUT'])
def update_product(name):
    char = db.product
    x = char.find_one({'Name' : name})
    if x:
        myquery = {'Name' : x['Name'],'price' : x['price'],
                        'color' : x['color']
                       }

    name = request.json['Name']
    price = request.json['price']
    color = request.json['color']

    
    newvalues = {"$set" : {'Name' : name, 'price' : price,
                        'color' : color
                        }}

    char_id = char.update_one(myquery, newvalues)

    output = {'Name' : name, 'price' : price,
                        'color' : color
                        }

    return jsonify(output)

# ##################### DELETE ############################ 
@app.route('/product/<name>', methods=['DELETE'])
def delete_product(name):
    char = db.product
    x = char.find_one({'Name' : name})

    char_id = char.delete_one(x)

    output = "Deleted complete"

    return jsonify(output)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 80)