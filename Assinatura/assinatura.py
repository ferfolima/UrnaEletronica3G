from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from base64 import b64encode

def sign(message, f):
    privateKeyFile = f.read()
    key = RSA.importKey(privateKeyFile)
    message = bytes(message).encode('utf-8')
    h = SHA256.new(message)
    signer = PKCS1_v1_5.new(key)
    signature = b64encode(signer.sign(h))
    return signature, message

def verifySignature(sigAndMessage, f):
    signature, message = sigAndMessage.split(":")
    publicKeyFile = f.read()
    key = RSA.importKey(publicKeyFile)
    h = SHA256.new(signature)
    verifier = PKCS1_v1_5.new(key)
    verifier.verify(h, signature)
    return message