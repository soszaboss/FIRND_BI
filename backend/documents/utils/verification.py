from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import hashlib

def hasher_pdf(chemin_pdf):
    with open(chemin_pdf, 'rb') as fichier_pdf:
        contenu = fichier_pdf.read()
        hash_obj = hashlib.sha256(contenu)
        return hash_obj.hexdigest()

def verifier_signature(hash_contenu, signature, cle_publique):
    try:
        cle_publique_obj = RSA.import_key(cle_publique)
        hash_obj = SHA256.new(hash_contenu.encode('utf-8'))
        pkcs1_15.new(cle_publique_obj).verify(hash_obj, signature)
        return True
    except (ValueError, TypeError):
        return False
