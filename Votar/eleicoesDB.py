#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, and_
from model import Partidos, Cargos, Candidatos, Base

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

    def getQtdeCargos(self):
        row = self.session.query(func.sum(Cargos.qtde_votos))
        row = [i for i, in row]
        return row[0]

    def getQtdeVotosCargo(self, cargo):
        row = self.session.query(Cargos.qtde_votos).filter(Cargos.nome_cargo == cargo)
        row = [i for i, in row]
        return row[0]

    def getCandidatoNumeroPartido(self, numerosDigitados, cargo):
        numero = "".join(str(x) for x in numerosDigitados)
        row_count = self.session.query(Candidatos.nome_candidato, Candidatos.numero_candidato, Partidos.sigla_partido, Candidatos.foto_candidato)\
            .join(Partidos, Candidatos.id_partido == Partidos.id)\
            .join(Cargos, Candidatos.id_cargo == Cargos.id) \
            .filter(and_(Cargos.nome_cargo == cargo, Candidatos.numero_candidato == numero))\
            .all()
        if len(row_count) < 1:
            return (None, None, None, None)
        else:
            return row_count[0]