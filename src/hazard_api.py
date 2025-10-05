# main.py
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database_proc import database, models, schemas
from .helpers import fetch_wfs
from uuid import UUID
from passlib.hash import sha256_crypt
from config import WFS_URL

router = APIRouter(prefix="/hazards", tags=["hazards"])

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    return next(database.get_db())

def hash_password(password: str) -> str:
    return sha256_crypt.hash(password)

@router.post("/", response_model=schemas.HazardOut, status_code=status.HTTP_201_CREATED)
def create_hazard(hazard_in: schemas.HazardCreate, db: Session = Depends(get_db)):
    hazard = models.Hazard(**hazard_in.model_dump())
    db.add(hazard)
    db.commit()
    db.refresh(hazard)
    return hazard

@router.get("/", response_model=List[schemas.HazardOut])
def list_hazards(db: Session = Depends(get_db)):
    return db.query(models.Hazard).all()

@router.get("/external", response_model=List[schemas.HazardOut])
def aggregate_all():
    all_data = []

    # === WFS ===

    all_data.extend(fetch_wfs(WFS_URL))

    # === DATEX2 and GTFS-rt ===

    return all_data

@router.patch("/{hazard_id}", response_model=schemas.HazardOut)
def update_hazard(hazard_id: UUID, hazard_in: schemas.HazardUpdate, db: Session = Depends(get_db)):
    hazard = db.get(models.Hazard, hazard_id)
    if not hazard:
        raise HTTPException(status_code=404, detail="Hazard not found")

    update_data = hazard_in.model_dump(exclude_unset=True)  # тільки ті, що передані
    for key, value in update_data.items():
        setattr(hazard, key, value)

    db.add(hazard)
    db.commit()
    db.refresh(hazard)
    return hazard

# (DEV ONLY!)
@router.delete("/clear/", status_code=status.HTTP_204_NO_CONTENT)
def clear_hazards(db: Session = Depends(get_db)):
    db.query(models.Hazard).delete()
    db.commit()
    return None
