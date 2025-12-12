from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from ..db.database import Base
# Modelo de la tabla de Usuarios
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    # Relación con la tabla de productos
    products = relationship("Product", back_populates="owner")
    # Relación con animales
    animals = relationship("Animal", back_populates="owner")

# Modelo de la tabla de Productos (el CRUD principal)
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Clave foránea para el usuario que creó el producto
    owner_id = Column(Integer, ForeignKey("users.id"))
    # Relación con la tabla de usuarios
    owner = relationship("User", back_populates="products")

# --- Enumeraciones para el sistema ganadero ---
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

# --- Modelo de Razas ---
class Breed(Base):
    __tablename__ = "breeds"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    characteristics = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relación con animales
    animals = relationship("Animal", back_populates="breed")

# --- Modelo de Animales (Principal) ---
class Animal(Base):
    __tablename__ = "animals"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)  # Código/Arete
    name = Column(String, index=True)
    birth_date = Column(DateTime)
    sex = Column(SQLEnum(AnimalSex), nullable=False)
    status = Column(SQLEnum(AnimalStatus), default=AnimalStatus.ACTIVO)
    weight = Column(Float)
    photo_url = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Claves foráneas
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    breed_id = Column(Integer, ForeignKey("breeds.id"))
    # Relaciones
    owner = relationship("User", back_populates="animals")
    breed = relationship("Breed", back_populates="animals")
    medical_records = relationship("MedicalRecord", back_populates="animal", cascade="all, delete-orphan")
    reproductions = relationship("Reproduction", foreign_keys="Reproduction.mother_id", back_populates="mother")
    productions = relationship("Production", back_populates="animal", cascade="all, delete-orphan")
    weight_records = relationship("WeightRecord", back_populates="animal", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="animal", cascade="all, delete-orphan")

# --- Modelo de Registros Médicos ---
class MedicalRecord(Base):
    __tablename__ = "medical_records"
    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    record_type = Column(SQLEnum(MedicalRecordType), nullable=False)
    description = Column(Text)
    veterinarian = Column(String)
    cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relación
    animal = relationship("Animal", back_populates="medical_records")

# --- Modelo de Reproducción ---
class Reproduction(Base):
    __tablename__ = "reproductions"
    id = Column(Integer, primary_key=True, index=True)
    mother_id = Column(Integer, ForeignKey("animals.id"), nullable=False)
    father_id = Column(Integer, ForeignKey("animals.id"))
    insemination_date = Column(DateTime)
    expected_birth_date = Column(DateTime)
    actual_birth_date = Column(DateTime)
    status = Column(String, default="en_gestacion")  # en_gestacion, completado, aborto
    offspring_count = Column(Integer, default=1)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relaciones
    mother = relationship("Animal", foreign_keys=[mother_id], back_populates="reproductions")
    father = relationship("Animal", foreign_keys=[father_id])

# --- Modelo de Producción ---
class Production(Base):
    __tablename__ = "productions"
    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    production_type = Column(SQLEnum(ProductionType), nullable=False)
    quantity = Column(Float, nullable=False)
    quality = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relación
    animal = relationship("Animal", back_populates="productions")

# --- Modelo de Registro de Pesos ---
class WeightRecord(Base):
    __tablename__ = "weight_records"
    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    weight = Column(Float, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relación
    animal = relationship("Animal", back_populates="weight_records")

# --- Modelo de Eventos ---
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"))
    event_type = Column(SQLEnum(EventType), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    description = Column(Text)
    amount = Column(Float)  # Para ventas/compras
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relación
    animal = relationship("Animal", back_populates="events")