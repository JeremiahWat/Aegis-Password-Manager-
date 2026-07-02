# Aegis-Password-Manager-
A local encrypted password manager built in Python.
Argon2id was used for key derivation, AES-256-GCM for encryption, with no stored password hash. 

## Features
- Create and unlock an encrypted vault
- Add, view, search, and delete entries
- Cryptographically secure password generation
- Wrong password and tamper detection
- Single-device local storage

## Security Design
While some models online use SHA256 the disadvantage is despite its spead it can be brute forced. Argon2id is intentially a slow and memory-hard algorithm for hassing. It makes GPU-based brute force cracking significantly more expensive if an attacker obtains the encrypted vault. 
I used AES-256-GCM because I wanted authenticated encryption. Instead of just encrypting the vaults contents, I was also verifying that the encrypted data hadn't been modified. If someone tampered with the ciphertext, decryption would fail instead of returning corrupted or malicious data. 
A nonce is also used because AES-GCM requires it for each operation. I generate a new nonce every time I encrypt data so that encrypting identical passwords or vault data multiple times would produce different ciphertext each time. This prevents attackers from identifying repeated patterns.
The master password is never stored anywhere. The only proof of a correct password is that decryption succeeds. A wrong password derives the wrong key and AES-GCM;s authentication check fails. 
## Installation
pip install -r requirements.txt

## Usage
python Password_Manager.py

## Project Structure
- vault_crypto.py — cryptographic primitives
- vault.py — entry management  
- Password_Manager.py — main entry point

## Requirements
See requirements.txt
