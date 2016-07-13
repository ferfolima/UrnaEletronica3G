#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Cargos, Base

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
        self.engine = create_engine('sqlite:///../files/eleicoesdb.db')
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