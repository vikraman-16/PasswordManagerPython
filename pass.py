import firebase_admin
from firebase_admin import credentials, firestore
import getpass
import hashlib
import os


# Initialize Firebase Admin SDK
cred = credentials.Certificate("./passwordmanager-7bda5-firebase-adminsdk-wrgst-9a55a6dec0.json")
firebase_admin.initialize_app(cred)  # Initialize the app with credentials

# Create a Firestore client
db = firestore.client()

def hash_password(password):
    """Hash the password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_password(account_name, username, password):
    """Add a password to the cloud."""
    hashed_password = hash_password(password)
    db.collection('passwords').document(account_name).set({
        'username': username,
        'password': hashed_password
    })
    print(f"Password for {account_name} added successfully.")

def get_password(account_name):
    """Retrieve a password from the cloud."""
    doc = db.collection('passwords').document(account_name).get()
    if doc.exists:
        data = doc.to_dict()
        print(f"Account: {account_name}")
        print(f"Username: {data['username']}")
        print(f"Password (hashed): {data['password']}")
    else:
        print(f"No account found for {account_name}.")

def delete_password(account_name):
    """Delete a password from the cloud."""
    db.collection('passwords').document(account_name).delete()
    print(f"Password for {account_name} deleted successfully.")

def main():
    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. Get Password")
        print("3. Delete Password")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            account_name = input("Enter the account name: ")
            username = input("Enter the username: ")
            password = getpass.getpass("Enter the password: ")
            add_password(account_name, username, password)
        elif choice == '2':
            account_name = input("Enter the account name: ")
            get_password(account_name)
        elif choice == '3':
            account_name = input("Enter the account name: ")
            delete_password(account_name)
        elif choice == '4':
            print("Exiting Password Manager.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

