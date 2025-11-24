"""
Serviço de Tokens de Autenticação
Responsável por gerenciar tokens persistentes para login automático.
"""
import secrets
from datetime import datetime, timedelta
from database import db
from typing import Optional, Dict


class TokenService:
    """
    Serviço para gerenciar tokens de autenticação persistente.
    Tokens permitem login automático sem necessidade de senha.
    """
    COLLECTION_NAME = 'auth_tokens'

    @staticmethod
    def get_collection():
        """Retorna a coleção de tokens."""
        return db.get_collection(TokenService.COLLECTION_NAME)

    @staticmethod
    def create_token(user_id: str, email: str, days_valid: int = 30) -> str:
        """
        Cria um novo token de autenticação para o usuário.
        
        Args:
            user_id: ID do usuário
            email: Email do usuário
            days_valid: Dias de validade do token (padrão: 30 dias)
            
        Returns:
            Token gerado
        """
        # Gera um token único e seguro
        token = secrets.token_urlsafe(32)
        
        expires_at = datetime.utcnow() + timedelta(days=days_valid)
        
        token_data = {
            'token': token,
            'user_id': user_id,
            'email': email,
            'created_at': datetime.utcnow(),
            'expires_at': expires_at,
            'is_active': True
        }
        
        collection = TokenService.get_collection()
        collection.insert_one(token_data)
        
        print(f"[OK] Token criado para usuario: {email} (valido por {days_valid} dias)")
        return token

    @staticmethod
    def validate_token(token: str) -> Optional[Dict]:
        """
        Valida um token e retorna informações do usuário se válido.
        
        Args:
            token: Token a ser validado
            
        Returns:
            Dicionário com informações do usuário ou None se inválido
        """
        collection = TokenService.get_collection()
        token_doc = collection.find_one({
            'token': token,
            'is_active': True
        })
        
        if not token_doc:
            return None
        
        # Verifica se o token não expirou
        expires_at = token_doc.get('expires_at')
        if isinstance(expires_at, datetime):
            if datetime.utcnow() > expires_at:
                # Marca o token como inativo
                collection.update_one(
                    {'_id': token_doc['_id']},
                    {'$set': {'is_active': False}}
                )
                return None
        
        # Atualiza a última data de uso
        collection.update_one(
            {'_id': token_doc['_id']},
            {'$set': {'last_used_at': datetime.utcnow()}}
        )
        
        return {
            'user_id': token_doc['user_id'],
            'email': token_doc['email']
        }

    @staticmethod
    def revoke_token(token: str) -> bool:
        """
        Revoga um token (torna inativo).
        
        Args:
            token: Token a ser revogado
            
        Returns:
            True se revogado com sucesso, False caso contrário
        """
        collection = TokenService.get_collection()
        result = collection.update_one(
            {'token': token},
            {'$set': {'is_active': False, 'revoked_at': datetime.utcnow()}}
        )
        return result.modified_count > 0

    @staticmethod
    def revoke_all_user_tokens(user_id: str) -> int:
        """
        Revoga todos os tokens de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Número de tokens revogados
        """
        collection = TokenService.get_collection()
        result = collection.update_many(
            {'user_id': user_id, 'is_active': True},
            {'$set': {'is_active': False, 'revoked_at': datetime.utcnow()}}
        )
        return result.modified_count

