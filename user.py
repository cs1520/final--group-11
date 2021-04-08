from google.cloud import datastore
import datetime
import hashlib
import os

class User:
    def __init__(self,username, password_hash, salt):
        self.username = username
        self.password_hash = password_hash
        self.salt = salt

def generate_credentials(username, password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("utf-8")
    encoded = password.encode("utf-8")
    password_hash = hashlib.pbkdf2_hmac("sha256", encoded, salt, 100000)
    return User(username, password_hash, salt)

class UserStorage:
    def __init__(self, datastore_client):
        self.ds_c = datastore_client
    
    def verify_password(self, username, password):
        user_key = self.ds_c.key("Login", username)
        user = self.ds_c.get(user_key)
        if user == False:
            return None
        encoded = password.encode("utf-8")
        hash_attempt = hashlib.pbkdf2_hmac("sha256", encoded, user["salt"], 100000)
        if hash_attempt != user["password_hash"]:
            return None
        return User(user["username"], user["password_hash"], user["salt"])
    
    def store_new_credentials(self, creds):
        user_key = self.ds_c.key("Login", creds.username)
        user = datastore.Entity(key=user_key)
        user["username"] = creds.username
        user["password_hash"] = creds.password_hash
        user["salt"] = creds.salt
        self.ds_c.put(user)

    def list_existing_users(self):
        query = self.ds_c.query(kind="Login")
        users = query.fetch()
        return [u["username"] for u in users if "username" in u]