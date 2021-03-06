import pymongo
from bson import json_util
from flask import Flask,jsonify,render_template,request
#from flask_pymongo import PyMongo

app = Flask(__name__)


client = pymongo.MongoClient("mongodb://admin:EPQcnb07382@node9140-advweb-02.app.ruk-com.cloud:11167")

db = client["stock"]


@app.route("/")
def index():
    texts = "Hello World , Welcome to MongoDB"   
    return texts 


@app.route("/product", methods=['GET']) 
def get_allproduct(): 
    char = db.product 
    output = char.find()  
    return json_util.dumps(output) 


@app.route("/product/<name>", methods=['GET']) 
def get_oneproduct(name):
    char = db.product 
    output = char.find_one({'Name' : name}) 
    
    return json_util.dumps(output) 



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


@app.route('/product/<name>', methods=['DELETE'])
def delete_product(name):
    char = db.product 
    x = char.find_one({'Name' : name})  

    char_id = char.delete_one(x) 

    output = "Deleted complete" 

    return jsonify(output) 

@app.route("/details", methods=['GET'])
def get_Join():
    pro = db.product
    pipel = pro.aggregate( [     
            {
                '$lookup':  {
                        'from' : 'detail',
                        'localField': 'id_detail',
                        'foreignField':'id_detail' ,
                        'as': 'Join'
                }
            }   
        ]  
    )  
    return json_util.dumps(pipel)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 5000)