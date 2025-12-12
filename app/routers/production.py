from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..crud import crud
from ..schemas import schemas
from ..db.database import get_db

router = APIRouter(
    prefix="/productions",
    tags=["Producción"],
)

@router.post(
    "/", 
    response_model=schemas.Production, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear registro de producción",
    description="Crea un nuevo registro de producción para un animal."
)
def create_production(
    production: schemas.ProductionCreate,
    db: Session = Depends(get_db)
):
    # Verificar que el animal existe
    animal = crud.get_animal(db, production.animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return crud.create_production(db=db, production=production)

@router.get(
    "/", 
    response_model=List[schemas.Production],
    summary="Listar registros de producción",
    description="Obtiene una lista de todos los registros de producción con opción de filtrado por animal."
)
def read_productions(
    skip: int = 0,
    limit: int = 100,
    animal_id: Optional[int] = Query(None, description="Filtrar por ID de animal"),
    db: Session = Depends(get_db)
):
    productions = crud.get_productions(db, skip=skip, limit=limit, animal_id=animal_id)
    return productions

@router.get(
    "/{production_id}", 
    response_model=schemas.Production,
    summary="Obtener registro de producción por ID",
    description="Obtiene la información completa de un registro de producción específico por su ID."
)
def read_production(production_id: int, db: Session = Depends(get_db)):
    db_production = crud.get_production(db, production_id=production_id)
    if db_production is None:
        raise HTTPException(status_code=404, detail="Registro de producción no encontrado")
    return db_production

@router.put(
    "/{production_id}", 
    response_model=schemas.Production,
    summary="Actualizar registro de producción",
    description="Actualiza la información de un registro de producción existente."
)
def update_production(
    production_id: int,
    production: schemas.ProductionUpdate,
    db: Session = Depends(get_db)
):
    db_production = crud.get_production(db, production_id)
    if db_production is None:
        raise HTTPException(status_code=404, detail="Registro de producción no encontrado")
    return crud.update_production(db, production_id, production)

@router.delete(
    "/{production_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar registro de producción",
    description="Elimina un registro de producción del sistema."
)
def delete_production(
    production_id: int,
    db: Session = Depends(get_db)
):
    db_production = crud.get_production(db, production_id)
    if db_production is None:
        raise HTTPException(status_code=404, detail="Registro de producción no encontrado")
    crud.delete_production(db, production_id)
    return {"ok": True}

