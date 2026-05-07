from conexion import *
import pytest
import requests

class Test_paises:

    def setup_class(self):
        self.url = "http://localhost:5081/paises"

        id = "01"
        nombre = "PaisPrueba"
        continente = "America"

        sql = f"INSERT INTO paises (idPais,nombre,continente) VALUES ('{id}','{nombre}','{continente}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        sql = "DELETE FROM paises WHERE idPais IN ('01','02')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def test_lista_paises(self):
        esperado = "paises"
        calculado = requests.get(self.url)

        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada","esperado_entrada"],
        [
            ({"idPais":"02", "nombre":"PaisTest","continente":"Europa"}, "Pais agregado con éxito"),
            ({"idPais":"01", "nombre":"PaisPrueba","continente":"America"}, "Id de Pais ya existe")
        ]
    )
    def test_agregar(self, nuevo_entrada, esperado_entrada):
        calculado = requests.post(self.url, json=nuevo_entrada)

        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [
            ("01","Pais encontrado"),
            ("03","Pais no encontrado")
        ]
    )
    def test_busqueda(self, id_entrada, esperado_entrada):
        calculado = requests.get(f"{self.url}/{id_entrada}")

        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]

    def test_modifica1(self):
        id = "01"
        nuevo = {"idPais":id, "nombre":"PaisModificado","continente":"Asia"}
        esperado = "Pais modificado con éxito"

        calculado = requests.put(f"{self.url}/{id}", json=nuevo)

        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

        sql = f"SELECT * FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]

        assert datos[1] == "PaisModificado" and datos[2] == "Asia"

    def test_modifica2(self):
        id = "99"
        nuevo = {"idPais":id, "nombre":"Inexistente","continente":"Oceania"}
        esperado = "Pais no existe"

        calculado = requests.put(f"{self.url}/{id}", json=nuevo)

        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [
            ("02","Pais eliminado con éxito"),
            ("99","Pais no existe")
        ]
    )
    def test_elimina(self, id_entrada, esperado_entrada):
        calculado = requests.delete(f"{self.url}/{id_entrada}")

        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]

        mi_db.commit()
        sql = f"SELECT * FROM paises WHERE idPais='{id_entrada}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()

        assert len(datos) == 0