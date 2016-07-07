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

    def getCargosQtde(self):
        cursor = self._get_cursor()
        cursor.execute("SELECT nome_cargo, qtde_votos FROM cargos")
        rows = cursor.fetchall()
        cursor.close()
        rows = [y[0] for y in rows for x in range(int(y[1]))]
        return rows
