from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..crud import crud
from ..schemas import schemas
from ..db.database import get_db

router = APIRouter(
    prefix="/events",
    tags=["Eventos"],
)

@router.post(
    "/", 
    response_model=schemas.Event, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo evento",
    description="Crea un nuevo evento en el sistema, opcionalmente asociado a un animal."
)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db)
):
    # Verificar que el animal existe si se proporciona
    if event.animal_id:
        animal = crud.get_animal(db, event.animal_id)
        if not animal:
            raise HTTPException(status_code=404, detail="Animal no encontrado")
    return crud.create_event(db=db, event=event)

@router.get(
    "/", 
    response_model=List[schemas.Event],
    summary="Listar eventos",
    description="Obtiene una lista de todos los eventos con opción de filtrado por animal o tipo de evento."
)
def read_events(
    skip: int = 0,
    limit: int = 100,
    animal_id: Optional[int] = Query(None, description="Filtrar por ID de animal"),
    event_type: Optional[str] = Query(None, description="Filtrar por tipo de evento"),
    db: Session = Depends(get_db)
):
    events = crud.get_events(db, skip=skip, limit=limit, animal_id=animal_id, event_type=event_type)
    return events

@router.get(
    "/{event_id}", 
    response_model=schemas.Event,
    summary="Obtener evento por ID",
    description="Obtiene la información completa de un evento específico por su ID."
)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return db_event

@router.put(
    "/{event_id}", 
    response_model=schemas.Event,
    summary="Actualizar evento",
    description="Actualiza la información de un evento existente."
)
def update_event(
    event_id: int,
    event: schemas.EventUpdate,
    db: Session = Depends(get_db)
):
    db_event = crud.get_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return crud.update_event(db, event_id, event)

@router.delete(
    "/{event_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar evento",
    description="Elimina un evento del sistema."
)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    db_event = crud.get_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    crud.delete_event(db, event_id)
    return {"ok": True}

