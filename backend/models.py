from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ============ MEMBER MODELS ============

class MemberBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre completo")
    nickname: Optional[str] = Field(None, max_length=50, description="Apodo o nombre de usuario")
    email: Optional[EmailStr] = Field(None, description="Email (opcional, no sensible)")
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono (opcional)")
    city: Optional[str] = Field(None, max_length=100, description="Ciudad de residencia")
    description: Optional[str] = Field(None, max_length=500, description="Descripción personal")
    birthday: Optional[str] = Field(None, description="Fecha de cumpleaños (YYYY-MM-DD)")
    join_date: Optional[str] = Field(None, description="Fecha de ingreso al club (YYYY-MM-DD)")
    car_year: Optional[int] = Field(None, ge=1980, le=2030, description="Año del vehículo")
    car_model: Optional[str] = Field(None, max_length=50, description="Modelo específico del Jetta")
    car_color: Optional[str] = Field(None, max_length=50, description="Color del vehículo")
    is_active: Optional[bool] = Field(True, description="Estado activo/inactivo del miembro")

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    nickname: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    city: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    birthday: Optional[str] = Field(None, description="Fecha de cumpleaños (YYYY-MM-DD)")
    join_date: Optional[str] = Field(None, description="Fecha de ingreso al club (YYYY-MM-DD)")
    car_year: Optional[int] = Field(None, ge=1980, le=2030)
    car_model: Optional[str] = Field(None, max_length=50)
    car_color: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None

class Member(MemberBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ============ CITY MODELS ============

class CityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre de la ciudad")
    is_active: Optional[bool] = Field(True, description="Ciudad activa/inactiva")

class CityCreate(CityBase):
    pass

class City(CityBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ============ CONTACT MODELS ============

class ContactBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del contacto")
    category: str = Field(..., min_length=1, max_length=50, description="Categoría (latonería, lujos, etc.)")
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")
    email: Optional[EmailStr] = Field(None, description="Email de contacto")
    address: Optional[str] = Field(None, max_length=200, description="Dirección")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del servicio")
    website: Optional[str] = Field(None, max_length=200, description="Sitio web")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Calificación (1-5)")

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

