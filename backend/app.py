from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Usuario, Receta, Ingrediente, Subcategoria, Categoria, RecetasIngredientes
from flask_migrate import Migrate



app = Flask(__name__)
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost:5432/db_recetas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def home():
    return """
    <html>
        <body>
            <h1>API de Recetas</h1>
            <a href="/recetas">Ir a la pagina </a>
        </body>
    </html>
    """

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    try:
        data = request.get_json()
        nuevo_usuario = Usuario(
            usuario = data['usuario'],
            nombre = data['nombre'],
            apellido = data['apellido'],
            correo = data['correo'],
            contrasenia = data['contrasenia']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return {'mensaje': 'Usuario creado exitosamente'}, 201
    except Exception as error:
        return jsonify ({'error': str(error)}), 500
    
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        usuarios = Usuario.query.all()
        lista_usuarios = [
            {
                'id_usuario': usuario.id_usuario,
                'usuario': usuario.usuario,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'correo': usuario.correo
            }
            for usuario in usuarios
        ]
        return jsonify(lista_usuarios), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500
    

@app.route('/usuarios/<id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    try:
        usuario = Usuario.query.get(id_usuario)
        if usuario is None:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        usuario_data = {
                'id_usuario': usuario.id_usuario,
                'usuario': usuario.usuario,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'correo': usuario.correo
                }

        return jsonify(usuario_data), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500
    

@app.route('/recetas', methods = ['GET'])
def obtener_recetas():
    try:
        recetas = Receta.query.all()
        lista_recetas = [
            {
                'id_receta': receta.id_receta,
                'nombre': receta.nombre,
                'descripcion': receta.descripcion,
                'instrucciones': receta.instrucciones,
                'imagen_url': receta.imagen_url,
                'id_usuario': receta.id_usuario,
                'id_subcategoria': receta.id_subcategoria
            } for receta in recetas                            
        ]
        return jsonify(lista_recetas), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500
        
@app.route('/recetas', methods = ['POST'])
def crear_receta():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        instrucciones = data.get('instrucciones')
        imagen_url = data.get('imagen_url')
        id_usuario = int(data.get('id_usuario'))
        id_subcategoria = int(data.get('id_subcategoria'))
        ingredientes = data.get('ingredientes')

        subcategoria = Subcategoria.query.get(id_subcategoria)
        if not subcategoria:
            return jsonify({'error': 'Subcategoria no encontrada'}), 404
        
        

        nueva_receta = Receta(
            nombre = nombre,
            descripcion = descripcion,
            instrucciones = instrucciones,
            imagen_url = imagen_url,
            id_usuario = id_usuario,
            id_subcategoria = id_subcategoria
        )
        db.session.add(nueva_receta)
        
        db.session.flush() #Obtengo el ID de la receta ante del commit
        
        
        for ingrediente in ingredientes:
            nuevo_ingrediente = Ingrediente.query.filter_by(nombre = ingrediente.get('nombre')).first()
            if not nuevo_ingrediente:
                nuevo_ingrediente = Ingrediente(nombre = ingrediente.get('nombre'))
                db.session.add(nuevo_ingrediente)
                db.session.flush()
                
                
            receta_ingrediente = RecetasIngredientes(
                id_receta = nueva_receta.id_receta,
                id_ingrediente = nuevo_ingrediente.id_ingrediente,
                cantidad = ingrediente.get('cantidad'),
                unidad = ingrediente.get('unidad')
            )
            db.session.add(receta_ingrediente)
            
        db.session.commit()        
        return {'mensaje': 'Receta creada exitosamente'}, 201
    except Exception as error:
        return jsonify ({'error': str(error)}), 500
    
@app.route('/recetas/<id_receta>', methods= ['DELETE'])
def eliminar_receta(id_receta):
    try:
        #Elimino primero los ingredientes
        db.session.execute(
            'DELETE FROM ingredientes WHERE id_receta = :id_receta',
            {'id_receta': id_receta}
        )
        
        receta = Receta.query.get(id_receta)
        db.session.delete(receta)
        db.session.commit()
        return jsonify({'mensaje': 'Receta eliminada exitosamente'}), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500
    

@app.route('/recetas/<id_receta>', methods = ['PUT'])
def actualizar_receta(id_receta):
    try:
        data = request.get_json()
        receta = Receta.query.get(id_receta)
        
        receta.nombre = data.get('nombre', receta.nombre)
        receta.descripcion = data.get('descripcion', receta.descripcion)
        receta.instrucciones = data.get('instrucciones', receta.instrucciones)
        receta.imagen_url = data.get('imagen_url', receta.imagen_url)
        receta.id_usuario = data.get('id_usuario', receta.id_usuario)
        receta.id_subcategoria = data.get('id_subcategoria', receta.id_subcategoria)
        
        if 'ingrediente' in data:
            #Ingredientes existentes
            ingredientes_existentes = {ing.id_ingrediente for ing in receta.ingredientes}
        
            #creo un set para nuevos ingredientes
            ingredientes_nuevos = {ing['id_ingrediente'] for ing in data['ingredientes']}

            #Elimino ingredientes 
            ingredientes_a_eliminar = ingredientes_existentes - ingredientes_nuevos
            for id_ingrediente in ingredientes_a_eliminar:
                RecetasIngredientes.query.filter_by(id_receta = id_receta, id_ingrediente = id_ingrediente).delete()
            
            # Agregar nueva receta o actualizar
            for ing in data['ingredientes']:
                ingrediente = RecetasIngredientes.query.filter_by(id_receta = id_receta, id_ingrediente = ing['id_ingrediente']).first()
                
                if ingrediente:
                    #Actualizo
                    ingrediente.cantidad = ing.get('cantidad', ingrediente.cantidad)
                    ingrediente.unidad = ing.get('unidad', ingrediente.unidad)
                else:
                    # NUevo ingrediente
                    nuevo_ingrediente = RecetasIngredientes(
                        id_receta = id_receta,
                        id_ingrediente = ing['id_ingrediente'],
                        cantidad = ing.get('cantidad', ''),
                        unidad = ing.get('unidad', '')
                    )
        
                    db.session.add(nuevo_ingrediente)
        db.session.commit()
        
        return jsonify({'mensaje': 'Receta actualizada correctamente'}), 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500

@app.route('/recetas/<id_receta>')
def obtener_receta(id_receta):
    try:
        receta = Receta.query.get(id_receta)
        receta_data = {
            'id': receta.id_receta,
            'nombre': receta.nombre,
            'descripcion': receta.descripcion,
            'instrucciones': receta.instrucciones,
            'imagen_url': receta.imagen_url,
            'id_usuario': receta.id_usuario,
            'id_subcategoria': receta.id_subcategoria,
            'usuario': {
                'id_usuario': receta.usuario.id_usuario,
                'nombre': receta.usuario.nombre,
                'apellido': receta.usuario.apellido
            },
            'subcategoria': {
                'id_subcategoria': receta.subcategoria.id_subcategoria,
                'nombre': receta.subcategoria.nombre
            }, 
            'ingredientes': [
                {
                    'id_ingrediente': relacion.id_ingrediente,
                    'nombre': relacion.ingrediente.nombre,
                    'cantidad': relacion.cantidad if relacion.cantidad else ' ',
                    'unidad': relacion.unidad if relacion.unidad else ' '
                } for relacion in receta.ingredientes
            ]
        }
        
        return jsonify(receta_data), 200
    
    except Exception as error:
        return jsonify({'error': str(error)}), 500
    
    
@app.route('/recetas/<id_receta>')
def obtener_id_receta(id_receta):
    receta = Receta.query.get(id_receta)
    return jsonify({'id_receta': receta.id_receta})


@app.route('/recetas/<id_receta>/ingredientes', methods=['GET'])
def obtener_ingredientes_receta(id_receta):
    try:
        receta = Receta.query.get(id_receta)
        if not receta:
            return jsonify({'error': 'Receta no encontrada'}), 404
            
        ingredientes = db.session.execute(
            '''
            SELECT ingredientes.nombre, recetas_ingredientes.cantidad, recetas_ingredientes.unidad
            FROM recetas_ingredientes
            JOIN ingredientes ON recetas_ingredientes.id_ingrediente = ingredientes.id_ingrediente
            WHERE recetas_ingredientes.id_receta = :id_receta
            ''',
            {'id_receta': id_receta}
        ).fetchall()
        
        lista_ingredientes = [
            {'nombre': ing.nombre, 'cantidad': ing.cantidad, 'unidad': ing.unidad} 
            for ing in ingredientes
            ]
        
        return jsonify(lista_ingredientes), 200
    
    except Exception as error:
        return jsonify({'error': str(error)}), 500




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(host = '0.0.0.0', debug = True, port = port)