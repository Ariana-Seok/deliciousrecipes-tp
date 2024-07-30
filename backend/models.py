from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key = True)
    usuario = db.Column(db.String(50), nullable = False)
    nombre = db.Column(db.String(50), nullable = False)
    apellido = db.Column(db.String(120), nullable = False)
    correo = db.Column(db.String(255), nullable = False)
    contrasenia = db.Column(db.String(16), nullable = False)
    recetas = db.relationship('Receta', backref = 'usuario')
    
class Categoria(db.Model):
    __tablename__ = 'categorias'
    id_categoria = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), nullable = False)
    subcategoria = db.relationship('Subcategoria', backref = 'categoria')
    
class Subcategoria(db.Model):
    __tablename__ = 'subcategorias'
    id_subcategoria = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), nullable = False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable = False)
    recetas = db.relationship('Receta', backref = 'subcategoria')

class RecetasIngredientes(db.Model):
    __tablename__ = 'recetas_ingredientes'
    id_receta = db.Column(db.Integer, db.ForeignKey('recetas.id_receta'), primary_key = True)
    id_ingrediente = db.Column(db.Integer, db.ForeignKey('ingredientes.id_ingrediente'), primary_key = True)
    cantidad = db.Column(db.String(10))
    unidad = db.Column(db.String(50))
    
    ingrediente = db.relationship('Ingrediente', backref = 'recetas_ingredientes')
    
class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    id_ingrediente = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    

class Receta(db.Model):
    __tablename__ = 'recetas'
    id_receta = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(70), nullable = False)
    descripcion = db.Column(db.Text, nullable = False)
    instrucciones = db.Column(db.Text, nullable = False)
    imagen_url = db.Column(db.String(300), nullable = False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable = False)
    id_subcategoria = db.Column(db.Integer, db.ForeignKey('subcategorias.id_subcategoria'), nullable = False)
    ingredientes = db.relationship('Ingrediente', secondary = 'recetas_ingredientes', backref = 'recetas')
    
    ingredientes = db.relationship('RecetasIngredientes', backref = 'receta')
    

