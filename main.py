#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from Urna.Apurar import main as apurar
from Urna.SetupEleicao import main as setupEleicao
from Urna.SetupUrna import main as setupUrna
from Urna.Verificar import main as verificar
from Urna.Votar import main as votar

parser = argparse.ArgumentParser(description="Selecione o módulo desejado")
parser.add_argument('--modulo','-m', help='Digite o nome do modulo <apurar>, <setupEleicao>, <setupUrna>, <verificar>, <votar>')

args = parser.parse_args()

switcher = {
    "apurar": apurar,
    "setupEleicao": setupEleicao,
    "setupUrna": setupUrna,
    "verificar": verificar,
    "votar": votar
}

func = switcher.get(args.modulo)
if(func is not None):
    func.main()
else:
    print("Módulo escolhido não existe")
