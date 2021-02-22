import pymongo
from bson import json_util
from flask import Flask,jsonify,render_template,request
#from flask_pymongo import PyMongo

app = Flask(__name__)


client = pymongo.MongoClient("mongodb://admin:EPQcnb07382@10.100.2.117:27017")#ประกาศตัวแปลโดยมีการเชื่อมต่อกับ mongo ที่ต้องมี user และ password

db = client["stock"]


################## เป็นฟังชั่นสำหรับหน้า index ##################
@app.route("/")
def index():
    texts = "Hello World , Welcome to MongoDB"   #ตัวแปลที่เก็บค่า string
    return texts # retrun ค่า texts กลับไปรายงาน 

################## เป็นการทำงานในส่วนของการรายงาน product ทั้งหมด ##################
@app.route("/product", methods=['GET']) # ทำการเอาข้อมูลในตารางผ่าน methods GET
def get_allproduct(): 
    char = db.product #ประกาศตัวแปล char ไว้สำหรับตาราง product
    output = char.find() #ตัวแปล output 
    return json_util.dumps(output) # return ค่า output กลับไปแสดง

################## การทำงานในการรายงาน product อย่างใดอย่างนึงกลับไป ##################
@app.route("/product/<name>", methods=['GET']) # ทำการเอาข้อมูลในตาราง product และชื่อที่ตรงกันในตารางผ่าน methods GET
def get_oneproduct(name):
    char = db.product #ประกาศตัวแปล char ไว้สำหรับตาราง product
    output = char.find_one({'Name' : name}) #ตัวแปล output ที่มีค่าจากตารางตรงกัน
    
    return json_util.dumps(output) #return ค่า output กลับไปแสดง


################## การทำงานในการเพิ่มข้อมูลเข้าไปใน DB ##################
@app.route('/product', methods=['POST'])
def add_product():
  char = db.product #ประกาศตัวแปล char ไว้สำหรับตาราง product
  name = request.json['Name'] # ตัวแปล name  เพื่อเอาไว้เก็บค่าชื่อ 
  price = request.json['price'] # ตัวแปล price เพื่อเอาไว้เก็บค่าราคา
  color = request.json['color'] # ตัวแปล color เพื่อเอาไว้เก็บค่าสี
  
  char_id = char.insert({'Name': name, 'price': price,
                        'color': color})
  new_char = char.find_one({'_id': char_id })
  output = {'Name' : new_char['Name'], 'price' : new_char['price'],
                        'color' : new_char['color']}
  return jsonify(output) #ตัวแปล output ที่มีค่าจากตารางตรงกัน
    

################## การทำงานในการแก้ไขข้อมูลของสินค้าใน DB ##################
@app.route('/product/<name>', methods=['PUT'])
def update_product(name):
    char = db.product#ประกาศตัวแปล char ไว้สำหรับตาราง product
    x = char.find_one({'Name' : name}) # ตัวแปล x เพื่อไว้เก็บค่าของสินค้าที่จะแก้ไข
    if x:                                                         # เช็คว่า x มีชื่อที่ตรงกับตารางไหม
        myquery = {'Name' : x['Name'],'price' : x['price'],
                        'color' : x['color']
                       }

    name = request.json['Name']       #
    price = request.json['price']     #   สร้างตัวแปลที่มีข้อมูลข้างในของตาราง
    color = request.json['color']     #

    
    newvalues = {"$set" : {'Name' : name, 'price' : price, #
                        'color' : color                    #   set ข้อมูลใหม่ลงในตาราง
                        }}                                 #

    char_id = char.update_one(myquery, newvalues) # id ที่รับค่า ของ  myquery และ newvalues

    output = {'Name' : name, 'price' : price,  
                        'color' : color        #ตัวแปล output ที่มีค่าจากตาราง
                        }

    return jsonify(output) # return ค่า output


################## การทำงานมนการลบข้อมูล ในตาราง DB ##################
@app.route('/product/<name>', methods=['DELETE'])
def delete_product(name):
    char = db.product #ประกาศตัวแปล char ไว้สำหรับตาราง product
    x = char.find_one({'Name' : name})  #ตัวแปล x ที่มีค่าจาก หัวตาราง เหมือนกัน

    char_id = char.delete_one(x) #ลบ id ของสินค้าในตารางที่มีชื่อตรงกัน

    output = "Deleted complete" #โชว์ว่าลบสำเร็จ

    return jsonify(output) # return ค่า output


if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 80)