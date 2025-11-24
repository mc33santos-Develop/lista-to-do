"""
Modelo de Tarefa
"""
from typing import Optional, Dict, List
from bson import ObjectId
from database import db


class Task:
    """
    Modelo para representar uma tarefa no sistema.
    Responsável por operações relacionadas a tarefas no banco de dados.
    """
    COLLECTION_NAME = 'todos'

    def __init__(self, text: str, done: bool = False, user_id: str = None, task_id: str = None):
        self.text = text
        self.done = done
        self.user_id = user_id
        self._id = task_id

    @property
    def collection(self):
        """Retorna a coleção de tarefas."""
        return db.get_collection(self.COLLECTION_NAME)

    @classmethod
    def find_by_id(cls, task_id: str, user_id: str) -> Optional['Task']:
        """
        Busca uma tarefa pelo ID e verifica se pertence ao usuário.
        
        Args:
            task_id: ID da tarefa
            user_id: ID do usuário
            
        Returns:
            Instância de Task ou None se não encontrado
        """
        try:
            obj_id = ObjectId(task_id)
        except Exception:
            return None

        collection = db.get_collection(cls.COLLECTION_NAME)
        task_doc = collection.find_one({'_id': obj_id, 'user_id': user_id})
        
        if task_doc:
            return cls(
                text=task_doc['text'],
                done=task_doc.get('done', False),
                user_id=task_doc.get('user_id'),
                task_id=str(task_doc['_id'])
            )
        return None

    @classmethod
    def find_all_by_user(cls, user_id: str) -> List['Task']:
        """
        Busca todas as tarefas de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Lista de instâncias de Task
        """
        collection = db.get_collection(cls.COLLECTION_NAME)
        cursor = collection.find({'user_id': user_id})
        
        tasks = []
        for task_doc in cursor:
            tasks.append(cls(
                text=task_doc['text'],
                done=task_doc.get('done', False),
                user_id=task_doc.get('user_id'),
                task_id=str(task_doc['_id'])
            ))
        return tasks

    def save(self) -> str:
        """
        Salva a tarefa no banco de dados.
        
        Returns:
            ID da tarefa criada
        """
        task_data = {
            'text': self.text,
            'done': self.done,
            'user_id': self.user_id
        }
        
        result = self.collection.insert_one(task_data)
        self._id = str(result.inserted_id)
        return self._id

    def update(self, text: str = None, done: bool = None) -> bool:
        """
        Atualiza a tarefa no banco de dados.
        
        Args:
            text: Novo texto da tarefa (opcional)
            done: Novo status da tarefa (opcional)
            
        Returns:
            True se atualizado com sucesso, False caso contrário
        """
        if not self._id:
            return False

        try:
            obj_id = ObjectId(self._id)
        except Exception:
            return False

        update_data = {}
        if text is not None:
            self.text = text
            update_data['text'] = text
        if done is not None:
            self.done = done
            update_data['done'] = done

        if not update_data:
            return False

        query_filter = {'_id': obj_id, 'user_id': self.user_id}
        result = self.collection.update_one(query_filter, {'$set': update_data})
        return result.matched_count > 0

    def delete(self) -> bool:
        """
        Deleta a tarefa do banco de dados.
        
        Returns:
            True se deletado com sucesso, False caso contrário
        """
        if not self._id:
            return False

        try:
            obj_id = ObjectId(self._id)
        except Exception:
            return False

        query_filter = {'_id': obj_id, 'user_id': self.user_id}
        result = self.collection.delete_one(query_filter)
        return result.deleted_count > 0

    def to_dict(self) -> Dict:
        """Converte a tarefa para dicionário."""
        return {
            '_id': self._id,
            'text': self.text,
            'done': self.done
        }

