from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

# --- Esquemas de Productos ---
class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    price: float = Field(..., gt=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[float] = None

class Product(ProductBase):
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True  # Permite leer datos directamente de modelos SQLAlchemy (Pydantic v2)

# --- Esquemas de Usuarios y Autenticación ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    products: List[Product] = []
    
    class Config:
        from_attributes = True

# --- Esquemas de Tokens JWT ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Enumeraciones para Schemas ---
class AnimalStatus(str, Enum):
    ACTIVO = "activo"
    VENDIDO = "vendido"
    MUERTO = "muerto"
    ENFERMO = "enfermo"

class AnimalSex(str, Enum):
    MACHO = "macho"
    HEMBRA = "hembra"

class MedicalRecordType(str, Enum):
    VACUNACION = "vacunacion"
    TRATAMIENTO = "tratamiento"
    ENFERMEDAD = "enfermedad"
    DESPARASITACION = "desparasitacion"
    OTRO = "otro"

class EventType(str, Enum):
    NACIMIENTO = "nacimiento"
    MUERTE = "muerte"
    VENTA = "venta"
    COMPRA = "compra"
    TRASLADO = "traslado"
    OTRO = "otro"

class ProductionType(str, Enum):
    LECHE = "leche"
    HUEVOS = "huevos"
    CARNE = "carne"
    OTRO = "otro"

# --- Esquemas de Razas ---
class BreedBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    characteristics: Optional[str] = None

class BreedCreate(BreedBase):
    pass

class BreedUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    characteristics: Optional[str] = None

class Breed(BreedBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Esquemas de Animales ---
class AnimalBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    name: Optional[str] = Field(None, max_length=100)
    birth_date: Optional[datetime] = None
    sex: AnimalSex
    status: Optional[AnimalStatus] = AnimalStatus.ACTIVO
    weight: Optional[float] = Field(None, gt=0)
    photo_url: Optional[str] = None
    notes: Optional[str] = None

class AnimalCreate(AnimalBase):
    breed_id: Optional[int] = None

class AnimalUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, max_length=100)
    birth_date: Optional[datetime] = None
    sex: Optional[AnimalSex] = None
    status: Optional[AnimalStatus] = None
    weight: Optional[float] = Field(None, gt=0)
    photo_url: Optional[str] = None
    notes: Optional[str] = None
    breed_id: Optional[int] = None

class Animal(AnimalBase):
    id: int
    owner_id: int
    breed_id: Optional[int] = None
    created_at: datetime
    breed: Optional[Breed] = None
    
    class Config:
        from_attributes = True

# --- Esquemas de Registros Médicos ---
class MedicalRecordBase(BaseModel):
    date: datetime = Field(default_factory=datetime.utcnow)
    record_type: MedicalRecordType
    description: Optional[str] = None
    veterinarian: Optional[str] = Field(None, max_length=100)
    cost: Optional[float] = Field(0.0, ge=0)

class MedicalRecordCreate(MedicalRecordBase):
    animal_id: int

class MedicalRecordUpdate(BaseModel):
    date: Optional[datetime] = None
    record_type: Optional[MedicalRecordType] = None
    description: Optional[str] = None
    veterinarian: Optional[str] = Field(None, max_length=100)
    cost: Optional[float] = Field(None, ge=0)

class MedicalRecord(MedicalRecordBase):
    id: int
    animal_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Esquemas de Reproducción ---
class ReproductionBase(BaseModel):
    insemination_date: Optional[datetime] = None
    expected_birth_date: Optional[datetime] = None
    actual_birth_date: Optional[datetime] = None
    status: Optional[str] = "en_gestacion"
    offspring_count: Optional[int] = Field(1, ge=1)
    notes: Optional[str] = None

class ReproductionCreate(ReproductionBase):
    mother_id: int
    father_id: Optional[int] = None

class ReproductionUpdate(BaseModel):
    insemination_date: Optional[datetime] = None
    expected_birth_date: Optional[datetime] = None
    actual_birth_date: Optional[datetime] = None
    status: Optional[str] = None
    offspring_count: Optional[int] = Field(None, ge=1)
    notes: Optional[str] = None
    father_id: Optional[int] = None

class Reproduction(ReproductionBase):
    id: int
    mother_id: int
    father_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Esquemas de Producción ---
class ProductionBase(BaseModel):
    date: datetime = Field(default_factory=datetime.utcnow)
    production_type: ProductionType
    quantity: float = Field(..., gt=0)
    quality: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None

class ProductionCreate(ProductionBase):
    animal_id: int

class ProductionUpdate(BaseModel):
    date: Optional[datetime] = None
    production_type: Optional[ProductionType] = None
    quantity: Optional[float] = Field(None, gt=0)
    quality: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None

class Production(ProductionBase):
    id: int
    animal_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Esquemas de Registro de Pesos ---
class WeightRecordBase(BaseModel):
    date: datetime = Field(default_factory=datetime.utcnow)
    weight: float = Field(..., gt=0)
    notes: Optional[str] = None

class WeightRecordCreate(WeightRecordBase):
    animal_id: int

class WeightRecordUpdate(BaseModel):
    date: Optional[datetime] = None
    weight: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = None

class WeightRecord(WeightRecordBase):
    id: int
    animal_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Esquemas de Eventos ---
class EventBase(BaseModel):
    event_type: EventType
    date: datetime = Field(default_factory=datetime.utcnow)
    description: Optional[str] = None
    amount: Optional[float] = Field(None, ge=0)

class EventCreate(EventBase):
    animal_id: Optional[int] = None

class EventUpdate(BaseModel):
    event_type: Optional[EventType] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    amount: Optional[float] = Field(None, ge=0)

class Event(EventBase):
    id: int
    animal_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
