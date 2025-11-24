"""
Serviço de Sessão
Responsável por salvar informações legíveis das sessões no MongoDB.
"""
from datetime import datetime, timedelta
from database import db
from typing import Optional, Dict


class SessionService:
    """
    Serviço para gerenciar informações legíveis de sessões no MongoDB.
    Armazena email, data de criação, atualização e expiração de forma legível.
    """
    COLLECTION_NAME = 'sessions_info'

    @staticmethod
    def get_collection():
        """Retorna a coleção de informações de sessão."""
        return db.get_collection(SessionService.COLLECTION_NAME)

    @staticmethod
    def create_session_info(session_id: str, email: str, user_id: str, expiration_minutes: int = 31) -> Dict:
        """
        Cria informações legíveis de uma sessão no MongoDB.
        
        Args:
            session_id: ID da sessão do Flask
            email: Email do usuário
            user_id: ID do usuário
            expiration_minutes: Minutos até a expiração (padrão: 31 minutos)
            
        Returns:
            Dicionário com informações da sessão criada
        """
        now = datetime.utcnow()
        expiration = now + timedelta(minutes=expiration_minutes)
        
        session_info = {
            'session_id': session_id,
            'email': email,
            'user_id': user_id,
            'created_at': now,
            'updated_at': now,
            'expires_at': expiration,
            'is_active': True
        }
        
        collection = SessionService.get_collection()
        collection.insert_one(session_info)
        
        print(f"[OK] Informacoes de sessao salvas: {email} (ID: {session_id[:20]}...)")
        return session_info

    @staticmethod
    def update_session_info(session_id: str) -> bool:
        """
        Atualiza a data de atualização de uma sessão.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            True se atualizado com sucesso, False caso contrário
        """
        collection = SessionService.get_collection()
        result = collection.update_one(
            {'session_id': session_id, 'is_active': True},
            {'$set': {'updated_at': datetime.utcnow()}}
        )
        return result.modified_count > 0

    @staticmethod
    def deactivate_session(session_id: str) -> bool:
        """
        Desativa uma sessão (logout).
        
        Args:
            session_id: ID da sessão
            
        Returns:
            True se desativado com sucesso, False caso contrário
        """
        collection = SessionService.get_collection()
        result = collection.update_one(
            {'session_id': session_id},
            {'$set': {'is_active': False, 'updated_at': datetime.utcnow()}}
        )
        return result.modified_count > 0

    @staticmethod
    def get_session_info(session_id: str) -> Optional[Dict]:
        """
        Busca informações de uma sessão.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            Dicionário com informações da sessão ou None se não encontrado
        """
        collection = SessionService.get_collection()
        session_info = collection.find_one({'session_id': session_id})
        
        if session_info:
            # Converte ObjectId e datetime para strings legíveis
            session_info['_id'] = str(session_info['_id'])
            if isinstance(session_info.get('created_at'), datetime):
                session_info['created_at'] = session_info['created_at'].isoformat()
            if isinstance(session_info.get('updated_at'), datetime):
                session_info['updated_at'] = session_info['updated_at'].isoformat()
            if isinstance(session_info.get('expires_at'), datetime):
                session_info['expires_at'] = session_info['expires_at'].isoformat()
        
        return session_info

    @staticmethod
    def get_all_active_sessions() -> list:
        """
        Retorna todas as sessões ativas.
        
        Returns:
            Lista de sessões ativas
        """
        collection = SessionService.get_collection()
        sessions = list(collection.find({'is_active': True}).sort('created_at', -1))
        
        # Converte para formato legível
        for session in sessions:
            session['_id'] = str(session['_id'])
            if isinstance(session.get('created_at'), datetime):
                session['created_at'] = session['created_at'].isoformat()
            if isinstance(session.get('updated_at'), datetime):
                session['updated_at'] = session['updated_at'].isoformat()
            if isinstance(session.get('expires_at'), datetime):
                session['expires_at'] = session['expires_at'].isoformat()
        
        return sessions

