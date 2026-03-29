from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/payments", response_model=schemas.Payment, status_code=status.HTTP_201_CREATED)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    """Crear un nuevo pago"""
    # Verificar que la póliza existe
    policy = db.query(models.Policy).filter(models.Policy.id == payment.policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Póliza no encontrada")
    
    # Verificar transaction_id único
    if payment.transaction_id:
        existing = db.query(models.Payment).filter(
            models.Payment.transaction_id == payment.transaction_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="ID de transacción ya existe")
    
    db_payment = models.Payment(**payment.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/payments", response_model=List[schemas.Payment])
def get_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos los pagos"""
    payments = db.query(models.Payment).offset(skip).limit(limit).all()
    return payments

@router.get("/payments/{payment_id}", response_model=schemas.Payment)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """Obtener un pago por ID"""
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return payment

@router.get("/policies/{policy_id}/payments", response_model=List[schemas.Payment])
def get_policy_payments(policy_id: int, db: Session = Depends(get_db)):
    """Obtener todos los pagos de una póliza"""
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Póliza no encontrada")
    return policy.payments

@router.put("/payments/{payment_id}", response_model=schemas.Payment)
def update_payment(payment_id: int, payment_update: schemas.PaymentUpdate, db: Session = Depends(get_db)):
    """Actualizar un pago"""
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    update_data = payment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_payment, field, value)
    
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.delete("/payments/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    """Eliminar un pago"""
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    db.delete(db_payment)
    db.commit()
    return None