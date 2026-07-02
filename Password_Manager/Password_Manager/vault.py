import json

def load_entries(decrypted_bytes: bytes) -> list:
	"""
	Load entries from decrypted bytes.
	Args:
		decrypted_bytes (bytes): The decrypted bytes to load entries from.
	Returns:
		list: A list of entries loaded from the decrypted bytes.
	"""
	try:
		# Decode the bytes to a string
		decrypted_str = decrypted_bytes.decode('utf-8')
		# Load the JSON data from the string
		vault_dict = json.loads(decrypted_str)
		return vault_dict["entries"]
	except (UnicodeDecodeError, json.JSONDecodeError) as e:
		print(f"Error loading entries: {e}")
		return []

def save_entries(entries: list) -> bytes:
	"""
	Take a list of entries and convert it to JSON bytes.
	"""
	try:
		# Create a dictionary with the entries
		vault_dict = {"entries": entries}
		# Convert the dictionary to a JSON string
		vault_str = json.dumps(vault_dict)
		# Encode the string to bytes
		return vault_str.encode('utf-8')
	except (TypeError, ValueError) as e:
		print(f"Error saving entries: {e}")
		return b""

def add_entry(entries: list, site: str, username: str, password: str, notes: str = "") -> list:
	"""
	Add a new entry to the list of entries.
	Args:
		entries (list): The current list of entries.
		site (str): The site or app name.
		username (str): The username or email.
		password (str): The password.
		notes (str): Optional notes. Defaults to empty string.
	Returns:
		list: The updated list of entries.
	"""
	new_entry = {
		"site": site,
		"username": username,
		"password": password,
		"notes": notes,
	}
	entries.append(new_entry)
	return entries

def find_entries(entries: list, site: str) -> list:
	"""
	Search for entries matching a site name.
		Returns a list of matching entries(could be more than one).
	"""
	matching_entries = [entry for entry in entries if site.lower() in entry["site"].lower()]
	return matching_entries

def delete_entry(entries: list, index: int) -> list:
	"""
	Delete an entry at the specified index.
	Returns the updated list of entries.
	"""
	if 0 <= index < len(entries):
		entries.pop(index)
	else:
		print(f"Invalid index: {index}. No entry deleted.")
	return entries

def list_entries(entries: list) -> None:
	"""
	Print all entries in a readable format.
	"""
	if not entries:
		print("No entries found.")
		return
	for i, entry in enumerate(entries):
		print(f"Entry {i}:")
		print(f"  Site: {entry['site']}")
		print(f"  Username: {entry['username']}")
		print(f"  Password: ********")
		if entry.get('notes'):
			print(f"  Notes: {entry['notes']}")
		print("-" * 20)
