#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cargos(Base):
    __tablename__ = 'cargos'
    id = Column(Integer, primary_key=True)
    nome_cargo = Column(String(250), nullable=False)
    qtde_votos = Column(Integer, nullable=False)