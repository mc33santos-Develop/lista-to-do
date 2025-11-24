"""
Modelo de Usuário
"""
from typing import Optional, Dict
from bson import ObjectId
from database import db


class User:
    """
    Modelo para representar um usuário no sistema.
    Responsável por operações relacionadas a usuários no banco de dados.
    """
    COLLECTION_NAME = 'users'

    def __init__(self, email: str, password_hash: str = None, user_id: str = None):
        self.email = email
        self.password_hash = password_hash
        self._id = user_id

    @property
    def collection(self):
        """Retorna a coleção de usuários."""
        return db.get_collection(self.COLLECTION_NAME)

    @classmethod
    def find_by_email(cls, email: str) -> Optional['User']:
        """
        Busca um usuário pelo email.
        
        Args:
            email: Email do usuário
            
        Returns:
            Instância de User ou None se não encontrado
        """
        collection = db.get_collection(cls.COLLECTION_NAME)
        user_doc = collection.find_one({'email': email})
        
        if user_doc:
            return cls(
                email=user_doc['email'],
                password_hash=user_doc.get('password'),
                user_id=str(user_doc['_id'])
            )
        return None

    @classmethod
    def find_by_id(cls, user_id: str) -> Optional['User']:
        """
        Busca um usuário pelo ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Instância de User ou None se não encontrado
        """
        try:
            obj_id = ObjectId(user_id)
        except Exception:
            return None

        collection = db.get_collection(cls.COLLECTION_NAME)
        user_doc = collection.find_one({'_id': obj_id})
        
        if user_doc:
            return cls(
                email=user_doc['email'],
                password_hash=user_doc.get('password'),
                user_id=str(user_doc['_id'])
            )
        return None

    def exists(self) -> bool:
        """Verifica se o usuário já existe no banco de dados."""
        return self.collection.find_one({'email': self.email}) is not None

    def save(self) -> Optional[str]:
        """
        Salva o usuário no banco de dados.
        
        Returns:
            ID do usuário criado ou None se já existir
        """
        if self.exists():
            return None

        user_data = {
            'email': self.email,
            'password': self.password_hash
        }
        
        result = self.collection.insert_one(user_data)
        self._id = str(result.inserted_id)
        return self._id

    def to_dict(self) -> Dict:
        """Converte o usuário para dicionário (sem senha)."""
        return {
            '_id': self._id,
            'email': self.email
        }

