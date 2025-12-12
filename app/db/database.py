from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a la base de datos. Por defecto, SQLite.
# Para cambiar a PostgreSQL, solo se debe modificar esta línea:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host:port/dbname"
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# El argumento connect_args es necesario solo para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal es la clase que usaremos para crear sesiones de base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase base de la que heredarán todos nuestros modelos de SQLAlchemy.
Base = declarative_base()

# Función de utilidad para obtener una sesión de base de datos (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
