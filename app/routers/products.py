from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..crud import crud
from ..schemas import schemas
from ..db.database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Productos"],
)

@router.post(
    "/", 
    response_model=schemas.Product, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo producto",
    description="Crea un nuevo producto en el sistema."
)
def create_product_for_user(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    # Obtener el primer usuario disponible o crear uno por defecto si no hay owner_id
    from ..modelo import modelo
    user_id = getattr(product, 'owner_id', None)
    if user_id is None:
        # Buscar el primer usuario en la base de datos
        first_user = db.query(modelo.User).first()
        if first_user:
            user_id = first_user.id
        else:
            # Crear un usuario por defecto si no existe ninguno
            from ..schemas import schemas as schemas_module
            default_user = schemas_module.UserCreate(
                email="default@example.com",
                password="default123"
            )
            new_user = crud.create_user(db=db, user=default_user)
            user_id = new_user.id
    return crud.create_user_product(db=db, product=product, user_id=user_id)

@router.get(
    "/", 
    response_model=List[schemas.Product],
    summary="Listar productos",
    description="Obtiene una lista de todos los productos con opción de paginación."
)
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.get(
    "/{product_id}", 
    response_model=schemas.Product,
    summary="Obtener producto por ID",
    description="Obtiene la información completa de un producto específico por su ID."
)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_product

@router.put(
    "/{product_id}", 
    response_model=schemas.Product,
    summary="Actualizar producto",
    description="Actualiza la información de un producto existente."
)
def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return crud.update_product(db, product_id, product)

@router.delete(
    "/{product_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar producto",
    description="Elimina un producto del sistema."
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    crud.delete_product(db, product_id)
    return {"ok": True}
