from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..crud import crud
from ..schemas import schemas
from ..db.database import get_db

router = APIRouter(
    prefix="/breeds",
    tags=["Razas"],
)

@router.post(
    "/", 
    response_model=schemas.Breed, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva raza",
    description="Crea una nueva raza de animal en el sistema."
)
def create_breed(
    breed: schemas.BreedCreate,
    db: Session = Depends(get_db)
):
    return crud.create_breed(db=db, breed=breed)

@router.get(
    "/", 
    response_model=List[schemas.Breed],
    summary="Listar razas",
    description="Obtiene una lista de todas las razas registradas en el sistema."
)
def read_breeds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    breeds = crud.get_breeds(db, skip=skip, limit=limit)
    return breeds

@router.get(
    "/{breed_id}", 
    response_model=schemas.Breed,
    summary="Obtener raza por ID",
    description="Obtiene la información completa de una raza específica por su ID."
)
def read_breed(breed_id: int, db: Session = Depends(get_db)):
    db_breed = crud.get_breed(db, breed_id=breed_id)
    if db_breed is None:
        raise HTTPException(status_code=404, detail="Raza no encontrada")
    return db_breed

@router.put(
    "/{breed_id}", 
    response_model=schemas.Breed,
    summary="Actualizar raza",
    description="Actualiza la información de una raza existente."
)
def update_breed(
    breed_id: int,
    breed: schemas.BreedUpdate,
    db: Session = Depends(get_db)
):
    db_breed = crud.get_breed(db, breed_id)
    if db_breed is None:
        raise HTTPException(status_code=404, detail="Raza no encontrada")
    return crud.update_breed(db, breed_id, breed)

@router.delete(
    "/{breed_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar raza",
    description="Elimina una raza del sistema."
)
def delete_breed(
    breed_id: int,
    db: Session = Depends(get_db)
):
    db_breed = crud.get_breed(db, breed_id)
    if db_breed is None:
        raise HTTPException(status_code=404, detail="Raza no encontrada")
    crud.delete_breed(db, breed_id)
    return {"ok": True}

