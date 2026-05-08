from conexion import *
import pytest

class Test_editoriales:

    def setup_class(self):
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5083/editoriales"
        # Limpiar por si quedaron datos de corridas anteriores
        mi_cursor.execute(f"DELETE FROM editoriales WHERE idEditorial IN ('ed001','ed002')")
        mi_cursor.execute(f"DELETE FROM paises WHERE idPais='ES'")
        mi_db.commit()
        # Insertar pais propio para las pruebas de editoriales
        mi_cursor.execute(f"INSERT INTO paises (idPais,nombre,continente) VALUES ('ES','España','Europa')")
        mi_db.commit()
        id = "ed001"
        nombre = "Planeta Editorial"
        idPais = "ES"
        sql = f"INSERT INTO editoriales (idEditorial,nombre,idPais) VALUES ('{id}','{nombre}','{idPais}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        # Limpia la base de datos
        mi_cursor.execute(f"DELETE FROM editoriales WHERE idEditorial IN ('ed001','ed002')")
        mi_cursor.execute(f"DELETE FROM paises WHERE idPais='ES'")
        mi_db.commit()

    def test_lista_editoriales(self):
        esperado = "editoriales"
        # Ejecutar la prueba
        calculado = requests.get(self.url)
        # Verificación
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"]==esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada","esperado_entrada"],
        [({"idEditorial":"ed002", "nombre":"Norma Editorial","idPais":"ES"},"Editorial agregada con éxito"),
         ({"idEditorial":"ed001", "nombre":"Planeta Editorial","idPais":"ES"},"Id de editorial ya existe")]
    )
    def test_agregar(self,nuevo_entrada,esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.post(self.url,json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("ed001","Editorial encontrada"),
         ("ed099","Editorial no encontrada")]
    )
    def test_busqueda(self,id_entrada,esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.get(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    # Para cuando la editorial existe y se modifica con éxito
    def test_modifica1(self):
        id = "ed001"
        nombre = "Planeta Editorial Modificada"
        idPais = "ES"
        nuevo = {"idEditorial":id, "nombre":nombre, "idPais":idPais}
        esperado = "Editorial modificada con éxito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        sql =f"SELECT * FROM editoriales WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre==datos[1]

# Para cuando la editorial no existe
    def test_modifica2(self):
        id = "ed099"
        nombre = "Editorial Inexistente"
        idPais = "ES"
        nuevo = {"idEditorial":id, "nombre":nombre, "idPais":idPais}
        esperado = "Editorial no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("ed002","Editorial eliminada con éxito"),
         ("ed099","Editorial no existe")]
    )
    def test_elimina(self,id_entrada, esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.delete(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        mi_db.commit()
        sql =f"SELECT * FROM editoriales WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos)==0