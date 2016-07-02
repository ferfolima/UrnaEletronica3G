#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class DAO(Singleton):
    def __init__(self):
        """
        Inits MySQL connection
        """
        self._connect()
        return

    def _connect(self):
        """
            Creates connection
            """
        self.connection = mdb.connect(host="localhost", \
                                          user="root", \
                                          passwd="#F20e12R90#", \
                                          db="eleicoesdb", \
                                          port=3306)
        return

    def _get_cursor(self):
        """
            Pings connection and returns cursor
            """
        try:
            self.connection.ping()
        except:
            self._connect()
        return self.connection.cursor()

    def _commit(self):
        self.connection.commit()

    def inserirPartido(self, numeroPartido, nomePartido, siglaPartido, presidentePartido, img):
        cursor = self._get_cursor()
        cursor.execute("INSERT INTO partidos VALUES (%s, %s, %s, %s, %s)", (numeroPartido, nomePartido, siglaPartido, presidentePartido, img))
        self._commit()
        cursor.close()

    def getSiglas(self):
        cursor = self._get_cursor()
        cursor.execute("SELECT sigla_partido FROM partidos")
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def getPartidoId(self, partido):
        cursor = self._get_cursor()
        cursor.execute("SELECT numero_partido FROM partidos where sigla_partido = %s", partido)
        row = cursor.fetchone()
        cursor.close()
        return row[0]

    def inserirCargo(self, nomeCargo):
        cursor = self._get_cursor()
        cursor.execute("INSERT INTO cargos (nome_cargo) VALUES (%s)", (nomeCargo))
        self._commit()
        cursor.close()

    def getCargos(self):
        cursor = self._get_cursor()
        cursor.execute("SELECT nome_cargo FROM cargos")
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def getCargoId(self, cargo):
        cursor = self._get_cursor()
        cursor.execute("SELECT id FROM cargos where nome_cargo = %s", cargo)
        row = cursor.fetchone()
        cursor.close()
        return row[0]

    def getQtdeCargos(self):
        cursor = self._get_cursor()
        cursor.execute("SELECT COUNT(id) FROM cargos")
        row = cursor.fetchone()
        cursor.close()
        return row[0]

    def inserirCandidato(self, idCargo, idPartido, numeroCandidato, nomeCandidato, tituloCandidato, fotoCandidato):
        cursor = self._get_cursor()
        cursor.execute("INSERT INTO candidatos (id_cargo, id_partido, numero_candidato, nome_candidato, titulo_candidato, foto_candidato) "
                       "VALUES (%s, %s, %s, %s, %s, %s)", (idCargo, idPartido, numeroCandidato, nomeCandidato, tituloCandidato, fotoCandidato))
        self._commit()
        cursor.close()

    def getCandidatoNumeroPartido(self, numerosDigitados, cargo):
        numero = "".join(str(x) for x in numerosDigitados)
        cursor = self._get_cursor()
        row_count = cursor.execute("SELECT A.nome_candidato, A.numero_candidato, B.sigla_partido, A.foto_candidato "
                                   "from candidatos as A  "
                                   "inner join partidos as B on A.id_partido = B.numero_partido  "
                                   "inner join cargos as C on A.id_cargo = C.id  "
                                   "where A.numero_candidato = {0} and C.nome_cargo = '{1}';".format(int(numero), cargo))

        if row_count > 0:
            row = cursor.fetchone()
            cursor.close()
            return row
        return (None, None, None, None)

    def getFotoPartido(self, sigla):
        cursor = self._get_cursor()
        cursor.execute("SELECT foto_partido FROM partidos where sigla_partido = '{0}'".format(sigla))
        row = cursor.fetchone()
        cursor.close()
        return row[0]

def main():
    DAO().inserirPartido("nome", "sigla", 1, "presidente")

if __name__ == "__main__":
    main()
