from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class RoleBase(BaseModel):
    RoleName: str
    
class SessionData(BaseModel):
    user_id: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    RoleID: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    Username: str
    Email: str
    PhoneNumber: Optional[int]
    RoleID: int

class UserCreate(UserBase):
    Password: str

class UserUpdate(BaseModel):
    Password: Optional[str] = None
    Username: Optional[str] = None
    Email: Optional[str] = None
    
class User(UserBase):
    UserID: UUID4
    role: Role

    class Config:
        orm_mode = True

class LocationBase(BaseModel):
    LocationAddress: str
    Latitude: float
    Longitude: float

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    LocationID: int

    class Config:
        orm_mode = True

class CourierBase(BaseModel):
    CourierName: str

class CourierCreate(CourierBase):
    pass

class Courier(CourierBase):
    CourierID: int

    class Config:
        orm_mode = True

class DryLeavesBase(BaseModel):
    UserID: UUID4
    WetLeavesID: int
    Processed_Weight: Optional[float]
    Expiration: Optional[datetime]

class DryLeavesCreate(DryLeavesBase):
    pass

class DryLeaves(DryLeavesBase):
    DryLeavesID: int

    class Config:
        orm_mode = True

class DryLeavesUpdate(BaseModel):
    Weight: float

class WetLeavesBase(BaseModel):
    UserID: UUID4
    Weight: float
    ReceivedTime: datetime

class WetLeavesCreate(WetLeavesBase):
    pass

class WetLeaves(WetLeavesBase):
    WetLeavesID: int

    class Config:
        orm_mode = True

class WetLeavesUpdate(BaseModel):
    Weight: float

class FlourBase(BaseModel):
    UserID: UUID4
    DryLeavesID: int
    WetLeavesID: int
    Flour_Weight: float
    Expiration: Optional[datetime]

class FlourCreate(FlourBase):
    pass

class Flour(FlourBase):
    FlourID: int

    class Config:
        orm_mode = True

class FlourUpdate(BaseModel):
    Weight: float

class ShipmentBase(BaseModel):
    CourierID: int
    UserID: UUID4
    FlourID: int
    ShipmentQuantity: int
    ShipmentDate: datetime
    Check_in_Date: Optional[datetime]
    Check_in_Quantity: Optional[int]
    Harbor_Reception_File: Optional[str]
    Rescalled_Weight: Optional[float]
    Rescalled_Date: Optional[datetime]
    Centra_Reception_File: Optional[str]


class ShipmentCreate(ShipmentBase):
    pass

class ShipmentUpdate(BaseModel):
    CourierID: Optional[int] = None
    FlourID: Optional[int] = None
    ShipmentQuantity: Optional[int] = None
    Check_in_Quantity: Optional[int] = None
    Harbor_Reception_File: Optional[str] = None
    Rescalled_Weight: Optional[float] = None
    Centra_Reception_File: Optional[str] = None
    
class Shipment(ShipmentBase):
    ShipmentID: int

    class Config:
        orm_mode = True
