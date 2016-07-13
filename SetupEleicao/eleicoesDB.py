#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = self.engine

        self.DBSession = sessionmaker(bind=self.engine)
        # A DBSession() instance establishes all conversations with the database
        # and represents a "staging zone" for all the objects loaded into the
        # database session object. Any change made against the objects in the
        # session won't be persisted into the database until you call
        # session.commit(). If you're not happy about the changes, you can
        # revert all of them back to the last commit by calling
        # session.rollback()
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
        self.session.add(novo_candidato)
        self.session.commit()

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

    def getFotoPartido(self, sigla):
        row = self.session.query(Partidos.foto_partido).filter(Partidos.sigla_partido == sigla)
        row = [i for i, in row]
        return row[0]