#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Cargos(Base):
    __tablename__ = 'cargos'
    id = Column(Integer, primary_key=True)
    nome_cargo = Column(String(250), nullable=False)
    qtde_votos = Column(Integer, nullable=False)

class Partidos(Base):
    __tablename__ = 'partidos'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=False)
    nome_partido = Column(String(250), nullable=False)
    sigla_partido = Column(String(250), nullable=False)
    presidente_partido = Column(String(250), nullable=False)
    foto_partido = Column(BLOB, nullable=True)

class Candidatos(Base):
    __tablename__ = 'candidatos'
    id = Column(Integer, primary_key=True)
    id_cargo = Column(Integer, ForeignKey('cargos.id'), nullable=False)
    id_partido = Column(Integer, ForeignKey('partidos.id'), nullable=False)
    numero_candidato = Column(Integer, nullable=False)
    nome_candidato = Column(String(250), nullable=False)
    titulo_candidato = Column(String(250), nullable=False, unique=True)
    foto_candidato = Column(BLOB, nullable=True)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
# engine = create_engine('sqlite:///../files/eleicoesdb.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
# Base.metadata.create_all(engine)