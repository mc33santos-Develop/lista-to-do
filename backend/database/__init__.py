"""
Módulo de banco de dados - Singleton para conexão MongoDB
"""
from .connection import DatabaseConnection

# Exporta a instância única do banco de dados
db = DatabaseConnection.get_instance()

