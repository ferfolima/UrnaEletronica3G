import ed25519

def sign(message, f):
    privateKeyFile = f.read()
    key = ed25519.SigningKey(privateKeyFile)
    signature = key.sign(message, encoding="base64")
    return signature, message

def verifySignature(sigAndMessage, f):
    signature, message = sigAndMessage.split(":")
    publicKeyFile = f.read()
    key = ed25519.VerifyingKey(publicKeyFile)
    key.verify(signature, message, encoding="base64")
    return message