from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime, Enum, BigInteger, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, UUID

Base = declarative_base()

# Association table for many-to-many relationship between Shipments and Flour
shipment_flour_association = Table(
    'shipment_flour_association', Base.metadata,
    Column('shipment_id', Integer, ForeignKey('shipments.ShipmentID')),
    Column('flour_id', Integer, ForeignKey('flour.FlourID'))
)

class SessionData(Base):
    __tablename__ = "sessions"

    session_id = Column(String(36), unique=True, primary_key=True)
    user_id = Column(String(36), ForeignKey('users.UserID'))

class RoleModel(Base):
    __tablename__ = "roles"
    
    RoleID = Column(Integer, primary_key=True)
    RoleName = Column(String(50))

class User(Base):
    __tablename__ = "users"

    UserID = Column(String(36), primary_key=True) 
    Username = Column(String(50))
    Email = Column(String(100), unique=True)
    PhoneNumber = Column(BigInteger)
    Password = Column(String(100))
    RoleID = Column(Integer, ForeignKey('roles.RoleID'))
    role = relationship("RoleModel")

class Location(Base):
    __tablename__ = "locations"

    LocationID = Column(Integer, primary_key=True, autoincrement=True)
    LocationAddress = Column(String(100))
    Latitude = Column(Float, nullable=False)
    Longitude = Column(Float, nullable=False)

class Courier(Base):
    __tablename__ = "couriers"
    
    CourierID = Column(Integer, primary_key=True, autoincrement=True) 
    CourierName = Column(String(50), nullable=False)

class WetLeaves(Base):
    __tablename__ = "wet_leaves"

    WetLeavesID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(String(36), ForeignKey("users.UserID"))
    Weight = Column(Float)
    ReceivedTime = Column(DateTime)
    Status = Column(String(50), default="Awaiting")

class DryLeaves(Base):
    __tablename__ = "dry_leaves"

    DryLeavesID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(String(36), ForeignKey("users.UserID"))
    WetLeavesID = Column(Integer, ForeignKey("wet_leaves.WetLeavesID"))
    Processed_Weight = Column(Float)
    Expiration = Column(DateTime, nullable=True)
    Status = Column(String(50), default="Awaiting")

class Flour(Base):
    __tablename__ = "flour"

    FlourID = Column(Integer, primary_key=True, autoincrement=True)
    DryLeavesID = Column(Integer, ForeignKey("dry_leaves.DryLeavesID"))
    UserID = Column(String(36), ForeignKey("users.UserID"))
    Flour_Weight = Column(Float)
    Expiration = Column(DateTime, nullable=True)
    Status = Column(String(50), default="Awaiting")

class Shipment(Base):
    __tablename__ = "shipments"

    ShipmentID = Column(Integer, primary_key=True, autoincrement=True)
    CourierID = Column(Integer, ForeignKey("couriers.CourierID"))
    UserID = Column(String(36), ForeignKey("users.UserID"))
    ShipmentQuantity = Column(Integer)
    ShipmentDate = Column(DateTime, nullable=True)
    Check_in_Date = Column(DateTime, nullable=True)
    Check_in_Quantity = Column(Integer, nullable=True)
    Harbor_Reception_File = Column(String(50), nullable=True)
    Rescalled_Weight = Column(Float, nullable=True)
    Rescalled_Date = Column(DateTime, nullable=True)
    Centra_Reception_File = Column(String(50), nullable=True)
    
    flours = relationship("Flour", secondary=shipment_flour_association, backref="shipments")