import secrets
from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import json



def generate_salt(length: int = 16) -> bytes:
    """
    We default to 16 as AES has 128 bit, and overall our chances of overlapping with any other passwords is tiny. 
    """
    if length < 16:
        raise ValueError("Salt length must be at least 16 bytes.")
    salt = secrets.token_bytes(length)
    return salt



def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    We derive our key from the master password and salt using Argon2id, which is a memory-hard hashing algorithm designed to resist GPU cracking attacks.
    This is superior to using a simple hash function like SHA-256, which is fast and can be brute-forced more easily.
    """
    derived_key = hash_secret_raw(
        secret = master_password.encode('utf-8'),
        salt = salt,
        time_cost = 3,
        memory_cost = 65536,
        parallelism = 4,
        hash_len = 32,
        type = Type.ID)
    return derived_key


def generate_nonce() -> bytes:
    """
    Must be unique 12-byte nonce for AES-GCM
    """
    nonce = secrets.token_bytes(12)
    return nonce

def encrypt(key: bytes, plaintext: bytes, nonce: bytes) -> bytes:
    """
    Encrypt the plaintext using AES-GCM with the derived key and nonce. AES-GCM provides both confidentiality and integrity for the encrypted data.
    """
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return ciphertext

def decrypt(key: bytes, ciphertext: bytes, nonce: bytes) -> bytes:
    """
    Decrypt the ciphertext using AES-GCM with the derived key and nonce.
    """
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext

def bytes_to_base64(data: bytes) -> str:
    """ 
    Convert bytes to a base64 encoded string.
    """
    return base64.b64encode(data).decode('utf-8')

def base64_to_bytes(data: str) -> bytes:
    """
    Convert a base64 encoded string back to bytes.
    """
    return base64.b64decode(data.encode('utf-8'))

def save_vault(filepath: str, salt: bytes, nonce: bytes, ciphertext: bytes) -> None:
    """
    Save the vault data to a JSON file.
    """
    vault_data = {
        'salt': bytes_to_base64(salt),
        'nonce': bytes_to_base64(nonce),
        'ciphertext': bytes_to_base64(ciphertext)
    }
    with open(filepath, 'w') as f:
        json.dump(vault_data, f)

def load_vault(filepath: str) -> tuple:
    """
    Read a vault JSON file and return (salt, nonce, ciphertext) as bytes.
    """
    with open(filepath, 'r') as f:
        vault_data = json.load(f)
    return (
        base64_to_bytes(vault_data['salt']),
        base64_to_bytes(vault_data['nonce']),
        base64_to_bytes(vault_data['ciphertext'])
    )
