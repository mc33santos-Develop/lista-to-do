"""
Serviço de Tarefas
Responsável pela lógica de negócio relacionada a tarefas.
"""
from typing import Optional, Dict, List
from models.task import Task


class TaskService:
    """
    Serviço responsável por operações de tarefas.
    Separa a lógica de negócio das rotas e modelos.
    """

    @staticmethod
    def get_all_tasks(user_id: str) -> List[Dict]:
        """
        Recupera todas as tarefas de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Lista de tarefas em formato de dicionário
        """
        tasks = Task.find_all_by_user(user_id)
        return [task.to_dict() for task in tasks]

    @staticmethod
    def create_task(text: str, user_id: str) -> Dict:
        """
        Cria uma nova tarefa.
        
        Args:
            text: Texto da tarefa
            user_id: ID do usuário
            
        Returns:
            Tarefa criada em formato de dicionário
        """
        task = Task(text=text, done=False, user_id=user_id)
        task_id = task.save()
        task._id = task_id
        return task.to_dict()

    @staticmethod
    def update_task(task_id: str, user_id: str, text: str = None, done: bool = None) -> Optional[Dict]:
        """
        Atualiza uma tarefa existente.
        
        Args:
            task_id: ID da tarefa
            user_id: ID do usuário
            text: Novo texto da tarefa (opcional)
            done: Novo status da tarefa (opcional)
            
        Returns:
            Tarefa atualizada em formato de dicionário ou None se não encontrada
        """
        task = Task.find_by_id(task_id, user_id)
        
        if not task:
            return None

        # Atualiza apenas os campos fornecidos
        update_text = text if text is not None else task.text
        update_done = done if done is not None else task.done
        
        success = task.update(text=update_text, done=update_done)
        
        if success:
            return task.to_dict()
        return None

    @staticmethod
    def delete_task(task_id: str, user_id: str) -> bool:
        """
        Deleta uma tarefa.
        
        Args:
            task_id: ID da tarefa
            user_id: ID do usuário
            
        Returns:
            True se deletado com sucesso, False caso contrário
        """
        task = Task.find_by_id(task_id, user_id)
        
        if not task:
            return False

        return task.delete()

