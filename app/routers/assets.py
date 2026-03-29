from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/assets", response_model=schemas.Asset, status_code=status.HTTP_201_CREATED)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    """Crear un nuevo bien"""
    # Verificar serial number único
    if asset.serial_number:
        existing = db.query(models.Asset).filter(
            models.Asset.serial_number == asset.serial_number
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Número de serie ya existe")
    
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/assets", response_model=List[schemas.Asset])
def get_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos los bienes"""
    assets = db.query(models.Asset).offset(skip).limit(limit).all()
    return assets

@router.get("/assets/{asset_id}", response_model=schemas.Asset)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    """Obtener un bien por ID"""
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Bien no encontrado")
    return asset

@router.put("/assets/{asset_id}", response_model=schemas.Asset)
def update_asset(asset_id: int, asset_update: schemas.AssetUpdate, db: Session = Depends(get_db)):
    """Actualizar un bien"""
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Bien no encontrado")
    
    update_data = asset_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_asset, field, value)
    
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.delete("/assets/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    """Eliminar un bien"""
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Bien no encontrado")
    
    db.delete(db_asset)
    db.commit()
    return None