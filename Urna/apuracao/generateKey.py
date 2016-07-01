# -*- coding: utf-8 -*-
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode

def generate_RSA(bits=1024):
	new_key = RSA.generate(bits, e=65537)
	public_key = new_key.publickey().exportKey("PEM")
	private_key = new_key.exportKey("PEM")
	pubHandle = open('../../files/publickey.pem','wb')
	pubHandle.write(public_key)
	pubHandle.close()
	privHandle = open('../../files/privatekey.pem', 'wb')
	privHandle.write(private_key)
	privHandle.close()

def encrypt(message, f):
	publicKeyFile = f.read()
	rsakey = RSA.importKey(publicKeyFile)
	rsakey = PKCS1_OAEP.new(rsakey)
	encrypted = rsakey.encrypt(message)
	# print encrypted.encode('base64')
	return encrypted.encode('base64')

def decrypt(message, f):
	ciphertext = base64.b64decode(message) if not isinstance(message, bytes) else message
	privateKeyFile = f.read()
	rsakey = RSA.importKey(privateKeyFile)
	rsakey = PKCS1_OAEP.new(rsakey)
	# print message
	decrypted = rsakey.decrypt(b64decode(message))
	return decrypted


# Decrypt messages using own private keys...
# decrypted      = keypair.decrypt(encrypted)

# Signature validation and console output...
# hash_decrypted = MD5.new(decrypted).digest()
# if pubkey.verify(hash_decrypted, signature):
#     print "Message received:"
#     print decrypted
#     print ""
