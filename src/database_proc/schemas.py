# schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str
    trust_level: Optional[int] = 0
    points: Optional[int] = 0
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    trust_level: Optional[int] = None
    points: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    password: Optional[str] = Field(None, min_length=6)

class UserOut(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class HazardBase(BaseModel):
    problem: str
    description: Optional[str] = None
    delay_sec: Optional[int] = None
    vehicle_id: Optional[str] = None
    trip_id: Optional[str] = None
    route_id: Optional[str] = None
    source: str = "user"
    reporter_user_id: Optional[UUID] = None
    severity_num: int = 0
    confidence: float = 0.5
    latitude: float = Field(..., alias="lat")
    longitude: float = Field(..., alias="lon")

    model_config = {
        "populate_by_name": True,  # 👈 дозволяє фронту слати lat/lon
        "from_attributes": True
    }


class HazardCreate(HazardBase):
    pass

class HazardOut(HazardBase):
    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    valid_until: Optional[datetime]

    model_config = {
        "from_attributes": True
    }

class HazardUpdate(BaseModel):
    problem: Optional[str] = None
    description: Optional[str] = None
    delay_sec: Optional[int] = None
    vehicle_id: Optional[str] = None
    trip_id: Optional[str] = None
    route_id: Optional[str] = None
    source: Optional[str] = None
    severity_num: Optional[int] = None
    confidence: Optional[float] = None
    latitude: Optional[float] = Field(None, alias="lat")
    longitude: Optional[float] = Field(None, alias="lon")
    status: Optional[str] = None
    valid_until: Optional[str] = None

    model_config = {
        "populate_by_name": True
    }


class Point(BaseModel):
    lat: float
    lng: float
