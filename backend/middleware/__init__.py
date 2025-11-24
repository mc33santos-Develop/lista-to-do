"""
Middlewares da aplicação
"""
from .auth_middleware import require_auth

__all__ = ['require_auth']

