from app.database import SessionLocal, engine
from app import models
from datetime import datetime, timedelta

# Crear tablas
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Datos de prueba
try:
    # Clientes
    customers = [
        models.Customer(first_name="Ana", last_name="García", email="ana@example.com", phone="555-0001", address="Av. Reforma 123"),
        models.Customer(first_name="Carlos", last_name="López", email="carlos@example.com", phone="555-0002", address="Insurgentes 456"),
        models.Customer(first_name="María", last_name="Martínez", email="maria@example.com", phone="555-0003", address="Polanco 789"),
    ]
    db.add_all(customers)
    db.commit()
    
    # Bienes
    assets = [
        models.Asset(asset_type="Auto", description="Honda Civic", value=280000, serial_number="ABC789", location="CDMX"),
        models.Asset(asset_type="Casa", description="Casa habitación", value=1800000, serial_number="CASA001", location="Estado de México"),
        models.Asset(asset_type="Joya", description="Reloj Rolex", value=120000, serial_number="RLX001", location="CDMX"),
    ]
    db.add_all(assets)
    db.commit()
    
    # Pólizas
    policies = [
        models.Policy(
            policy_number="POL001",
            policy_type="Auto",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=365),
            premium_amount=5000,
            coverage_amount=280000,
            customer_id=customers[0].id,
            assets=[assets[0]]
        ),
        models.Policy(
            policy_number="POL002",
            policy_type="Hogar",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=365),
            premium_amount=8000,
            coverage_amount=1800000,
            customer_id=customers[1].id,
            assets=[assets[1]]
        ),
    ]
    db.add_all(policies)
    db.commit()
    
    # Pagos
    payments = [
        models.Payment(
            payment_date=datetime.now(),
            amount=5000,
            payment_method="Transferencia",
            transaction_id="TXN001",
            status="completed",
            policy_id=policies[0].id
        ),
        models.Payment(
            payment_date=datetime.now(),
            amount=8000,
            payment_method="Tarjeta",
            transaction_id="TXN002",
            status="completed",
            policy_id=policies[1].id
        ),
    ]
    db.add_all(payments)
    db.commit()
    
    print("✅ Datos de prueba insertados correctamente")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()