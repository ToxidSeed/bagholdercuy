from model.usuario import UsuarioModel

class Auth:
    def get_usuario(usuario_id):        
        return UsuarioModel.get(usuario_id)
