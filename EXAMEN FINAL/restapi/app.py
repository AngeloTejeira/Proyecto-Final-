from flask import Flask, request
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId


app = Flask(__name__)
CORS(app,resources={"*": {"origins": "*"}})
mongo = MongoClient("mongo",27017)

@app.route('/api',methods=['GET'])
def getAll():
  citas = list(mongo.db.citas.find())
  for i in range(len(citas)):
    citas[i]['_id'] = str(citas[i]['_id'])
  return {'citas':citas}

@app.route('/api', methods=['POST'])
def create():
  mongo.db.citas.insert_one({
    'paciente': request.json['paciente'],
    'descripcion':request.json['descripcion'], 
    'fecha': request.json['fecha']
  })
  return request.json

@app.route('/api/<id>', methods=['GET'])
def get(id):
  cita = mongo.db.citas.find_one({'_id':ObjectId(id)})
  if cita:
    cita['_id'] = str(cita['_id'])
    return cita
  return {'mensaje': 'La cita no está registrada!'}

@app.route('/api/<id>', methods=['PATCH'])
def update(id):
  print('OK')
  mongo.db.citas.update_one({'_id':ObjectId(id)},{
    '$set':{
      'paciente':request.json['paciente'],
      'descripcion':request.json['descripcion'],
      'fecha':request.json['fecha']
      }
    })
  return request.json

@app.route('/api/<id>', methods=['DELETE'])
def delete(id):
  mongo.db.citas.delete_one({'_id':ObjectId(id)})
  return{
    '_id': id
  }

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001, debug=True)