from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/policies", response_model=schemas.Policy, status_code=status.HTTP_201_CREATED)
def create_policy(policy: schemas.PolicyCreate, db: Session = Depends(get_db)):
    """Crear una nueva póliza"""
    # Verificar que el cliente existe
    customer = db.query(models.Customer).filter(models.Customer.id == policy.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Verificar que el número de póliza no exista
    existing_policy = db.query(models.Policy).filter(
        models.Policy.policy_number == policy.policy_number
    ).first()
    if existing_policy:
        raise HTTPException(status_code=400, detail="Número de póliza ya existe")
    
    # Crear póliza
    db_policy = models.Policy(**policy.model_dump(exclude={'asset_ids'}))
    db.add(db_policy)
    db.flush()  # Para obtener el ID
    
    # Agregar assets
    if policy.asset_ids:
        assets = db.query(models.Asset).filter(models.Asset.id.in_(policy.asset_ids)).all()
        db_policy.assets.extend(assets)
    
    db.commit()
    db.refresh(db_policy)
    return db_policy

@router.get("/policies", response_model=List[schemas.Policy])
def get_policies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todas las pólizas"""
    policies = db.query(models.Policy).offset(skip).limit(limit).all()
    return policies

@router.get("/policies/{policy_id}", response_model=schemas.Policy)
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    """Obtener una póliza por ID"""
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Póliza no encontrada")
    return policy

@router.put("/policies/{policy_id}", response_model=schemas.Policy)
def update_policy(policy_id: int, policy_update: schemas.PolicyUpdate, db: Session = Depends(get_db)):
    """Actualizar una póliza"""
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not db_policy:
        raise HTTPException(status_code=404, detail="Póliza no encontrada")
    
    update_data = policy_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_policy, field, value)
    
    db.commit()
    db.refresh(db_policy)
    return db_policy

@router.post("/policies/{policy_id}/assets/{asset_id}")
def add_asset_to_policy(policy_id: int, asset_id: int, db: Session = Depends(get_db)):
    """Agregar un bien a una póliza"""
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Póliza no encontrada")
    
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Bien no encontrado")
    
    if asset not in policy.assets:
        policy.assets.append(asset)
        db.commit()
    
    return {"message": "Bien agregado a la póliza"}

@router.delete("/policies/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_policy(policy_id: int, db: Session = Depends(get_db)):
    """Eliminar una póliza"""
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not db_policy:
        raise HTTPException(status_code=404, detail="Póliza no encontrada")
    
    db.delete(db_policy)
    db.commit()
    return None