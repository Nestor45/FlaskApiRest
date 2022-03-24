from unittest import result
from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)

cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'system'

mysql = MySQL(app)

#Retornar todos los clientes
@app.route('/api/customers')
@cross_origin()
def getAllCustomers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, firstname, lastname, email, phone, address FROM `customers`;")
    datas = cur.fetchall() #OBTENERMOS TODOS LOS REGISTROS Y LOS ALMACENAMOS EN data
    result = []
    for data in datas:
        content = {'id':data[0], 'firstname':data[1], 'lastname':data[2], 'email':data[3], 'phone':data[4], 'address':data[5]}
        result.append(content)
    
    return jsonify(result) #DEVOLVEMOS EL RESULTADO EN FORMATO JSON


#Retornar un cliente
@app.route('/api/customers/<int:id>')
@cross_origin()
def getCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, firstname, lastname, email, phone, address FROM `customers` WHERE id = %s;", str(id))
    datas = cur.fetchall() #OBTENERMOS TODOS LOS REGISTROS Y LOS ALMACENAMOS EN data
    for data in datas:
        content = {'id':data[0], 'firstname':data[1], 'lastname':data[2], 'email':data[3], 'phone':data[4], 'address':data[5]}
    
    return jsonify(content) #DEVOLVEMOS EL RESULTADO EN FORMATO JSON

#Actualizar del cliente
@app.route('/api/customers', methods = ['PUT'])
@cross_origin()
def updateCustomer():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE `customers` SET `firstname` = %s, `lastname` = %s, `email` = %s, `phone` = %s, `address` = %s WHERE `customers`.`id` = %s", 
        (request.json['firstname'], request.json['lastname'], request.json['email'], request.json['phone'], request.json['address'], request.json['id']))
    mysql.connection.commit()
    return "ok update"


#Creacion del cliente
@app.route('/api/customers', methods = ['POST'])
@cross_origin()
def createCustomer():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `customers` (`id`, `firstname`, `lastname`, `email`, `phone`, `address`) VALUES (NULL, %s, %s, %s, %s, %s);",
        (request.json['firstname'],request.json['lastname'],request.json['email'],request.json['phone'],request.json['address']))
    mysql.connection.commit()
    return "ok save"


#Eliminacion de un cliente
@app.route('/api/customers/<int:id>', methods = ['DELETE'])
@cross_origin()
def removeCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM `customers` WHERE `customers`.`id` = %s", str(id))
    mysql.connection.commit()
    return "ok delete"


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host=HOST,port=PORT,debug=DEBUG)
