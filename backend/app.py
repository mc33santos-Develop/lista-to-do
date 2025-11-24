from flask import Flask, g
from flask_cors import CORS
from flask_session import Session
from config import Config
from routes import auth_bp, task_bp
from services.session_service import SessionService
from database import db


def create_app():
    """
    Factory function para criar a aplicação Flask.
    Facilita testes e configuração de diferentes ambientes.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuração de sessão
    Session(app)

    # Configuração de CORS
    CORS(
        app,
        resources={r"/todos/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"]
        }},
        supports_credentials=True
    )

    # Hook para salvar informações legíveis da sessão após o login
    @app.after_request
    def save_session_info(response):
        """Salva informações legíveis da sessão após cada requisição."""
        from flask import session as flask_session
        
        # Verifica se há informações para salvar (definido no login)
        if hasattr(g, '_save_session_info'):
            try:
                # Obtém o ID da sessão do MongoDB
                # O flask-session salva com o formato: "session:{session_id}"
                sessions_collection = db.get_collection('sessions')
                
                # Busca a última sessão criada (ordenada por _id descendente)
                latest_session = sessions_collection.find_one(
                    {},
                    sort=[('_id', -1)]
                )
                
                if latest_session:
                    session_id = latest_session.get('id', '')
                    # Remove o prefixo "session:" se existir
                    if session_id.startswith('session:'):
                        session_id = session_id.replace('session:', '')
                    
                    # Salva informações legíveis
                    SessionService.create_session_info(
                        session_id=session_id,
                        email=g._save_session_info['email'],
                        user_id=g._save_session_info['user_id']
                    )
                    
                    # Remove a flag para não salvar novamente
                    delattr(g, '_save_session_info')
            except Exception as e:
                print(f"[ERRO] Falha ao salvar info de sessao: {e}")
        
        # Atualiza a data de atualização se houver uma sessão ativa
        if 'user' in flask_session:
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
                    SessionService.update_session_info(session_id)
            except Exception as e:
                # Ignora erros silenciosamente para não afetar requisições
                pass
        
        return response

    # Registra os Blueprints (rotas)
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app


# Cria a instância da aplicação
app = create_app()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
