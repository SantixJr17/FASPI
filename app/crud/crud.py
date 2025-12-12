from sqlalchemy.orm import Session
from typing import Optional
from ..modelo import modelo
from ..schemas import schemas
from ..security.security import get_password_hash

# --- Operaciones de Usuarios ---
def get_user_by_email(db: Session, email: str):
    """Busca un usuario por su email."""
    return db.query(modelo.User).filter(modelo.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Crea un nuevo usuario y hashea la contraseña."""
    hashed_password = get_password_hash(user.password)
    db_user = modelo.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Operaciones de Productos (CRUD) ---
def get_products(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de productos con paginación."""
    return db.query(modelo.Product).offset(skip).limit(limit).all()

def create_user_product(db: Session, product: schemas.ProductCreate, user_id: int):
    """Crea un producto asociado a un usuario."""
    db_product = modelo.Product(**product.model_dump(), owner_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    """Obtiene un producto por su ID."""
    return db.query(modelo.Product).filter(modelo.Product.id == product_id).first()

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    """Actualiza un producto existente."""
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product

def delete_product(db: Session, product_id: int):
    """Elimina un producto por su ID."""
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

# --- Operaciones de Razas (CRUD) ---
def get_breeds(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de razas con paginación."""
    return db.query(modelo.Breed).offset(skip).limit(limit).all()

def get_breed(db: Session, breed_id: int):
    """Obtiene una raza por su ID."""
    return db.query(modelo.Breed).filter(modelo.Breed.id == breed_id).first()

def create_breed(db: Session, breed: schemas.BreedCreate):
    """Crea una nueva raza."""
    db_breed = modelo.Breed(**breed.model_dump())
    db.add(db_breed)
    db.commit()
    db.refresh(db_breed)
    return db_breed

def update_breed(db: Session, breed_id: int, breed: schemas.BreedUpdate):
    """Actualiza una raza existente."""
    db_breed = get_breed(db, breed_id)
    if db_breed:
        update_data = breed.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_breed, key, value)
        db.commit()
        db.refresh(db_breed)
        return db_breed
    return None

def delete_breed(db: Session, breed_id: int):
    """Elimina una raza por su ID."""
    db_breed = get_breed(db, breed_id)
    if db_breed:
        db.delete(db_breed)
        db.commit()
        return True
    return False

# --- Operaciones de Animales (CRUD) ---
def get_animals(db: Session, skip: int = 0, limit: int = 100, owner_id: Optional[int] = None):
    """Obtiene una lista de animales con paginación."""
    query = db.query(modelo.Animal)
    if owner_id:
        query = query.filter(modelo.Animal.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()

def get_animal(db: Session, animal_id: int):
    """Obtiene un animal por su ID."""
    return db.query(modelo.Animal).filter(modelo.Animal.id == animal_id).first()

def get_animal_by_code(db: Session, code: str):
    """Obtiene un animal por su código/arete."""
    return db.query(modelo.Animal).filter(modelo.Animal.code == code).first()

def create_animal(db: Session, animal: schemas.AnimalCreate, owner_id: int):
    """Crea un nuevo animal."""
    db_animal = modelo.Animal(**animal.model_dump(), owner_id=owner_id)
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

def update_animal(db: Session, animal_id: int, animal: schemas.AnimalUpdate):
    """Actualiza un animal existente."""
    db_animal = get_animal(db, animal_id)
    if db_animal:
        update_data = animal.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_animal, key, value)
        db.commit()
        db.refresh(db_animal)
        return db_animal
    return None

def delete_animal(db: Session, animal_id: int):
    """Elimina un animal por su ID."""
    db_animal = get_animal(db, animal_id)
    if db_animal:
        db.delete(db_animal)
        db.commit()
        return True
    return False

# --- Operaciones de Registros Médicos (CRUD) ---
def get_medical_records(db: Session, skip: int = 0, limit: int = 100, animal_id: Optional[int] = None):
    """Obtiene registros médicos con paginación."""
    query = db.query(modelo.MedicalRecord)
    if animal_id:
        query = query.filter(modelo.MedicalRecord.animal_id == animal_id)
    return query.order_by(modelo.MedicalRecord.date.desc()).offset(skip).limit(limit).all()

def get_medical_record(db: Session, record_id: int):
    """Obtiene un registro médico por su ID."""
    return db.query(modelo.MedicalRecord).filter(modelo.MedicalRecord.id == record_id).first()

def create_medical_record(db: Session, record: schemas.MedicalRecordCreate):
    """Crea un nuevo registro médico."""
    db_record = modelo.MedicalRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_medical_record(db: Session, record_id: int, record: schemas.MedicalRecordUpdate):
    """Actualiza un registro médico existente."""
    db_record = get_medical_record(db, record_id)
    if db_record:
        update_data = record.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
        return db_record
    return None

def delete_medical_record(db: Session, record_id: int):
    """Elimina un registro médico por su ID."""
    db_record = get_medical_record(db, record_id)
    if db_record:
        db.delete(db_record)
        db.commit()
        return True
    return False

# --- Operaciones de Reproducción (CRUD) ---
def get_reproductions(db: Session, skip: int = 0, limit: int = 100, animal_id: Optional[int] = None):
    """Obtiene registros de reproducción con paginación."""
    query = db.query(modelo.Reproduction)
    if animal_id:
        query = query.filter(
            (modelo.Reproduction.mother_id == animal_id) | 
            (modelo.Reproduction.father_id == animal_id)
        )
    return query.order_by(modelo.Reproduction.insemination_date.desc()).offset(skip).limit(limit).all()

def get_reproduction(db: Session, reproduction_id: int):
    """Obtiene un registro de reproducción por su ID."""
    return db.query(modelo.Reproduction).filter(modelo.Reproduction.id == reproduction_id).first()

def create_reproduction(db: Session, reproduction: schemas.ReproductionCreate):
    """Crea un nuevo registro de reproducción."""
    db_reproduction = modelo.Reproduction(**reproduction.model_dump())
    db.add(db_reproduction)
    db.commit()
    db.refresh(db_reproduction)
    return db_reproduction

def update_reproduction(db: Session, reproduction_id: int, reproduction: schemas.ReproductionUpdate):
    """Actualiza un registro de reproducción existente."""
    db_reproduction = get_reproduction(db, reproduction_id)
    if db_reproduction:
        update_data = reproduction.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_reproduction, key, value)
        db.commit()
        db.refresh(db_reproduction)
        return db_reproduction
    return None

def delete_reproduction(db: Session, reproduction_id: int):
    """Elimina un registro de reproducción por su ID."""
    db_reproduction = get_reproduction(db, reproduction_id)
    if db_reproduction:
        db.delete(db_reproduction)
        db.commit()
        return True
    return False

# --- Operaciones de Producción (CRUD) ---
def get_productions(db: Session, skip: int = 0, limit: int = 100, animal_id: Optional[int] = None):
    """Obtiene registros de producción con paginación."""
    query = db.query(modelo.Production)
    if animal_id:
        query = query.filter(modelo.Production.animal_id == animal_id)
    return query.order_by(modelo.Production.date.desc()).offset(skip).limit(limit).all()

def get_production(db: Session, production_id: int):
    """Obtiene un registro de producción por su ID."""
    return db.query(modelo.Production).filter(modelo.Production.id == production_id).first()

def create_production(db: Session, production: schemas.ProductionCreate):
    """Crea un nuevo registro de producción."""
    db_production = modelo.Production(**production.model_dump())
    db.add(db_production)
    db.commit()
    db.refresh(db_production)
    return db_production

def update_production(db: Session, production_id: int, production: schemas.ProductionUpdate):
    """Actualiza un registro de producción existente."""
    db_production = get_production(db, production_id)
    if db_production:
        update_data = production.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_production, key, value)
        db.commit()
        db.refresh(db_production)
        return db_production
    return None

def delete_production(db: Session, production_id: int):
    """Elimina un registro de producción por su ID."""
    db_production = get_production(db, production_id)
    if db_production:
        db.delete(db_production)
        db.commit()
        return True
    return False

# --- Operaciones de Registro de Pesos (CRUD) ---
def get_weight_records(db: Session, skip: int = 0, limit: int = 100, animal_id: Optional[int] = None):
    """Obtiene registros de peso con paginación."""
    query = db.query(modelo.WeightRecord)
    if animal_id:
        query = query.filter(modelo.WeightRecord.animal_id == animal_id)
    return query.order_by(modelo.WeightRecord.date.desc()).offset(skip).limit(limit).all()

def get_weight_record(db: Session, weight_record_id: int):
    """Obtiene un registro de peso por su ID."""
    return db.query(modelo.WeightRecord).filter(modelo.WeightRecord.id == weight_record_id).first()

def create_weight_record(db: Session, weight_record: schemas.WeightRecordCreate):
    """Crea un nuevo registro de peso."""
    db_weight_record = modelo.WeightRecord(**weight_record.model_dump())
    db.add(db_weight_record)
    db.commit()
    db.refresh(db_weight_record)
    return db_weight_record

def update_weight_record(db: Session, weight_record_id: int, weight_record: schemas.WeightRecordUpdate):
    """Actualiza un registro de peso existente."""
    db_weight_record = get_weight_record(db, weight_record_id)
    if db_weight_record:
        update_data = weight_record.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_weight_record, key, value)
        db.commit()
        db.refresh(db_weight_record)
        return db_weight_record
    return None

def delete_weight_record(db: Session, weight_record_id: int):
    """Elimina un registro de peso por su ID."""
    db_weight_record = get_weight_record(db, weight_record_id)
    if db_weight_record:
        db.delete(db_weight_record)
        db.commit()
        return True
    return False

# --- Operaciones de Eventos (CRUD) ---
def get_events(db: Session, skip: int = 0, limit: int = 100, animal_id: Optional[int] = None, event_type: Optional[str] = None):
    """Obtiene eventos con paginación."""
    query = db.query(modelo.Event)
    if animal_id:
        query = query.filter(modelo.Event.animal_id == animal_id)
    if event_type:
        query = query.filter(modelo.Event.event_type == event_type)
    return query.order_by(modelo.Event.date.desc()).offset(skip).limit(limit).all()

def get_event(db: Session, event_id: int):
    """Obtiene un evento por su ID."""
    return db.query(modelo.Event).filter(modelo.Event.id == event_id).first()

def create_event(db: Session, event: schemas.EventCreate):
    """Crea un nuevo evento."""
    db_event = modelo.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event: schemas.EventUpdate):
    """Actualiza un evento existente."""
    db_event = get_event(db, event_id)
    if db_event:
        update_data = event.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_event, key, value)
        db.commit()
        db.refresh(db_event)
        return db_event
    return None

def delete_event(db: Session, event_id: int):
    """Elimina un evento por su ID."""
    db_event = get_event(db, event_id)
    if db_event:
        db.delete(db_event)
        db.commit()
        return True
    return False
