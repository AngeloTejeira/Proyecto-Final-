from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API = 'http://restapi:5001/api' 

@app.route('/',methods=['GET','POST'])
def index():
  data = {}
  if request.method == 'POST':
    requests.post(
      API,
      json={
        'descripcion': request.form['descripcion'],
        'paciente': request.form['paciente'],
        'fecha': request.form['fecha']
      })
    data['mensaje'] = "Cita ingresada"
  data['citas'] = obtenerCitas()
  return render_template('index.html',data=data)

@app.route('/eliminar/<id>',methods=['GET'])
def eliminar(id):
  requests.delete(f'{API}/{id}')
  data = {'mensaje': 'Cita eliminada'}
  data['citas'] = obtenerCitas()
  return render_template('index.html',data=data)

@app.route('/editar/<id>', methods=['GET'])
def editar(id):
  res = requests.get(f'{API}/{id}').json()
  data = {'cita':res}
  
  data['citas'] = obtenerCitas()
  return render_template('index.html',data=data)

@app.route('/editar/<id>', methods=['POST'])
def editar2(id):
  requests.patch(
    f'{API}/{id}',
    json={
      'descripcion': request.form['descripcion'],
      'paciente': request.form['paciente'],
      'fecha': request.form['fecha'],
    })
  data = {'mensaje':'Cita editada'}
  data['citas'] = obtenerCitas()
  return render_template('index.html',data=data)

def obtenerCitas():
  res = requests.get(API).json()
  return res['citas']

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=5000,debug=True)
