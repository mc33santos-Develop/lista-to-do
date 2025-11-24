"""
Rotas de Autenticação
Gerencia todas as rotas relacionadas a autenticação de usuários.
"""
from flask import Blueprint, request, jsonify, session
from services.auth_service import AuthService
from services.session_service import SessionService
from services.token_service import TokenService
from database import db

# Cria um Blueprint para as rotas de autenticação
auth_bp = Blueprint('auth', __name__, url_prefix='/todos')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Rota de cadastro de novo usuário.
    
    Body:
        {
            "email": "usuario@email.com",
            "password": "senha123"
        }
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400
    
    user_id = AuthService.create_user(email, password)
    
    if user_id is None:
        return jsonify({'error': 'Usuário já existe'}), 409
    
    return jsonify({
        'message': 'Usuário cadastrado com sucesso!',
        'user_id': user_id
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Rota de login - autentica um usuário e cria uma sessão.
    
    Body:
        {
            "email": "usuario@email.com",
            "password": "senha123",
            "remember_me": true (opcional)
        }
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    remember_me = data.get('remember_me', False)

    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400

    user_id = AuthService.authenticate(email, password)
    
    if user_id is None:
        return jsonify({'error': 'Email ou senha inválidos'}), 401

    user = AuthService.get_user_by_email(email)
    
    # Cria a sessão do Flask
    session['user'] = {'email': user['email'], '_id': user['_id']}
    session.permanent = True
    
    # Marca para salvar informações legíveis após a resposta
    from flask import g
    g._save_session_info = {
        'email': user['email'],
        'user_id': user['_id']
    }
    
    response_data = {
        'message': 'Acesso Permitido!',
        'user_id': user['_id']
    }
    
    # Se "Lembrar-me" estiver marcado, cria um token persistente
    if remember_me:
        token = TokenService.create_token(user['_id'], user['email'])
        response_data['token'] = token
        print(f"[OK] Token de autenticacao criado para: {user['email']}")
    
    print(f"[OK] Usuario autenticado! Sessao criada para: {user['email']}")
    return jsonify(response_data), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Rota de logout - encerra a sessão do usuário.
    Também revoga o token se fornecido.
    
    Body (opcional):
        {
            "token": "token_do_usuario"
        }
    """
    data = request.get_json() or {}
    token = data.get('token')
    
    # Se houver token, revoga ele
    if token:
        TokenService.revoke_token(token)
    
    if 'user' in session:
        # Obtém o ID da sessão antes de remover
        try:
            sessions_collection = db.get_collection('sessions')
            latest_session = sessions_collection.find_one(
                {},
                sort=[('_id', -1)]
            )
            if latest_session:
                session_id = latest_session.get('id', '')
                if session_id.startswith('session:'):
                    session_id = session_id.replace('session:', '')
                SessionService.deactivate_session(session_id)
        except Exception as e:
            print(f"[ERRO] Falha ao desativar sessao: {e}")
        
        session.pop('user', None)
        return jsonify({'message': 'Logout bem-sucedido'}), 200
    return jsonify({'error': 'Nenhuma sessão ativa'}), 400


@auth_bp.route('/session', methods=['GET'])
def check_session():
    """
    Rota para verificar se há uma sessão ativa.
    Útil para o frontend verificar o status de autenticação.
    """
    if 'user' in session:
        return jsonify({
            'logged_in': True,
            'user': session['user']
        }), 200
    return jsonify({'logged_in': False}), 401


@auth_bp.route('/sessions', methods=['GET'])
def get_all_sessions():
    """
    Rota para listar todas as sessões ativas (com informações legíveis).
    Útil para visualizar sessões no MongoDB Compass.
    """
    sessions = SessionService.get_all_active_sessions()
    return jsonify({
        'total': len(sessions),
        'sessions': sessions
    }), 200


@auth_bp.route('/auto-login', methods=['POST'])
def auto_login():
    """
    Rota para login automático usando token.
    Restaura a sessão do usuário se o token for válido.
    
    Body:
        {
            "token": "token_do_usuario"
        }
    """
    data = request.get_json()
    token = data.get('token') if data else None

    if not token:
        return jsonify({'error': 'Token é obrigatório'}), 400

    # Valida o token
    user_info = TokenService.validate_token(token)
    
    if user_info is None:
        return jsonify({'error': 'Token inválido ou expirado'}), 401

    # Restaura a sessão
    session['user'] = {
        'email': user_info['email'],
        '_id': user_info['user_id']
    }
    session.permanent = True
    
    # Marca para salvar informações legíveis após a resposta
    from flask import g
    g._save_session_info = {
        'email': user_info['email'],
        'user_id': user_info['user_id']
    }
    
    print(f"[OK] Login automatico realizado para: {user_info['email']}")
    return jsonify({
        'message': 'Login automático realizado com sucesso!',
        'user_id': user_info['user_id'],
        'user': {
            'email': user_info['email'],
            '_id': user_info['user_id']
        }
    }), 200

