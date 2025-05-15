import os
import pymongo
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

load_dotenv()

def get_db_connection():
    """
    Establece y retorna una conexión a MongoDB Atlas
    utilizando las credenciales almacenadas en variables de entorno
    """
    try:
        mongo_uri = os.getenv("MONGO_URI")
        
        if not mongo_uri:
            raise ValueError("No se encontró la variable de entorno MONGO_URI")
        
        # Crear cliente de MongoDB
        client = pymongo.MongoClient(mongo_uri)
        
        # Verificar la conexión
        client.admin.command('ping')
        print("Conexión a MongoDB Atlas establecida correctamente")
        
        db_name = os.getenv("DB_NAME", "nutriplan")
        
        return client[db_name]
        
    except ConnectionFailure as e:
        print(f"Error de conexión a MongoDB Atlas: {e}")
        raise
    except Exception as e:
        print(f"Error al conectar a MongoDB Atlas: {e}")
        raise 
    
#Exportar bd
db = get_db_connection()