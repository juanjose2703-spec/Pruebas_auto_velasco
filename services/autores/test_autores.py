from conexion import *
import pytest

class Test_autores:

    def setup_class(self):
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5082/autores"
        # Insertar pais propio para las pruebas de autores
        mi_cursor.execute("DELETE FROM autores WHERE idAutor IN ('autor001','autor002')")
        mi_cursor.execute("DELETE FROM paises WHERE idPais='MX'")
        mi_db.commit()
        sql = f"INSERT INTO paises (idPais,nombre,continente) VALUES ('MX','Mexico','America')"
        mi_cursor.execute(sql)
        mi_db.commit()
        id = "autor001"
        nombre = "Gabriel Garcia"
        email = "gabriel@test.com"
        idPais = "MX"
        sql = f"INSERT INTO autores (idAutor,nombre,email,idPais) VALUES ('{id}','{nombre}','{email}','{idPais}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        # Limpia la base de datos
        sql = f"DELETE FROM autores WHERE idAutor IN ('autor001','autor002')"
        mi_cursor.execute(sql)
        sql = f"DELETE FROM paises WHERE idPais='MX'"
        mi_cursor.execute(sql)
        mi_db.commit()

    def test_lista_autores(self):
        esperado = "autores"
        # Ejecutar la prueba
        calculado = requests.get(self.url)
        # Verificación
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"]==esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada","esperado_entrada"],
        [({"idAutor":"autor002", "nombre":"Andres Caicedo","email":"andres@test.com","idPais":"MX"},"Autor agregado con éxito"),
         ({"idAutor":"autor001", "nombre":"Gabriel Garcia","email":"gabriel@test.com","idPais":"MX"},"Id de autor ya existe")]
    )
    def test_agregar(self,nuevo_entrada,esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.post(self.url,json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("autor001","Autor encontrado"),
         ("autor999","Autor no encontrado")]
    )
    def test_busqueda(self,id_entrada,esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.get(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    # Para cuando el autor existe y se modifica con éxito
    def test_modifica1(self):
        id = "autor001"
        nombre = "Gabriel Garcia Modificado"
        email = "gabriel_mod@test.com"
        idPais = "MX"
        nuevo = {"idAutor":id, "nombre":nombre, "email":email, "idPais":idPais}
        esperado = "Autor modificado con éxito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        sql =f"SELECT * FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre==datos[1] and email==datos[2]

# Para cuando el autor no existe
    def test_modifica2(self):
        id = "autor999"
        nombre = "Autor Inexistente"
        email = "noexiste@test.com"
        idPais = "MX"
        nuevo = {"idAutor":id, "nombre":nombre, "email":email, "idPais":idPais}
        esperado = "Autor no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("autor002","Autor eliminado con éxito"),
         ("autor999","Autor no existe")]
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
        sql =f"SELECT * FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos)==0