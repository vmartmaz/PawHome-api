from fastapi import FastAPI

# Inicializamos la aplicación
app = FastAPI(
    title="API Búsqueda de Animales",
    description="API para la gestión de grupos de búsqueda de mascotas perdidas",
    version="1.0.0"
)

# Ruta base de prueba
@app.get("/")
async def root():
    return {"mensaje": "¡Bienvenido a la API de Búsqueda de Animales!"}