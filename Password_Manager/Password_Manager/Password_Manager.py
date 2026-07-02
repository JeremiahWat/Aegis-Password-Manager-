import getpass
import secrets
import string
import json
import random

from pathlib import Path


from vault_crypto import generate_salt, derive_key, generate_nonce, encrypt, decrypt, save_vault, load_vault

from vault import load_entries, save_entries, add_entry, find_entries, delete_entry, list_entries


def vault_exists(path: str) -> bool:
    """
    This function checks if a vault file already exists in the given path. 
    """
    return Path(path).exists()

def generate_password(length: int = 16) -> str:
    """
    Generate a cryptographically secure random password.
    """
    if length < 12:
        raise ValueError("Password length must be at least 12 characters.")
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password.extend(secrets.choice(alphabet) for _ in range(length - 4))
    random.SystemRandom().shuffle(password)
    return "".join(password)

def prompt_for_new_master_password() -> str:
    """
    PROMPT FOR NEW MASTER PASSWORD FUNCTION
    """
    while True:
        master_password = getpass.getpass(prompt="Please enter a new master password: ")
        confirm_password = getpass.getpass(prompt="Please confirm your new master password: ")
        if master_password == confirm_password and len(master_password) >= 12 and any(c.islower() for c in master_password) and any(c.isupper() for c in master_password) and any(c.isdigit() for c in master_password) and any(c in string.punctuation for c in master_password):
            return master_password
        elif master_password == confirm_password:
            print("Failed complexity requirements. Please try again.")
        elif master_password != confirm_password:
            print("Passwords do not match. Please try again.")

def prompt_for_existing_master_password() -> str:
    """
    PROMPT FOR EXISTING MASTER PASSWORD FUNCTION
    """
    master_password = getpass.getpass(prompt="Please enter your master password: ")
    return master_password

def create_empty_vault() -> bytes:
    """
    Return an empty vault structure as JSON bytes, ready to encrypt and store.
    """
    empty_vault = {
        "entries": []
    }
    return json.dumps(empty_vault).encode('utf-8')

def show_menu(entries: list, key: bytes, salt: bytes, vault_path: str) -> None:
    """
    Display the main menu and handle user choices.
    """
    while True:
        print("\n--- Password Manager ---")
        print("1. List entries")
        print("2. Add entry")
        print("3. Find entry")
        print("4. Delete entry")
        print("5. Lock and exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            list_entries(entries)
        elif choice == "2":
            site = input("Enter site: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            notes = input("Enter notes (optional): ")
            entries = add_entry(entries, site, username, password, notes)
        elif choice == "3":
            site = input("Enter site to search: ")
            matching_entries = find_entries(entries, site)
            list_entries(matching_entries)
        elif choice == "4":
            list_entries(entries)
            try:
                index = int(input("Enter the index of the entry to delete: "))
                entries = delete_entry(entries, index)
            except ValueError:
                print("Invalid input. Please enter a valid integer index.")
        elif choice == "5":
            vault_bytes = save_entries(entries)
            nonce = generate_nonce()
            ciphertext = encrypt(key, vault_bytes, nonce)
            save_vault(vault_path, salt, nonce, ciphertext)
            print("Vault locked. Goodbye.")
            break
        else:
            print("Invalid option. Please try again.")

"""
MAIN
"""
def main():
    vault_path = "vault.json"  # Specify the path to your vault file
    if vault_exists(vault_path):
        print("Vault file already exists.")
        master_password = prompt_for_existing_master_password()
        loaded_salt, loaded_nonce, loaded_ciphertext = load_vault(vault_path)
        loaded_key = derive_key(master_password, loaded_salt)
        try:
            decrypted_plaintext = decrypt(loaded_key, loaded_ciphertext, loaded_nonce)
            entries = load_entries(decrypted_plaintext)
            print("Vault unlocked successfully.")
            show_menu(entries, loaded_key, loaded_salt, vault_path)
        except Exception:
            print("Incorrect master password. Could not unlock vault.")
    else:
        print("Vault file does not exist. Creating a new vault.")
        master_password = prompt_for_new_master_password()
        vault_bytes = create_empty_vault()
        salt = generate_salt()
        key = derive_key(master_password, salt)
        nonce = generate_nonce()
        ciphertext = encrypt(key, vault_bytes, nonce)
        save_vault(vault_path, salt, nonce, ciphertext)
        print("New vault created successfully.")
        show_menu([], key, salt, vault_path)

    
if __name__ == "__main__":
    main()