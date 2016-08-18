#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Crypto.PublicKey import RSA
import os

script_dir = os.path.dirname(__file__)
PUBLIC_KEY = os.path.join(script_dir, "../files/publickey.pem")
PRIVATE_KEY = os.path.join(script_dir, "../files/privatekey.pem")


def generate_RSA(bits=2048):
    new_key = RSA.generate(bits, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")
    pubHandle = open(PUBLIC_KEY, 'wb')
    pubHandle.write(public_key)
    pubHandle.close()
    privHandle = open(PRIVATE_KEY, 'wb')
    privHandle.write(private_key)
    privHandle.close()