#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ed25519
import os

script_dir = os.path.dirname(__file__)
PUBLIC_KEY = os.path.join(script_dir, "../files/publickey.pem")
PRIVATE_KEY = os.path.join(script_dir, "../files/privatekey.pem")


def generateKey():
    private_key, public_key = ed25519.create_keypair()
    pubHandle = open(PUBLIC_KEY, 'wb')
    pubHandle.write(public_key.to_bytes())
    pubHandle.close()
    privHandle = open(PRIVATE_KEY, 'wb')
    privHandle.write(private_key.to_bytes())
    privHandle.close()