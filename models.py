from pydantic import BaseModel
from typing import Optional

# Definimos cómo es un "Animal Perdido" en nuestra app usando Pydantic
class Animal(BaseModel):
    nombre: Optional[str] = None  # El nombre puede ser opcional si es callejero
    especie: str                  # Ej: Perro, Gato... (Obligatorio)
    raza: Optional[str] = None
    descripcion: str              # Detalles de cómo es
    ubicacion: str                # Dónde se perdió
    estado: str = "Perdido"       # Por defecto estará "Perdido"