# /backend/database.py
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]
tasks_collection = db.todos 



def get_all_tasks(user_id):
   
    query_filter = {'user_id': user_id} 
    tasks = []
  
    cursor = tasks_collection.find(query_filter)
    
    for task in cursor:
        task['_id'] = str(task['_id'])
       
        tasks.append({'_id': task['_id'], 'text': task['text'], 'done': task['done']}) 
        
    return tasks

def add_task(data, user_id):
   
    data['user_id'] = user_id 
    
    result = tasks_collection.insert_one(data) 
    new_task = tasks_collection.find_one({'_id': result.inserted_id})
    if new_task:
        new_task['_id'] = str(new_task['_id'])
    return new_task

def update_task(task_id, data, user_id):
    
    try:
        obj_id = ObjectId(task_id) 
    except Exception:
        return None 

    query_filter = {'_id': obj_id, 'user_id': user_id}
    
 
    update_data = {}
    if 'text' in data:
        update_data['text'] = data['text']
    if 'done' in data:
        update_data['done'] = data['done']
        
    if not update_data:
        return None

    result = tasks_collection.update_one(query_filter, {'$set': update_data}) 
    
    if result.matched_count == 0:
        return None 

    updated_task = tasks_collection.find_one({'_id': obj_id})
    if updated_task:
        updated_task['_id'] = str(updated_task['_id'])
        
    return updated_task

def delete_task(task_id, user_id):
    
    try:
        obj_id = ObjectId(task_id) 
    except Exception:
        return False 

    query_filter = {'_id': obj_id, 'user_id': user_id}
    result = tasks_collection.delete_one(query_filter) 
    return result.deleted_count > 0 