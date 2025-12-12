from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..crud import crud
from ..schemas import schemas
from ..db.database import get_db

router = APIRouter(
    prefix="/animals",
    tags=["Animales"],
)

@router.post(
    "/", 
    response_model=schemas.Animal, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo animal",
    description="""
    Crea un nuevo animal en el sistema.
    
    **Campos requeridos:**
    - `code`: Código único del animal (máximo 50 caracteres)
    - `sex`: Sexo del animal - debe ser "macho" o "hembra"
    
    **Campos opcionales:**
    - `name`: Nombre del animal
    - `birth_date`: Fecha de nacimiento
    - `status`: Estado del animal (por defecto: "activo")
    - `weight`: Peso del animal
    - `photo_url`: URL de la foto del animal
    - `notes`: Notas adicionales
    - `breed_id`: ID de la raza (debe existir si se proporciona)
    """,
    responses={
        201: {
            "description": "Animal creado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "code": "BOV-001",
                        "name": "Toro Bravo",
                        "sex": "macho",
                        "status": "activo",
                        "weight": 450.5,
                        "owner_id": 1,
                        "breed_id": 1
                    }
                }
            }
        }
    }
)
def create_animal(
    animal: schemas.AnimalCreate,
    db: Session = Depends(get_db)
):
    # Verificar que el código no esté duplicado
    existing_animal = crud.get_animal_by_code(db, code=animal.code)
    if existing_animal:
        raise HTTPException(
            status_code=400, 
            detail="El código del animal ya está registrado"
        )
    
    # Validar que la raza existe si se proporciona breed_id
    if animal.breed_id is not None:
        breed = crud.get_breed(db, breed_id=animal.breed_id)
        if not breed:
            raise HTTPException(
                status_code=404, 
                detail=f"Raza con ID {animal.breed_id} no encontrada"
            )
    
    # Obtener el primer usuario disponible o crear uno por defecto si no hay owner_id
    from ..modelo import modelo
    owner_id = getattr(animal, 'owner_id', None)
    if owner_id is None:
        # Buscar el primer usuario en la base de datos
        first_user = db.query(modelo.User).first()
        if first_user:
            owner_id = first_user.id
        else:
            # Crear un usuario por defecto si no existe ninguno
            from ..schemas import schemas as schemas_module
            default_user = schemas_module.UserCreate(
                email="default@example.com",
                password="default123"
            )
            new_user = crud.create_user(db=db, user=default_user)
            owner_id = new_user.id
    
    return crud.create_animal(db=db, animal=animal, owner_id=owner_id)

@router.get(
    "/", 
    response_model=List[schemas.Animal],
    summary="Listar animales",
    description="Obtiene una lista de todos los animales con opción de paginación y filtrado.",
    responses={
        200: {
            "description": "Lista de animales obtenida exitosamente"
        }
    }
)
def read_animals(
    skip: int = Query(0, ge=0, description="Número de registros a omitir (paginación)"), 
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"), 
    owner_id: Optional[int] = Query(None, description="Filtrar por ID de propietario"),
    db: Session = Depends(get_db)
):
    animals = crud.get_animals(db, skip=skip, limit=limit, owner_id=owner_id)
    return animals

@router.get(
    "/{animal_id}", 
    response_model=schemas.Animal,
    summary="Obtener animal por ID",
    description="Obtiene la información completa de un animal específico por su ID.",
    responses={
        200: {
            "description": "Animal encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "code": "BOV-001",
                        "name": "Toro Bravo",
                        "sex": "macho",
                        "status": "activo"
                    }
                }
            }
        }
    }
)
def read_animal(animal_id: int, db: Session = Depends(get_db)):
    db_animal = crud.get_animal(db, animal_id=animal_id)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return db_animal

@router.put(
    "/{animal_id}", 
    response_model=schemas.Animal,
    summary="Actualizar animal",
    description="Actualiza la información de un animal existente. Todos los campos son opcionales.",
    responses={
        200: {
            "description": "Animal actualizado exitosamente"
        }
    }
)
def update_animal(
    animal_id: int,
    animal: schemas.AnimalUpdate,
    db: Session = Depends(get_db)
):
    db_animal = crud.get_animal(db, animal_id)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    
    # Validar que la raza existe si se proporciona breed_id
    if animal.breed_id is not None:
        breed = crud.get_breed(db, breed_id=animal.breed_id)
        if not breed:
            raise HTTPException(
                status_code=404, 
                detail=f"Raza con ID {animal.breed_id} no encontrada"
            )
    
    # Verificar código único si se está actualizando
    if animal.code and animal.code != db_animal.code:
        existing_animal = crud.get_animal_by_code(db, code=animal.code)
        if existing_animal:
            raise HTTPException(
                status_code=400, 
                detail="El código del animal ya está registrado"
            )
    return crud.update_animal(db, animal_id, animal)

@router.delete(
    "/{animal_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar animal",
    description="Elimina un animal del sistema. Esta acción no se puede deshacer.",
    responses={
        204: {
            "description": "Animal eliminado exitosamente"
        }
    }
)
def delete_animal(
    animal_id: int,
    db: Session = Depends(get_db)
):
    db_animal = crud.get_animal(db, animal_id)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    crud.delete_animal(db, animal_id)
    return {"ok": True}

