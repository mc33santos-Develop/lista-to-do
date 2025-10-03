
from flask import Flask, request, jsonify
from flask_cors import CORS
import database


app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

@app.route('/todolist', methods=['GET'])
def get_tasks():
    tasks = database.get_all_tasks()
    return jsonify(tasks), 200

@app.route('/todolist', methods=['POST'])
def create_task():
    data = request.get_json()

    
    if not data or 'titulo' not in data:
        return jsonify({'error': 'O campo "titulo" é obrigatório'}), 400
    
    new_task_data = {
        "titulo": data['titulo'],
        "concluido": False  
    }
    
    created_task = database.add_task(new_task_data)
    return jsonify(created_task), 201

@app.route('/todolist/<string:task_id>', methods=['PUT'])
def modify_task(task_id):
    data = request.get_json()
    updated_task = database.update_task(task_id, data)
    
    if updated_task is None:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
        
    return jsonify(updated_task), 200

@app.route('/todolist/<string:task_id>', methods=['DELETE'])
def remove_task(task_id):
    was_deleted = database.delete_task(task_id)
    
    if not was_deleted:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
        

    return jsonify({"message": "Tarefa deletada com sucesso"}), 200


if __name__ == '__main__':
    app.run(debug=True)