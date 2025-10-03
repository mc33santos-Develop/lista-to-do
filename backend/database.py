from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('mongodb://localhost:27017/')


db = client['todolist']


tasks_collection = db['todolist']

def get_all_tasks():
    tasks = []
    for task in tasks_collection.find():
        task['_id'] = str(task['_id'])
        tasks.append(task)
    return tasks

def add_task(data):
    result = tasks_collection.insert_one(data)
    new_task = tasks_collection.find_one({'_id': result.inserted_id})
    if new_task:
        new_task['_id'] = str(new_task['_id'])
    return new_task

def update_task(task_id, data):
    try:
        obj_id = ObjectId(task_id)
    except Exception:
        return None 

    tasks_collection.update_one({'_id': obj_id}, {'$set': data})
    
    updated_task = tasks_collection.find_one({'_id': obj_id})
    if updated_task:
        updated_task['_id'] = str(updated_task['_id'])
        
    return updated_task

def delete_task(task_id):
    try:
        obj_id = ObjectId(task_id)
    except Exception:
        return False 

    result = tasks_collection.delete_one({'_id': obj_id})
    return result.deleted_count > 0