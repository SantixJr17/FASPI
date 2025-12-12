from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from .modelo import modelo
from .db.database import engine, Base
from .routers import (
    users, products, animals, breeds, 
    medical_records, reproduction, production, 
    weight_records, events
)

# --- Configuración Inicial y Creación de Tablas ---
# Crea las tablas en la base de datos (solo si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Control Ganadero - FastAPI",
    description="Sistema completo de gestión ganadera con autenticación JWT, control de animales, registros médicos, reproducción, producción y eventos.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Personalizar el esquema OpenAPI para limpiar la documentación
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Limpiar respuestas 422 automáticas de la documentación visual
    # (se mantienen funcionalmente pero se minimizan en la UI)
    for path, path_item in openapi_schema.get("paths", {}).items():
        for method, operation in path_item.items():
            if isinstance(operation, dict) and "responses" in operation:
                # Mantener solo las respuestas documentadas explícitamente
                # El 422 seguirá funcionando pero no será tan prominente
                if "422" in operation["responses"]:
                    # Hacer que el 422 sea menos visible pero funcional
                    operation["responses"]["422"]["description"] = "Error de validación de datos"
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# --- Registro de Routers ---
# Autenticación y usuarios
app.include_router(users.router)
# Productos (ejemplo original)
app.include_router(products.router)
# Módulos del sistema ganadero
app.include_router(animals.router)
app.include_router(breeds.router)
app.include_router(medical_records.router)
app.include_router(reproduction.router)
app.include_router(production.router)
app.include_router(weight_records.router)
app.include_router(events.router)


# Endpoint de bienvenida
@app.get("/")
def read_root():
    return {
        "message": "Sistema de Control Ganadero API",
        "version": "1.0.0",
        "endpoints": {
            "documentation": "/docs",
            "users": "/users",
            "animals": "/animals",
            "breeds": "/breeds",
            "medical_records": "/medical-records",
            "reproductions": "/reproductions",
            "productions": "/productions",
            "weight_records": "/weight-records",
            "events": "/events"
        }
    }