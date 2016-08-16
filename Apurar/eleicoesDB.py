#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from model import Cargos, Base

script_dir = os.path.dirname(__file__)
ELEICOESDB_FILE = os.path.join(script_dir, "../files/eleicoesdb.db")

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class DAO(Singleton):
    def __init__(self):
        self._connect()
        return

    def _connect(self):
        self.engine = create_engine('sqlite:///' + ELEICOESDB_FILE)
        Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    def getCargos(self):
        rows = self.session.query(Cargos.nome_cargo).all()
        rows = [i for i, in rows]
        return rows

    def getCargosQtde(self):
        rows = self.session.query(Cargos.nome_cargo, Cargos.qtde_votos).all()
        rows = [y[0] for y in rows for x in range(int(y[1]))]
        return rows