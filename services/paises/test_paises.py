from conexion import *
import pytest

class Test_paises:

    def setup_class(self):
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5081/paises"
        id = "CO"
        nombre = "Colombia"
        continente = "America"
        sql = f"INSERT INTO paises (idPais,nombre,continente) VALUES ('{id}','{nombre}','{continente}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        # Limpia la base de datos
        sql = f"DELETE FROM paises WHERE idPais='CO'"
        mi_cursor.execute(sql)
        sql = f"DELETE FROM paises WHERE idPais='AR'"
        mi_cursor.execute(sql)
        mi_db.commit()

    def test_lista_paises(self):
        esperado = "paises"
        # Ejecutar la prueba
        calculado = requests.get(self.url)
        # Verificación
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"]==esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada","esperado_entrada"],
        [({"idPais":"AR", "nombre":"Argentina","continente":"America"},"Pais agregado con éxito"),
        ({"idPais":"CO", "nombre":"Colombia","continente":"America"},"Id de Pais ya existe")]
    )
    def test_agregar(self,nuevo_entrada,esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.post(self.url,json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("CO","Pais encontrado"),
        ("VE","Pais no encontrado")]
    )
    def test_busqueda(self,id_entrada,esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.get(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    # Para cuando el pais existe y se modifica con éxito
    def test_modifica1(self):
        id = "CO"
        nombre = "Colombia Modificado"
        continente = "America del Sur"
        nuevo = {"idPais":id, "nombre":nombre, "continente":continente}
        esperado = "Pais modificado con éxito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        sql =f"SELECT * FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre==datos[1] and continente==datos[2]

# Para cuando el pais no existe
    def test_modifica2(self):
        id = "VE"
        nombre = "Venezuela"
        continente = "America"
        nuevo = {"idPais":id, "nombre":nombre, "continente":continente}
        esperado = "Pais no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("AR","Pais eliminado con éxito"),
        ("VE","Pais no existe")]
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
        sql =f"SELECT * FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos)==0