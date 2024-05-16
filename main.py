from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import uuid

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#roles
@app.post("/roles/", response_model=schemas.Role,tags=["Roles"])
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return crud.create_role(db=db, role=role)

@app.get("/get_roles/", response_model=List[schemas.RoleBase],tags=["Roles"])
def get_roles(db: Session = Depends(get_db)):
    return crud.get_roles(db=db)

# users
@app.post('/users/', response_model=schemas.User,tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if role exists, if not, return error
    role = crud.get_role(db, role_id=user.RoleID)
    if not role:
        raise HTTPException(status_code=400, detail="Role does not exist")

    # Create a new user
    return crud.create_user(db=db, user=user)

@app.get("/get_users/", response_model=List[schemas.User],tags=["Users"])
def get_users(limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, limit=limit)
    return users

@app.get("/get_users_by_id/", response_model=List[schemas.User],tags=["Users"])
def get_user(role_id: int,db: Session = Depends(get_db)):
    role = crud.get_user_by_role(db, role_id)
    if not role:
     raise HTTPException(status_code=400, detail="Role does not exist")
    else:
        users = crud.get_user_by_role(db,role_id)
        return users

@app.put('/users/{user_id}', response_model=schemas.UserUpdate, tags=["Users"])
def update_user(user_id: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db=db, user_id=user_id, user_update=user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return updated_user

@app.delete("/delete_user_by_id", response_class=JSONResponse,tags=["Users"])
def delete_user(user_id: str ,db: Session = Depends(get_db)):
    deleted = crud.delete_user_by_id(db, user_id)
    if deleted:
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not found or deletion failed"}
    
#courier
@app.post("/create_couriers/", response_model=schemas.Courier,tags=["Courier"])
def create_courier(courier: schemas.CourierCreate, db: Session = Depends(get_db)):
    return crud.create_courier(db, courier)

@app.get("/get_courier/", response_model=List[schemas.Courier],tags=["Courier"])
def get_courier(db: Session = Depends(get_db)):
    return crud.get_couriers(db)

@app.delete("/get_courier/", response_class=JSONResponse,tags=["Courier"])
def delete_courier(courier_id: int, db: Session = Depends(get_db)):
    delete = crud.delete_courier(db=db, courier_id=courier_id)
    if delete:
        return {"message": "Courier deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Courier not found or deletion failed")
#wet_leaves
@app.post("/wet_leaves/", response_model=schemas.WetLeaves,tags=["WetLeaves"])
def create_wet_leaves(wet_leaves: schemas.WetLeavesCreate, db: Session = Depends(get_db)):
    return crud.create_wet_leaves(db=db, wet_leaves=wet_leaves)

@app.get("/wet_leaves/", response_model=List[schemas.WetLeaves],tags=["WetLeaves"])
def get_wet_leaves(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_wet_leaves(db=db, limit=limit)

@app.get("/wet_leaves/{wet_leaves_id}", response_model= schemas.WetLeaves,tags=["WetLeaves"])
def get_wet_leaves_id(wet_leaves_id: int,db: Session = Depends(get_db)):
    wet_leaves = crud.get_wet_leaves_by_id( db=db, wet_leaves_id =wet_leaves_id)
    if not wet_leaves:
        raise HTTPException(status_code=404, detail="wet leaves not found")
    return wet_leaves

@app.delete("/wet_leaves/{wet_leaves_id}", response_class=JSONResponse,tags=["WetLeaves"])
def delete_wet_leaves_by_id(wet_leaves_id: int, db: Session = Depends(get_db)):
    delete = crud.delete_wet_leaves_by_id( db=db, wet_leaves_id=wet_leaves_id)
    if delete:
        return{"message" : "wet leaves deleted successfully"}
    else:
        return{"message" : "wet leaves not found or deletion failed"}

@app.put("/wet_leaves/{wet_leaves_id}", response_model=schemas.WetLeaves,tags=["WetLeaves"])
def update_wet_leaves(wet_leaves_id: int, wet_leaves: schemas.WetLeavesUpdate, db: Session= Depends(get_db)):
    update_wet_leaves = crud.update_wet_leaves(db=db, wet_leaves_id=wet_leaves_id, wet_leaves_update= wet_leaves)
    if not update_wet_leaves:
        raise HTTPException(status_code=404, detail="wet leaves not found")
    return update_wet_leaves
 
# dry leaves
@app.post("/dry_leaves/", response_model=schemas.DryLeaves,tags=["DryLeaves"])
def create_dry_leaves(dry_leaves: schemas.DryLeavesCreate, db: Session = Depends(get_db)):
    return crud.create_dry_leaves(db=db, dry_leaves=dry_leaves)

@app.get("/get_dry_leaves/", response_model=List[schemas.DryLeaves],tags=["DryLeaves"])
def get_dry_leaves(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_dry_leaves(db=db, limit=limit)

@app.get("/dry_leaves/{dry_leaves_id}", response_model= schemas.DryLeaves,tags=["DryLeaves"])
def get_dry_leaves_id(dry_leaves_id: int,db: Session = Depends(get_db)):
    dry_leaves = crud.get_dry_leaves_by_id( db=db, dry_leaves_id = dry_leaves_id)
    if not dry_leaves:
        raise HTTPException(status_code=404, detail="dry leaves not found")
    return dry_leaves

@app.delete("/dry_leaves/{dry_leaves_id}", response_class=JSONResponse,tags=["DryLeaves"])
def delete_dry_leaves_by_id(dry_leaves_id: int, db: Session = Depends(get_db)):
    delete = crud.delete_dry_leaves_by_id( db=db, dry_leaves_id=dry_leaves_id)
    if delete:
        return{"message" : "dry leaves deleted successfully"}
    else:
        return{"message" : "dry leaves not found or deletion failed"}
    
@app.put("/dry_leaves/{dry_leaves_id}", response_model=schemas.DryLeaves,tags=["DryLeaves"])
def update_dry_leaves(dry_leaves_id: int, dry_leaves: schemas.DryLeavesUpdate, db: Session= Depends(get_db)):
    update_dry_leaves = crud.update_dry_leaves(db=db, dry_leaves_id=dry_leaves_id, dry_leaves_update= dry_leaves)
    if not update_dry_leaves:
        raise HTTPException(status_code=404, detail="dry leaves not found")
    return update_dry_leaves

#flour
@app.post("/flour/", response_model=schemas.Flour,tags=["Flour"])
def create_flour(flour: schemas.FlourCreate, db: Session = Depends(get_db)):
    return crud.create_flour(db=db, flour=flour)

@app.get("/flour/", response_model=List[schemas.Flour],tags=["Flour"])
def get_flour(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_flour(db=db,limit=limit)

@app.get("/flour/{flour_id}", response_model= schemas.Flour,tags=["Flour"])
def get_flour_by_id(flour_id: int,db: Session = Depends(get_db)):
    flour = crud.get_flour_by_id( db=db, flour_id = flour_id)
    if not flour:
        raise HTTPException(status_code=404, detail="flour not found")
    else:
        return flour
 
@app.delete("/flour/{flour_id}", response_class=JSONResponse,tags=["Flour"])
def delete_flour_by_id(flour_id: int, db: Session = Depends(get_db)):
    delete = crud.delete_flour_leaves_by_id( db=db, flour_id=flour_id)
    if delete:
        return{"message" : "flour deleted successfully"}
    else:
        return{"message" : "flour not found or deletion failed"}
    
@app.put("/flour/{wet_leaves_id}", response_model=schemas.Flour,tags=["Flour"])
def update_flour(flour_id: int, flour: schemas.FlourUpdate, db: Session= Depends(get_db)):
    update_flour = crud.update_flour(db=db, flour_id=flour_id, flour_update= flour)
    if not update_flour:
        raise HTTPException(status_code=404, detail="flour not found")
    return update_flour


#shipment
@app.post('/shipments', response_model=schemas.Shipment,tags=["Shipment"])
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    return crud.create_shipment(db=db, shipment=shipment)

@app.get('/shipments', response_model=List[schemas.Shipment],tags=["Shipment"])
def get_shipment(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_shipment(db=db, limit=limit)

@app.get('/shipments/{shipment_id}', response_model=schemas.Shipment,tags=["Shipment"])
def get_shipment_by_id(shipment_id:int, db: Session = Depends(get_db)):
    shipment = crud.get_shipment_by_id(db=db,shipment_id=shipment_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="shipment not found")
    return shipment

@app.put("/shipments/{shipment_id}", response_model=schemas.Shipment,tags=["Shipment"])
def update_shipment(shipment_id: int, shipment_update: schemas.ShipmentUpdate, db: Session = Depends(get_db)):
    db_shipment = crud.update_shipment(db, shipment_id, shipment_update)
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return db_shipment

@app.delete('/shipments/{shipment_id}',tags=["Shipment"])
def delete_shipment_by_id(shipment_id:int,db: Session = Depends(get_db)):
    delete = crud.delete_shipment_by_id(db=db,shipment_id=shipment_id)
    if delete:
        return{"message" : "shipment deleted successfully"}
    else:
        return{"message" : "shipment not found or deletion failed"}

#location    
@app.post('/location', response_model=schemas.Location,tags=["Location"])
def create_location(location:schemas.LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db,location=location)

@app.get('/location', response_model=List[schemas.Location],tags=["Location"])
def get_location(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_location(db=db, limit=limit)

@app.get('/location/{location_id}', response_model=schemas.Location,tags=["Location"])
def get_location_by_id(location_id:int, db: Session = Depends(get_db)):
    location = crud.get_location_by_id(db=db,location_id=location_id)
    if not location:
        raise HTTPException(status_code=404, detail="location not found")
    return location

@app.delete('/location/{location_id}',tags=["Location"])
def delete_location_by_id(location_id:int,db: Session = Depends(get_db)):
    delete = crud.delete_location_by_id(db=db,location_id=location_id)
    if delete:
        return{"message" : "location deleted successfully"}
    else:
        return{"message" : "location not found or deletion failed"}