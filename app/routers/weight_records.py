from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..crud import crud
from ..schemas import schemas
from ..db.database import get_db

router = APIRouter(
    prefix="/weight-records",
    tags=["Registros de Peso"],
)

@router.post(
    "/", 
    response_model=schemas.WeightRecord, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear registro de peso",
    description="Crea un nuevo registro de peso para un animal y actualiza el peso actual del animal."
)
def create_weight_record(
    weight_record: schemas.WeightRecordCreate,
    db: Session = Depends(get_db)
):
    # Verificar que el animal existe
    animal = crud.get_animal(db, weight_record.animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    # Actualizar el peso del animal
    animal.weight = weight_record.weight
    db.commit()
    return crud.create_weight_record(db=db, weight_record=weight_record)

@router.get(
    "/", 
    response_model=List[schemas.WeightRecord],
    summary="Listar registros de peso",
    description="Obtiene una lista de todos los registros de peso con opción de filtrado por animal."
)
def read_weight_records(
    skip: int = 0,
    limit: int = 100,
    animal_id: Optional[int] = Query(None, description="Filtrar por ID de animal"),
    db: Session = Depends(get_db)
):
    records = crud.get_weight_records(db, skip=skip, limit=limit, animal_id=animal_id)
    return records

@router.get(
    "/{weight_record_id}", 
    response_model=schemas.WeightRecord,
    summary="Obtener registro de peso por ID",
    description="Obtiene la información completa de un registro de peso específico por su ID."
)
def read_weight_record(weight_record_id: int, db: Session = Depends(get_db)):
    db_record = crud.get_weight_record(db, weight_record_id=weight_record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Registro de peso no encontrado")
    return db_record

@router.put(
    "/{weight_record_id}", 
    response_model=schemas.WeightRecord,
    summary="Actualizar registro de peso",
    description="Actualiza la información de un registro de peso existente."
)
def update_weight_record(
    weight_record_id: int,
    weight_record: schemas.WeightRecordUpdate,
    db: Session = Depends(get_db)
):
    db_record = crud.get_weight_record(db, weight_record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Registro de peso no encontrado")
    # Actualizar peso del animal si se cambia
    if weight_record.weight:
        animal = crud.get_animal(db, db_record.animal_id)
        if animal:
            animal.weight = weight_record.weight
            db.commit()
    return crud.update_weight_record(db, weight_record_id, weight_record)

@router.delete(
    "/{weight_record_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar registro de peso",
    description="Elimina un registro de peso del sistema."
)
def delete_weight_record(
    weight_record_id: int,
    db: Session = Depends(get_db)
):
    db_record = crud.get_weight_record(db, weight_record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Registro de peso no encontrado")
    crud.delete_weight_record(db, weight_record_id)
    return {"ok": True}

