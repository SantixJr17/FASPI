from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..crud import crud
from ..schemas import schemas
from ..db.database import get_db

router = APIRouter(
    prefix="/reproductions",
    tags=["Reproducción"],
)

@router.post(
    "/", 
    response_model=schemas.Reproduction, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear registro de reproducción",
    description="Crea un nuevo registro de reproducción para animales."
)
def create_reproduction(
    reproduction: schemas.ReproductionCreate,
    db: Session = Depends(get_db)
):
    # Verificar que la madre existe
    mother = crud.get_animal(db, reproduction.mother_id)
    if not mother:
        raise HTTPException(status_code=404, detail="Animal madre no encontrado")
    # Verificar padre si se proporciona
    if reproduction.father_id:
        father = crud.get_animal(db, reproduction.father_id)
        if not father:
            raise HTTPException(status_code=404, detail="Animal padre no encontrado")
    return crud.create_reproduction(db=db, reproduction=reproduction)

@router.get(
    "/", 
    response_model=List[schemas.Reproduction],
    summary="Listar registros de reproducción",
    description="Obtiene una lista de todos los registros de reproducción con opción de filtrado."
)
def read_reproductions(
    skip: int = 0,
    limit: int = 100,
    animal_id: Optional[int] = Query(None, description="Filtrar por ID de animal (madre o padre)"),
    db: Session = Depends(get_db)
):
    reproductions = crud.get_reproductions(db, skip=skip, limit=limit, animal_id=animal_id)
    return reproductions

@router.get(
    "/{reproduction_id}", 
    response_model=schemas.Reproduction,
    summary="Obtener registro de reproducción por ID",
    description="Obtiene la información completa de un registro de reproducción específico por su ID."
)
def read_reproduction(reproduction_id: int, db: Session = Depends(get_db)):
    db_reproduction = crud.get_reproduction(db, reproduction_id=reproduction_id)
    if db_reproduction is None:
        raise HTTPException(status_code=404, detail="Registro de reproducción no encontrado")
    return db_reproduction

@router.put(
    "/{reproduction_id}", 
    response_model=schemas.Reproduction,
    summary="Actualizar registro de reproducción",
    description="Actualiza la información de un registro de reproducción existente."
)
def update_reproduction(
    reproduction_id: int,
    reproduction: schemas.ReproductionUpdate,
    db: Session = Depends(get_db)
):
    db_reproduction = crud.get_reproduction(db, reproduction_id)
    if db_reproduction is None:
        raise HTTPException(status_code=404, detail="Registro de reproducción no encontrado")
    return crud.update_reproduction(db, reproduction_id, reproduction)

@router.delete(
    "/{reproduction_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar registro de reproducción",
    description="Elimina un registro de reproducción del sistema."
)
def delete_reproduction(
    reproduction_id: int,
    db: Session = Depends(get_db)
):
    db_reproduction = crud.get_reproduction(db, reproduction_id)
    if db_reproduction is None:
        raise HTTPException(status_code=404, detail="Registro de reproducción no encontrado")
    crud.delete_reproduction(db, reproduction_id)
    return {"ok": True}

