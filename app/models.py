from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Tabla intermedia para relación muchos a muchos entre Policy y Asset
policy_asset = Table(
    'policy_asset',
    Base.metadata,
    Column('policy_id', Integer, ForeignKey('policies.id'), primary_key=True),
    Column('asset_id', Integer, ForeignKey('assets.id'), primary_key=True)
)

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    address = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación: Un cliente tiene muchas pólizas
    policies = relationship("Policy", back_populates="customer", cascade="all, delete-orphan")
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Policy(Base):
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_number = Column(String(50), unique=True, index=True, nullable=False)
    policy_type = Column(String(50), nullable=False)  # Auto, Hogar, Vida, Salud
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    premium_amount = Column(Float, nullable=False)  # Prima
    coverage_amount = Column(Float, nullable=False)  # Monto asegurado
    status = Column(String(20), default="active")  # active, expired, cancelled
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    customer = relationship("Customer", back_populates="policies")
    assets = relationship("Asset", secondary=policy_asset, back_populates="policies")
    payments = relationship("Payment", back_populates="policy", cascade="all, delete-orphan")

class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_type = Column(String(50), nullable=False)  # Auto, Casa, Joya, etc.
    description = Column(String(200))
    value = Column(Float, nullable=False)
    serial_number = Column(String(100), unique=True, index=True)
    location = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación muchos a muchos con pólizas
    policies = relationship("Policy", secondary=policy_asset, back_populates="assets")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    payment_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)  # Tarjeta, Transferencia, Efectivo
    transaction_id = Column(String(100), unique=True, index=True)
    status = Column(String(20), default="pending")  # pending, completed, failed
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación
    policy = relationship("Payment", back_populates="payments")