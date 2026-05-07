"""
Modelo para la gestión de autores:
todo lo relacionado con la persistencia (SQL).
"""
from conexion import *

class Autores:
    def listar(self):
        sql = "SELECT * FROM autores"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado
    
    def consultar(self, id):
        sql = f"SELECT * FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado
    
    def agregar(self, id, nom, email, idPais):
        sql = f"INSERT INTO autores (idAutor, nombre, email, idPais) VALUES ('{id}', '{nom}', '{email}', '{idPais}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def modificar(self, id, nom, email, idPais):
        sql = f"UPDATE autores SET nombre='{nom}', email='{email}', idPais='{idPais}' WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        return self.consultar(id)

    def eliminar(self, id):
        sql = f"DELETE FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()

mis_autores = Autores()