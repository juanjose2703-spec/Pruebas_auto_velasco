from conexion import *
from autores import mis_autores

programa = Flask(__name__)
api = Api(programa)

class ListaAutores(Resource):
    def get(self):
        autores = mis_autores.listar()
        return jsonify({"mensaje": "autores", "data":autores})
    
    def post(self):
        nuevo = request.json
        resultado = mis_autores.consultar(nuevo["idAutor"])
        if len(resultado) == 0:
            mis_autores.agregar(nuevo["idAutor"], nuevo["nombre"])