from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import hashlib

def signer_hash(hash_contenu, cle_privee):
    cle_privee_obj = RSA.import_key(cle_privee)
    hash_obj = SHA256.new(hash_contenu.encode('utf-8'))
    signature = pkcs1_15.new(cle_privee_obj).sign(hash_obj)
    return signature

def generer_paire_de_cles():
    cle_privee = RSA.generate(2048)
    cle_publique = cle_privee.publickey().export_key()
    return cle_privee.export_key(), cle_publique

def hasher_pdf(file_path):
    with open(file_path, 'rb') as fichier_pdf:
        contenu = fichier_pdf.read()
        hash_obj = hashlib.sha256(contenu)
        fichier_pdf.close()
    return hash_obj.hexdigest(), contenu
