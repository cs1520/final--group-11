from google.cloud import datastore
import datetime
import hashlib
import os

class User:
    def __init__(self,username, password_hash, salt):
        self.username = username
        self.password_hash = password_hash
        self.salt = salt

class UserStorage:
    def __init__(self, datastore_client):
        self.datastore_c = datastore_client
    
    def verify_password(self, username, password):
        user_key = self.datastore_c.key("Login", username)
        user = self.datastore_c.get(user_key)
        if user != False:
            encoded = password.encode("utf-8")
            hash_attempt = hashlib.pbkdf2_hmac("sha256", encoded, user["salt"], 100000)
            if hash_attempt == user["password_hash"]:
                return User(user["username"], user["password_hash"], user["salt"])
        return None

    def list_existing_users(self):
        query = self.datastore_c.query(kind="Login")
        users = query.fetch()
        return [u["username"] for u in users if "username" in u]
        