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

    def criarTabelas(self):
        cursor = self._get_cursor()
        cursor.execute("create table if not exists partidos("
                       "numero_partido int not null, "
                       "nome_partido varchar(255) not null, "
                       "sigla_partido varchar(255) not null, "
                       "presidente_partido varchar(255) not null, "
                       "foto_partido mediumblob, "
                       "unique(numero_partido), "
                       "primary key (numero_partido));")

        cursor.execute("create table if not exists cargos("
                       "id int not null auto_increment, "
                       "nome_cargo varchar(255) not null, "
                       "primary key(id));")

        cursor.execute("create table if not exists candidatos("
                       "id_cargo int not null, "
                       "id_partido int not null, "
                       "numero_candidato int not null, "
                       "nome_candidato varchar(255) not null, "
                       "titulo_candidato varchar(255) not null, "
                       "id int not null auto_increment, "
                       "foto_candidato mediumblob, "
                       "unique(titulo_candidato), "
                       "primary key(id), "
                       "foreign key(id_cargo) references cargos(id), "
                       "foreign key(id_partido) references partidos(numero_partido));")

        cursor.close()

    def inserirCargo(self, nomeCargo):
        cursor = self._get_cursor()
        cursor.execute("INSERT INTO cargos (nome_cargo) VALUES (%s)", (nomeCargo))
        self._commit()
        cursor.close()

    def inserirPartido(self, numeroPartido, nomePartido, siglaPartido, presidentePartido, img):
        cursor = self._get_cursor()
        cursor.execute("INSERT INTO partidos (numero_partido, nome_partido, sigla_partido, presidente_partido, foto_partido) "
                       "VALUES (%s, %s, %s, %s, %s)", (numeroPartido, nomePartido, siglaPartido, presidentePartido, img))
        self._commit()
        cursor.close()

    def inserirCandidato(self, idCargo, idPartido, numeroCandidato, nomeCandidato, tituloCandidato, fotoCandidato):
        cursor = self._get_cursor()
        cursor.execute(
            "INSERT INTO candidatos (id_cargo, id_partido, numero_candidato, nome_candidato, titulo_candidato, foto_candidato) "
            "VALUES (%s, %s, %s, %s, %s, %s)", (idCargo, idPartido, numeroCandidato, nomeCandidato, tituloCandidato, fotoCandidato))
        self._commit()
        cursor.close()

    def getSiglas(self):
        cursor = self._get_cursor()
        cursor.execute("SELECT sigla_partido FROM partidos")
        rows = cursor.fetchall()
        cursor.close()
        rows = [x[0] for x in rows]
        return rows

    def getPartidoId(self, partido):
        cursor = self._get_cursor()
        cursor.execute("SELECT numero_partido FROM partidos where sigla_partido = %s", (partido))
        row = cursor.fetchone()
        cursor.close()
        return row[0]

    def getCargos(self):
        cursor = self._get_cursor()
        cursor.execute("SELECT nome_cargo FROM cargos")
        rows = cursor.fetchall()
        cursor.close()
        rows = [x[0] for x in rows]
        return rows

    def getCargoId(self, cargo):
        cursor = self._get_cursor()
        cursor.execute("SELECT id FROM cargos where nome_cargo = %s", (cargo))
        row = cursor.fetchone()
        cursor.close()
        return row[0]

    def getFotoPartido(self, sigla):
        cursor = self._get_cursor()
        cursor.execute("SELECT foto_partido FROM partidos where sigla_partido = %s", (sigla))
        row = cursor.fetchone()
        cursor.close()
        return row[0]