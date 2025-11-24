"""
Rotas de Tarefas
Gerencia todas as rotas relacionadas a tarefas.
"""
from flask import Blueprint, request, jsonify, session
from middleware.auth_middleware import require_auth
from services.task_service import TaskService

# Cria um Blueprint para as rotas de tarefas
task_bp = Blueprint('tasks', __name__, url_prefix='/todos')


@task_bp.route('', methods=['GET'])
@require_auth
def get_tasks():
    """
    Rota para recuperar todas as tarefas do usuário logado.
    Requer autenticação.
    """
    user_id = session['user']['_id']
    tasks = TaskService.get_all_tasks(user_id)
    return jsonify(tasks), 200


@task_bp.route('', methods=['POST'])
@require_auth
def create_task():
    """
    Rota para criar uma nova tarefa.
    Requer autenticação.
    
    Body:
        {
            "text": "Texto da tarefa"
        }
    """
    user_id = session['user']['_id']
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'O campo "text" é obrigatório'}), 400
    
    created_task = TaskService.create_task(data['text'], user_id)
    return jsonify(created_task), 201


@task_bp.route('/<string:task_id>', methods=['PUT'])
@require_auth
def modify_task(task_id):
    """
    Rota para atualizar uma tarefa existente.
    Requer autenticação.
    
    Body:
        {
            "text": "Novo texto" (opcional),
            "done": true/false (opcional)
        }
    """
    user_id = session['user']['_id']
    data = request.get_json()
    
    text = data.get('text') if data else None
    done = data.get('done') if data else None
    
    updated_task = TaskService.update_task(task_id, user_id, text=text, done=done)
    
    if updated_task is None:
        return jsonify({
            'error': 'Tarefa não encontrada ou não pertence ao usuário'
        }), 404
    
    return jsonify(updated_task), 200


@task_bp.route('/<string:task_id>', methods=['DELETE'])
@require_auth
def remove_task(task_id):
    """
    Rota para deletar uma tarefa.
    Requer autenticação.
    """
    user_id = session['user']['_id']
    was_deleted = TaskService.delete_task(task_id, user_id)
    
    if not was_deleted:
        return jsonify({
            'error': 'Tarefa não encontrada ou não pertence ao usuário'
        }), 404
    
    return jsonify({"message": "Tarefa deletada com sucesso"}), 200

