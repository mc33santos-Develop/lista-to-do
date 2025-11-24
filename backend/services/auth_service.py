"""
Serviço de Autenticação
Responsável pela lógica de negócio relacionada a autenticação de usuários.
"""
from typing import Optional, Dict
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User


class AuthService:
    """
    Serviço responsável por operações de autenticação.
    Separa a lógica de negócio das rotas e modelos.
    """

    @staticmethod
    def create_user(email: str, password: str) -> Optional[str]:
        """
        Cria um novo usuário no sistema.
        
        Args:
            email: Email do usuário
            password: Senha do usuário (será hasheada)
            
        Returns:
            ID do usuário criado ou None se o email já existe
        """
        # Verifica se o usuário já existe
        existing_user = User.find_by_email(email)
        if existing_user:
            return None

        # Cria hash da senha
        password_hash = generate_password_hash(password)
        
        # Cria e salva o usuário
        user = User(email=email, password_hash=password_hash)
        user_id = user.save()
        
        if user_id:
            print(f"[OK] Usuario criado com sucesso! ID: {user_id}")
        
        return user_id

    @staticmethod
    def authenticate(email: str, password: str) -> Optional[str]:
        """
        Autentica um usuário verificando email e senha.
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            
        Returns:
            ID do usuário se autenticado com sucesso, None caso contrário
        """
        user = User.find_by_email(email)
        
        if user and user.password_hash:
            if check_password_hash(user.password_hash, password):
                return user._id
        
        return None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict]:
        """
        Busca um usuário pelo email e retorna seus dados (sem senha).
        
        Args:
            email: Email do usuário
            
        Returns:
            Dicionário com dados do usuário ou None se não encontrado
        """
        user = User.find_by_email(email)
        if user:
            return user.to_dict()
        return None

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[Dict]:
        """
        Busca um usuário pelo ID e retorna seus dados (sem senha).
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Dicionário com dados do usuário ou None se não encontrado
        """
        user = User.find_by_id(user_id)
        if user:
            return user.to_dict()
        return None

