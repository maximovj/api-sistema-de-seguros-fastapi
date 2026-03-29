from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Optional, List

# Customer Schemas
class CustomerBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=200)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[str] = Field(None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=200)

class Customer(CustomerBase):
    id: int
    full_name: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Asset Schemas
class AssetBase(BaseModel):
    asset_type: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    value: float = Field(..., gt=0)
    serial_number: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=100)

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    asset_type: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    value: Optional[float] = Field(None, gt=0)
    serial_number: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=100)

class Asset(AssetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Policy Schemas
class PolicyBase(BaseModel):
    policy_number: str = Field(..., min_length=1, max_length=50)
    policy_type: str = Field(..., min_length=1, max_length=50)
    start_date: datetime
    end_date: datetime
    premium_amount: float = Field(..., gt=0)
    coverage_amount: float = Field(..., gt=0)
    status: Optional[str] = Field("active", pattern="^(active|expired|cancelled)$")

class PolicyCreate(PolicyBase):
    customer_id: int
    asset_ids: Optional[List[int]] = []

class PolicyUpdate(BaseModel):
    policy_type: Optional[str] = Field(None, min_length=1, max_length=50)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    premium_amount: Optional[float] = Field(None, gt=0)
    coverage_amount: Optional[float] = Field(None, gt=0)
    status: Optional[str] = Field(None, pattern="^(active|expired|cancelled)$")

class Policy(PolicyBase):
    id: int
    customer_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    customer: Optional[Customer] = None
    assets: List[Asset] = []
    
    model_config = ConfigDict(from_attributes=True)

# Payment Schemas
class PaymentBase(BaseModel):
    payment_date: datetime
    amount: float = Field(..., gt=0)
    payment_method: str = Field(..., min_length=1, max_length=50)
    transaction_id: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field("pending", pattern="^(pending|completed|failed)$")

class PaymentCreate(PaymentBase):
    policy_id: int

class PaymentUpdate(BaseModel):
    payment_date: Optional[datetime] = None
    amount: Optional[float] = Field(None, gt=0)
    payment_method: Optional[str] = Field(None, min_length=1, max_length=50)
    transaction_id: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, pattern="^(pending|completed|failed)$")

class Payment(PaymentBase):
    id: int
    policy_id: int
    created_at: datetime
    policy: Optional[Policy] = None
    
    model_config = ConfigDict(from_attributes=True)