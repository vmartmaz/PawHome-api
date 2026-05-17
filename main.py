import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Importamos el modelo de datos desde el archivo models.py
from models import Animal

# Cargamos las variables del archivo .env
load_dotenv()

# Variables globales para la conexión a la base de datos
client = None
db = None

# Gestiona el ciclo de vida de la API (Conexión y desconexión automática)
@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db
    # 1. Al arrancar: Conexión con MongoDB Atlas
    mongo_url = os.getenv("MONGODB_URL")
    client = AsyncIOMotorClient(mongo_url)
    db = client.pawhome_db  # Nombre de la base de datos
    print("¡Conectado a MongoDB exitosamente!")
    
    # AÑADE ESTA LÍNEA PARA VER QUÉ ESTÁ LEYENDO:
    print(f"---- URL QUE ESTOY USANDO: {mongo_url} ----")
    yield  # Aquí la API se queda escuchando peticiones
    
    # 2. Al apagar: Cerramos la conexión de forma segura
    client.close()
    print("Conexión con MongoDB cerrada.")

# Inicializamos FastAPI con la configuración de ciclo de vida
app = FastAPI(
    lifespan=lifespan,
    title="PawHome API",
    description="API para la gestión de grupos de búsqueda de mascotas perdidas",
    version="1.0.0"
)

# ----------------------------------------------------
# RUTAS DE NUESTRA API (ENDPOINTS)
# ----------------------------------------------------

# 1. Ruta Base de Bienvenida
@app.get("/")
async def root():
    return {"mensaje": "¡Bienvenido a la API de PawHome!"}


# 2. Ruta POST: Para registrar un nuevo animal perdido
@app.post("/animales/")
async def registrar_animal_perdido(animal: Animal):
    # Convertimos el objeto que nos llega de la app a un diccionario de Python
    animal_dict = animal.model_dump()
    
    # Lo guardamos dentro de la colección "animales" en MongoDB Atlas
    resultado = await db["animales"].insert_one(animal_dict)
    
    # Devolvemos un mensaje de éxito con el ID único que MongoDB le ha asignado
    return {
        "mensaje": "Animal registrado correctamente en la base de datos", 
        "id": str(resultado.inserted_id)
    }


# 3. Ruta GET: Para obtener la lista de todos los animales perdidos
@app.get("/animales/")
async def obtener_animales_perdidos():
    lista_animales = []
    
    # Buscamos todos los documentos ({}) en la colección "animales"
    cursor = db["animales"].find({})
    
    # Recorremos los datos que nos trae MongoDB de forma asíncrona
    async for documento in cursor:
        # MongoDB genera un ID especial tipo ObjectId que da error al enviarlo por internet.
        # Lo convertimos a un texto (string) normal para que la app Android lo entienda bien.
        documento["_id"] = str(documento["_id"])
        lista_animales.append(documento)
        
    return lista_animales