from app.database import Base, engine
from app import models

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas correctamente.")

if __name__ == "__main__":
    create_tables()
