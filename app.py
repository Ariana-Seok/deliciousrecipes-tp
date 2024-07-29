from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://christ:mozart007@localhost/proyecto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contrasenia = db.Column(db.String(120), nullable=False)

# Modelo Comentario2
class Comentario2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    comentario = db.Column(db.Text, nullable=False)

    # Relacion con el modelo Usuario
    usuario = db.relationship('Usuario', backref=db.backref('comentarios2', lazy=True))

@app.route('/iniciar_sesion', methods=['GET'])
def iniciar_sesion():
    correo = request.args.get('correo')
    contrasenia = request.args.get('contrasenia')

    print(f"Correo recibido: {correo}")
    print(f"Contraseña recibida: {contrasenia}")

    if not correo or not contrasenia:
        return jsonify({'error': 'Correo y contraseña son requeridos'}), 400

    usuario = Usuario.query.filter_by(correo=correo,contrasenia=contrasenia).first()
    
    if usuario:
        return jsonify({'message': 'Inicio de sesión exitoso'}), 200
    else:
        return jsonify({'error': 'Correo o contraseña incorrectos'}), 401

    '''
    #NO USAR
    if usuario:
        print(f"Contraseña almacenada (hasheada): {usuario.contrasenia}")
        if check_password_hash(usuario.contrasenia, contrasenia):
        
            return jsonify({'message': 'Inicio de sesión exitoso'}), 200
        else:
            return jsonify({'error': 'Correo o contraseña incorrectos'}), 401
    else:
        return jsonify({'error': 'Correo o contraseña incorrectos'}), 401
    '''
'''

'''
@app.route('/eliminar_usuario', methods=['DELETE'])
def eliminar_usuario():
    correo = request.args.get('correo')
    contrasenia = request.args.get('contrasenia')

    print(f"Correo recibido: {correo}")
    print(f"Contraseña recibida: {contrasenia}")

    if not correo or not contrasenia:
        return jsonify({"error": "Campos de correo o contraseña faltantes."}), 400

    # Busca al usuario en la base de datos
    user = Usuario.query.filter_by(correo=correo).first()
    
    if user:
        if user.contrasenia == contrasenia:
            db.session.delete(user)
            db.session.commit()
            print(f"Usuario con correo {correo} eliminado.")
            return jsonify({"message": "Usuario eliminado con éxito."}), 200
        else:
            return jsonify({"error": "Contraseña incorrecta."}), 401
    else:
        return jsonify({"error": "Usuario no encontrado."}), 404



@app.route('/editar_usuario', methods=['PATCH'])
def editar_usuario():
    correo = request.args.get('correo')
    contrasenia_actual = request.args.get('contrasenia')
    contrasenia_nueva = request.args.get('contrasenia_nueva')

    print(f"Correo recibido: {correo}")
    print(f"Contraseña actual recibida: {contrasenia_actual}")
    print(f"Contraseña nueva recibida: {contrasenia_nueva}")

    # Verificar que los parámetros estén presentes
    if not correo or not contrasenia_actual or not contrasenia_nueva:
        return jsonify({"error": "Campos de correo, contraseña actual y nueva contraseña son requeridos."}), 400

    user = Usuario.query.filter_by(correo=correo).first()
    
    if user:
        if user.contrasenia == contrasenia_actual:
            user.contrasenia = contrasenia_nueva
            db.session.commit()
            print(f"Contraseña del usuario con correo {correo} actualizada.")
            return jsonify({"message": "Contraseña actualizada con éxito."}), 200
        else:
            return jsonify({"error": "Contraseña actual incorrecta."}), 401
    else:
        return jsonify({"error": "Usuario no encontrado."}), 404



@app.route('/comentarios2', methods=['POST'])
def agregar_comentario():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    mensaje = data.get('mensaje')
    
    if not nombre or not correo or not mensaje:
        return jsonify({'error': 'Faltan datos'}), 400

    nuevo_comentario = Comentario(nombre=nombre, correo=correo, mensaje=mensaje)
    db.session.add(nuevo_comentario)
    db.session.commit()
    
    return jsonify({'success': 'Comentario agregado'}), 200
'''
@app.route('/comentarios', methods=['POST'])
def agregar_comentario():
    correo = request.args.get('correo')
    mensaje = request.args.get('mensaje')
    
    if not correo or not mensaje:
        return jsonify({'error': 'Todos los campos son requeridos.'}), 400

    nuevo_comentario = Comentario(correo=correo, mensaje=mensaje)
    db.session.add(nuevo_comentario)
    db.session.commit()

    return jsonify({'message': 'Comentario enviado con éxito.'}), 200


'''
'''
cambiar metodos
cambiar jsonify y fail
js --> verificar que esten los tres parametros antes de hacer
'''

@app.route('/suscripcion_usuario', methods=['POST'])
def suscripcion_usuario():
    data = request.get_json()
    correo = data.get('correo')
    contrasenia = data.get('contrasenia')

    if not correo or not contrasenia:
        return jsonify({'error': 'Correo y contraseña son requeridos'}), 400

    usuario_existente = Usuario.query.filter_by(correo=correo).first()
    if usuario_existente:
        return jsonify({'error': 'El correo ya está registrado'}), 400

    nuevo_usuario = Usuario(correo=correo, contrasenia=contrasenia)
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al registrar el usuario: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)