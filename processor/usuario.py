from model.usuario import UsuarioModel
from reader.usuario import UsuarioReader
from app import db

class UsuarioProcessor:
    def insertar(self, usuario:UsuarioModel):    
        db.session.add(usuario)            

    def actualizar(self, args={}):
        id_usuario = args.get("id_usuario")
        usuario = UsuarioReader.get()

        if "codigo" in args:
            usuario.codigo = args.get("codigo")

        if "nombres" in args:
            usuario.nombres = args.get("nombres")
        
        if "apellidos" in args:
            usuario.apellidos = args.get("apellidos")

        if "id_cuenta_default" in args:
            usuario.id_cuenta_default = args.get("id_cuenta_default")
        

        
