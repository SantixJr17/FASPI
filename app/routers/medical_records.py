from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..crud import crud
from ..schemas import schemas
from ..db.database import get_db

router = APIRouter(
    prefix="/medical-records",
    tags=["Registros Médicos"],
)

@router.post(
    "/", 
    response_model=schemas.MedicalRecord, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear registro médico",
    description="Crea un nuevo registro médico para un animal."
)
def create_medical_record(
    record: schemas.MedicalRecordCreate,
    db: Session = Depends(get_db)
):
    # Verificar que el animal existe
    animal = crud.get_animal(db, record.animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return crud.create_medical_record(db=db, record=record)

@router.get(
    "/", 
    response_model=List[schemas.MedicalRecord],
    summary="Listar registros médicos",
    description="Obtiene una lista de todos los registros médicos con opción de filtrado por animal."
)
def read_medical_records(
    skip: int = 0,
    limit: int = 100,
    animal_id: Optional[int] = Query(None, description="Filtrar por ID de animal"),
    db: Session = Depends(get_db)
):
    records = crud.get_medical_records(db, skip=skip, limit=limit, animal_id=animal_id)
    return records

@router.get(
    "/{record_id}", 
    response_model=schemas.MedicalRecord,
    summary="Obtener registro médico por ID",
    description="Obtiene la información completa de un registro médico específico por su ID."
)
def read_medical_record(record_id: int, db: Session = Depends(get_db)):
    db_record = crud.get_medical_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Registro médico no encontrado")
    return db_record

@router.put(
    "/{record_id}", 
    response_model=schemas.MedicalRecord,
    summary="Actualizar registro médico",
    description="Actualiza la información de un registro médico existente."
)
def update_medical_record(
    record_id: int,
    record: schemas.MedicalRecordUpdate,
    db: Session = Depends(get_db)
):
    db_record = crud.get_medical_record(db, record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Registro médico no encontrado")
    return crud.update_medical_record(db, record_id, record)

@router.delete(
    "/{record_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar registro médico",
    description="Elimina un registro médico del sistema."
)
def delete_medical_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    db_record = crud.get_medical_record(db, record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Registro médico no encontrado")
    crud.delete_medical_record(db, record_id)
    return {"ok": True}

