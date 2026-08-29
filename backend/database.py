from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "tasks_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "tasks")

try:
    client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=2000)
    # Testar conexão
    client.admin.command('ping')
    print("✅ Conectado ao MongoDB")
except Exception as e:
    print(f"❌ Erro ao conectar ao MongoDB: {e}")
    raise

db = client[DATABASE_NAME]
tasks_collection = db[COLLECTION_NAME]

# Exportar client para operações de admin (como health check)
__all__ = ['client', 'db', 'tasks_collection']
