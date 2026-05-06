from conexion import *
import pytest 

class Test_paises:

    def setup_class(self):
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5081/paises"
        sql = f"INSERT INTO paises (idpais,nombre,continente) VALUES ('01','PaisPrueba','America')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        # Limpia la base de datos
        sql = f"DELETE FROM paises WHERE idPais='01'"
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
        [({"idPais":"02", "nombre":"PaisTest","continente":"Europa"},"Pais agregado con éxito"),
        ({"idPais":"01", "nombre":"PaisPrueba", "continente":"America"},"Id de Pais ya existe")]
    )
    def test_agregar(self,nuevo_entrada,esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.post(self.url,json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado_entrada


    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("01","Pais encontrado"),
        ("03","Pais no encontrado"),]
    )
    
    def test_busqueda(self,id_entrada,esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.get(f"{self.url}/{id_entrada}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]

    # Para cuando el pais existe y se modifica con éxito
    def test_modifica1(self):
        id = "01"
        nuevo = {"idPais":id,"nombre":"PaisPruebaModificado", "continente":"Asia"}
        esperado = "Pais modificado con éxito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        sql =f"SELECT * FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert datos[1] == "PaisPruebaModificado" and datos[2] == "Asia"

# Para cuando el pais no existe
    def test_modifica2(self):
        id = "02"
        nuevo = {"idPais":id, "nombre": "Inexistente", "continente":"Oceania"}
        esperado = "Pais no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("01","Pais eliminado con éxito!"),
        ("03","Pais no existe")]
    )
    def test_elimina(self,id_entrada, esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.delete(f"{self.url}/{id_entrada}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada in calculado.json()["mensaje"]
        mi_db.commit()
        sql =f"SELECT * FROM paises WHERE idPais='{id_entrada}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos)==0
    
    
