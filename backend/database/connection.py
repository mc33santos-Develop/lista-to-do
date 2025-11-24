"""
Singleton para gerenciar a conexão com MongoDB.
Garante que apenas uma instância de conexão seja criada.
"""
from pymongo import MongoClient
from config import Config


class DatabaseConnection:
    """
    Singleton para conexão MongoDB.
    Garante uma única instância de conexão em toda a aplicação.
    """
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        """Cria uma única instância do DatabaseConnection."""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa a conexão com MongoDB."""
        if self._client is None:
            self._client = MongoClient(Config.MONGO_URI)
            self._db = self._client[Config.DB_NAME]
            print(f"[OK] Conexao MongoDB estabelecida: {Config.DB_NAME}")

    @classmethod
    def get_instance(cls):
        """Retorna a instância única do DatabaseConnection."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def client(self):
        """Retorna o cliente MongoDB."""
        return self._client

    @property
    def db(self):
        """Retorna o banco de dados."""
        return self._db

    def get_collection(self, collection_name):
        """Retorna uma coleção específica do banco de dados."""
        return self._db[collection_name]

    def close(self):
        """Fecha a conexão com MongoDB."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("[OK] Conexao MongoDB fechada")

