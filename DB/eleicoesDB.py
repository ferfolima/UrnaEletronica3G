#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, and_
import os
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from DB.model import Partidos, Cargos, Candidatos, Base

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

    def apagarDados(self):
        self.session.query(Candidatos).delete()
        self.session.query(Cargos).delete()
        self.session.query(Partidos).delete()
        self.session.commit()

    def inserirCargo(self, nomeCargo, qtdeVotos):
        novo_cargo = Cargos(nome_cargo=nomeCargo, qtde_votos=qtdeVotos)
        self.session.add(novo_cargo)
        self.session.commit()

    def inserirPartido(self, numeroPartido, nomePartido, siglaPartido, presidentePartido, img):
        novo_partido = Partidos(id=numeroPartido, nome_partido=nomePartido, sigla_partido=siglaPartido, presidente_partido=presidentePartido, foto_partido=img)
        self.session.add(novo_partido)
        self.session.commit()

    def inserirCandidato(self, idCargo, idPartido, numeroCandidato, nomeCandidato, tituloCandidato, fotoCandidato):
        novo_candidato = Candidatos(id_cargo=idCargo, id_partido=idPartido, numero_candidato=numeroCandidato, nome_candidato=nomeCandidato,     titulo_candidato=tituloCandidato, foto_candidato=fotoCandidato)
        try:
            self.session.add(novo_candidato)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            return None
        return novo_candidato

    def getSiglas(self):
        rows = self.session.query(Partidos.sigla_partido).all()
        rows =  [i for i, in rows]
        return rows

    def getPartidoId(self, partido):
        row = self.session.query(Partidos.id).filter(Partidos.sigla_partido == partido)
        row = [i for i, in row]
        return row[0]

    def getCargos(self):
        rows = self.session.query(Cargos.nome_cargo).all()
        rows = [i for i, in rows]
        return rows

    def getCargoId(self, cargo):
        row = self.session.query(Cargos.id).filter(Cargos.nome_cargo == cargo)
        row = [i for i, in row]
        return row[0]

    def getCargosQtde(self):
        rows = self.session.query(Cargos.nome_cargo, Cargos.qtde_votos).all()
        rows = [y[0] for y in rows for x in range(int(y[1]))]
        return rows

    def getFotoPartido(self, sigla):
        row = self.session.query(Partidos.foto_partido).filter(Partidos.sigla_partido == sigla)
        row = [i for i, in row]
        return row[0]

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