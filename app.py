from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from flask_cors import CORS
from config import config
from utils import enviar_email


app = Flask(__name__)

conexion = MySQL(app)

migrate = Migrate()
ma = Marshmallow()
cors = CORS()

ma.init_app(app)
cors.init_app(app)


@app.route('/api/barberos', methods=['GET'])
def listar_barberos():
    try:
        cursor = conexion.connection.cursor()

        query = 'SELECT id_barbero, nombre FROM barberos'
        cursor.execute(query)
        data = cursor.fetchall()
        barberos = [{'id': row[0], 'nombre':row[1]} for row in data]

        print(data)
        return jsonify({'barberos': barberos, 'mensaje': 'Barberos Listados'})

    except Exception as ex:
        return jsonify({'mensaje': 'Error'})


@app.route('/api/barberos', methods=['POST'])
def agregar_barbero():
    try:

        cursor = conexion.connection.cursor()
        nombre = request.json['nombre']

        query = """INSERT INTO barberos (nombre) VALUES('{0}')""".format(
            nombre)

        cursor.execute(query)

        conexion.connection.commit()

        return jsonify({'mensaje': 'Barbero agregado con exito'})

    except:
        return jsonify({'mensaje': 'Error'})


@app.route('/api/barberos/<id>', methods=['DELETE'])
def eliminar_barbero(id):
    try:

        cursor = conexion.connection.cursor()

        query = """DELETE FROM barberos WHERE id_barbero={0}""".format(id)

        cursor.execute(query)
        conexion.connection.commit()

        return jsonify({'mensaje': 'Barbero eliminado con exito'})

    except:
        return jsonify({'mensaje': 'Error'})


@app.route('/api/horas/<id>', methods=['PUT'])
def quitar_disponibilidad(id):
    try:
        cursor = conexion.connection.cursor()

        query = 'UPDATE horas SET disponible = false WHERE id_hora = {0}'.format(
            id)
        cursor.execute(query)
        conexion.connection.commit()

        return jsonify({'mensaje': 'Horas Agendada'})

    except Exception as ex:
        return {'mensaje': 'Error'}


@app.route('/api/horas', methods=['GET'])
def listar_horas_disponibles():
    try:
        cursor = conexion.connection.cursor()

        query = 'SELECT id_hora, dia, mes, hora_inicial, id_barbero, id_servicio FROM horas WHERE disponible = true'
        cursor.execute(query)
        data = cursor.fetchall()
        horas = [{'id_hora': row[0], 'dia':row[1], 'mes':row[2], 'hora_inicial':row[3],
                  'id_barbero':row[4], 'id_servicio':row[5]} for row in data]

        return jsonify({'horas': horas, 'mensaje': 'Horas Listadas'})

    except Exception as ex:
        return {'mensaje': 'Error'}


@app.route('/api/servicios', methods=['GET'])
def listar_servicios():
    try:
        cursor = conexion.connection.cursor()

        query = 'SELECT id_servicio, nombre, precio, duracion, descripcion FROM servicios'
        cursor.execute(query)
        data = cursor.fetchall()
        servicios = [{'id_servicio': row[0], 'nombre':row[1], 'precio':row[2], 'duracion':row[3],
                      'descripcion':row[4]} for row in data]

        return jsonify({'servicios': servicios, 'mensaje': 'Servicios Listadas'})

    except Exception as ex:
        return {'mensaje': 'Error'}


@app.route('/api/servicios', methods=['POST'])
def agregar_servicio():
    try:

        cursor = conexion.connection.cursor()
        nombre, precio, descripcion = request.json['nombre'], request.json['precio'], request.json['descripcion']

        query = """INSERT INTO servicios (nombre, precio, descripcion) VALUES('{0}', {1}, '{2}')""".format(
            nombre, precio, descripcion)

        cursor.execute(query)

        conexion.connection.commit()

        return jsonify({'mensaje': 'Servicio agregado con exito'})

    except:
        return jsonify({'mensaje': 'Error'})


@app.route('/api/servicios/<id>', methods=['DELETE'])
def eliminar_servicios(id):
    try:
        cursor = conexion.connection.cursor()

        query = """DELETE FROM servicios WHERE id_servicio={0}""".format(id)

        cursor.execute(query)
        conexion.connection.commit()

        return jsonify({'mensaje': 'Servicio eliminado con exito'})

    except:
        return jsonify({'mensaje': 'Error'})


@app.route('/api/reservas', methods=['GET'])
def listar_reservas():
    try:
        cursor = conexion.connection.cursor()

        query = '''SELECT reservas.nombre_cliente, reservas.telefono, horas.dia, horas.mes, horas.hora_inicial, horas.id_hora FROM reservas INNER JOIN horas ON horas.id_hora = reservas.id_hora'''
        cursor.execute(query)
        data = cursor.fetchall()
        reservas = [{'nombre_cliente': row[0], 'telefono':row[1], 'dia':row[2], 'mes':row[3],
                     'hora_inicial':row[4], 'id_hora':row[5]} for row in data]

        return jsonify({'reservas': reservas, 'mensaje': 'reservas Listadas'})

    except Exception as ex:
        return {'mensaje': 'Error'}


@app.route('/api/reservas', methods=['POST'])
def agregar_reserva():
    try:

        cursor = conexion.connection.cursor()
        nombre, apellido, correo, telefono, comentarios, id_hora = request.json[
            'nombre'], request.json['apellido'], request.json['correo'], request.json['telefono'], request.json['comentarios'], int(request.json['id_hora'])

        query = """INSERT INTO reservas (nombre, apellido, correo, telefono, comentarios, id_hora) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', {5})""".format(
            nombre, apellido, correo, telefono, comentarios, id_hora)

        cursor.execute(query)

        query = f'''select dia, mes, hora_inicial from horas where id_hora={id_hora}'''
        cursor.execute(query)

        data = cursor.fetchall()

        hora_ = [{'dia': row[0], 'mes':row[1], 'hora':row[2]} for row in data]

        dia, mes, hora = hora_[0]["dia"], hora_[0]["mes"], hora_[0]["hora"]

        print(dia, mes, hora)

        enviar_email(nombre, apellido, correo, dia, mes, hora)
        conexion.connection.commit()

        return jsonify({'mensaje': 'Reserva agregado con exito'})

    except:
        return jsonify({'mensaje': 'Error'})


if __name__ == "__main__":
    app.config.from_object(config['development'])

    app.run()
