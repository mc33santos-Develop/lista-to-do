# /backend/auth.py
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash 
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]
users_collection = db.users 


def add_user(email, password):
    if users_collection.find_one({'email': email}):
        return None  
    
    hashed_pw = generate_password_hash(password) 
    user_id = users_collection.insert_one({
        'email': email,
        'password': hashed_pw
    }).inserted_id 
    
    print(f"Usuário adicionado com sucesso! ID: {user_id}")
    return str(user_id)


def get_user_by_email(email):
    user = users_collection.find_one({'email': email})
    if user:
        return {
            '_id': str(user['_id']), 
            'email': user['email'], 
            'password': user['password'] 
        }
    return None


def authenticate_user(email, password):
    user = get_user_by_email(email)
   
    if user and check_password_hash(user['password'], password): 
        return str(user['_id'])
    return None