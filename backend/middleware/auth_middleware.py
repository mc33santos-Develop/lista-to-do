"""
Middleware de Autenticação
Decorador para proteger rotas que requerem autenticação.
"""
from functools import wraps
from flask import session, jsonify


def require_auth(f):
    """
    Decorador para proteger rotas que requerem autenticação.
    Verifica se há uma sessão ativa antes de executar a rota.
    
    Usage:
        @app.route('/protected')
        @require_auth
        def protected_route():
            user_id = session['user']['_id']
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Não autorizado'}), 401
        return f(*args, **kwargs)
    return decorated_function

