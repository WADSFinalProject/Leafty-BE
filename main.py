from fastapi import FastAPI, HTTPException, Depends, Request, Response, status, __version__
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import uuid
from BasicVerifier import BasicVerifier
from fastapi_sessions.backends.implementations import InMemoryBackend
from schemas import User, SessionData
from uuid import UUID, uuid4
from fastapi.middleware.cors import CORSMiddleware
import crud
import models
import schemas
import bcrypt
from typing import List
from database import SessionLocal, engine
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.session_verifier import SessionVerifier
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

backend = InMemoryBackend[UUID, SessionData]()

verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=backend,
    auth_http_exception=HTTPException(status_code=404, detail="invalid session"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

cookie_params = CookieParameters(
    secure=True,  # Ensures cookie is sent over HTTPS
    httponly=True,
    samesite="none"  # Allows the cookie to be sent with cross-origin requests
)

cookie = SessionCookie(
    cookie_name="session",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)

def format_large_number(number):
    if number < 1000:
        return str(number)
    elif number < 1_000_000:
        return f"{number // 1000},{number % 1000}k"
    else:
        return f"{number // 1_000_000},{(number // 1000) % 1000}m"
    
# Sessions
@app.post("/create_session/{user_id}", tags=["Sessions"])
async def create_session(user_id: str, response: Response, db: Session = Depends(get_db)):
    session = uuid4()
    user = crud.get_user_by_id(db, user_id)
    data = SessionData(user_id=user_id, user_role=user.RoleID, user_email=user.Email)

    await backend.create(session, data)
    cookie.attach_to_response(response, session)

    response.headers["Set-Cookie"] += "; SameSite=None"


    crud.create_session(db, session, user_id)

    return f"created session for {user_id}"


@app.get("/whoami", dependencies=[Depends(cookie)], tags=["Sessions"])
async def whoami(session_data: SessionData = Depends(verifier)):
    return session_data


@app.delete("/delete_session", dependencies=[Depends(cookie)], tags=["Sessions"])
async def del_session(response: Response, session_id: UUID = Depends(cookie), db: Session = Depends(get_db)):
    await backend.delete(session_id)
    cookie.delete_from_response(response)

    response.headers["Set-Cookie"] += "; SameSite=None"

    crud.delete_session(db)

    return "deleted session"

# Roles
@app.post("/role/post", response_model=schemas.Role, tags=["Roles"])
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return crud.create_role(db=db, role=role)

@app.get("/roles/get", response_model=List[schemas.RoleBase], tags=["Roles"])
def get_roles(db: Session = Depends(get_db)):
    return crud.get_roles(db=db)

@app.delete("/roles/delete/{role_id}", response_class=JSONResponse, tags=["Roles"])
def delete_user(role_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_role_by_id(db, role_id)
    if deleted:
        return {"message": "Role deleted successfully"}
    else:
        return {"message": "Role not found or deletion failed"}

# Users
@app.post('/user/post', response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if role exists, if not, return error
    role = crud.get_role(db, role_id=user.RoleID)
    if not role:
        raise HTTPException(status_code=400, detail="Role does not exist")

    # Create a new user
    return crud.create_user(db=db, user=user)

@app.get("/user/get", response_model=List[schemas.User], tags=["Users"])
def get_users(limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, limit=limit)
    return users

@app.get("/user/get_role/{role_id}", response_model=List[schemas.User], tags=["Users"])
def get_user(role_id: int, db: Session = Depends(get_db)):
    role = crud.get_user_by_role(db, role_id)
    if not role:
        raise HTTPException(status_code=400, detail="Role does not exist")
    else:
        users = crud.get_user_by_role(db, role_id)
        return users

@app.get("/user/get_user/{user_id}", response_model=schemas.User, tags=["Users"])
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    return user

@app.get("/user/get_user_email/{email}", response_model=schemas.User, tags=["Users"])
def get_user(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    return user

@app.put('/user/put/{user_id}', response_model=schemas.UserUpdate, tags=["Users"])
def update_user(user_id: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db=db, user_id=user_id, user_update=user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    return updated_user

@app.put('/user/update_role/{user_id}', response_model=schemas.User, tags=["Users"])
def update_user_role(user_id: str, role_update: schemas.UserRoleUpdate, db: Session = Depends(get_db)):
    role_name_to_id = {
        "Centra": 1,
        "Harbor": 2,
        "Company": 3,
        "Admin": 4,
        "Unverified": 5,
        "Rejected": 6
    }
    role_id = role_name_to_id.get(role_update.RoleName)
    print(role_id)
    if role_id is None:
        raise HTTPException(status_code=400, detail="Invalid role name")

    updated_user = crud.update_user_role(db=db, user_id=user_id, role_id=role_id)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User does not exist or role does not exist")
    return updated_user

@app.delete("/user/delete/{user_id}", response_class=JSONResponse, tags=["Users"])
def delete_user(user_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_user_by_id(db, user_id)
    if deleted:
        return {"message": "User deleted successfully"}
    else:
        return {"message": "User not found or deletion failed"}

# Courier
@app.post("/courier/post", response_model=schemas.Courier, tags=["Courier"])
def create_courier(courier: schemas.CourierCreate, db: Session = Depends(get_db)):
    return crud.create_courier(db, courier)

@app.get("/courier/get", response_model=List[schemas.Courier], tags=["Courier"])
def get_courier(db: Session = Depends(get_db)):
    return crud.get_couriers(db)

@app.get("/courier/get/{courier_id}", response_model=schemas.Courier, tags=["Courier"])
def get_courier_by_courier_id(courier_id:int, db: Session = Depends(get_db)):
    return crud.get_courier_by_id(db, courier_id)   

@app.delete("/courier/delete/{courier_id}", response_class=JSONResponse, tags=["Courier"])
def delete_courier(courier_id: int, db: Session = Depends(get_db)):
    delete = crud.delete_courier(db=db, courier_id=courier_id)
    if delete:
        return {"message": "Courier deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Courier not found or deletion failed")

# Wet Leaves
@app.post("/wetLeaves/post", response_model=schemas.WetLeaves, tags=["WetLeaves"])
def create_wet_leaves(wet_leaves: schemas.WetLeavesCreate, db: Session = Depends(get_db)):
    return crud.create_wet_leaves(db=db, wet_leaves=wet_leaves)

@app.get("/wetleaves/get", response_model=List[schemas.WetLeaves], tags=["WetLeaves"])
def get_wet_leaves(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_wet_leaves(db=db, limit=limit)

@app.get("/wetleaves/get/{wet_leaves_id}", response_model=schemas.WetLeaves, tags=["WetLeaves"])
def get_wet_leaves_id(wet_leaves_id: int, db: Session = Depends(get_db)):
    wet_leaves = crud.get_wet_leaves_by_id(db=db, wet_leaves_id=wet_leaves_id)
    if not wet_leaves:
        raise HTTPException(status_code=404, detail="wet leaves not found")
    return wet_leaves

@app.get("/wetleaves/get_by_user/{user_id}", response_model=List[schemas.WetLeaves], tags=["WetLeaves"])
def get_wet_leaves_by_user(user_id: str, db: Session = Depends(get_db)):
    wet_leaves = crud.get_wet_leaves_by_user_id(db, user_id)
    if not wet_leaves:
        raise HTTPException(status_code=404, detail="wet leaves not found")
    return wet_leaves

@app.delete("/wetleaves/delete/{wet_leaves_id}", response_class=JSONResponse, tags=["WetLeaves"])
def delete_wet_leaves_by_id(wet_leaves_id: int, db: Session = Depends(get_db)):
    delete = crud.delete_wet_leaves_by_id(db=db, wet_leaves_id=wet_leaves_id)
    if delete:
        return {"message": "wet leaves deleted successfully"}
    else:
        return {"message": "wet leaves not found or deletion failed"}

@app.put("/wetleaves/put/{wet_leaves_id}", response_model=schemas.WetLeaves, tags=["WetLeaves"])
def update_wet_leaves(wet_leaves_id: int, wet_leaves: schemas.WetLeavesUpdate, db: Session = Depends(get_db)):
    update_wet_leaves = crud.update_wet_leaves(db=db, wet_leaves_id=wet_leaves_id, wet_leaves_update=wet_leaves)
    if not update_wet_leaves:
        raise HTTPException(status_code=404, detail="wet leaves not found")
    return update_wet_leaves

@app.put("/wetleaves/update_status/{wet_leaves_id}", response_model=schemas.WetLeaves, tags=["WetLeaves"])
def update_wet_leaves_status(wet_leaves_id: int, status_update: schemas.WetLeavesStatusUpdate, db: Session = Depends(get_db)):
    updated_wet_leaves = crud.update_wet_leaves_status(db=db, wet_leaves_id=wet_leaves_id, status_update=status_update)
    if not updated_wet_leaves:
        raise HTTPException(status_code=404, detail="wet leaves not found")
    return updated_wet_leaves

# Dry Leaves
@app.post("/dryleaves/post", response_model=schemas.DryLeaves, tags=["DryLeaves"])
def create_dry_leaves(dry_leaves: schemas.DryLeavesCreate, db: Session = Depends(get_db)):
    return crud.create_dry_leaves(db=db, dry_leaves=dry_leaves)

@app.get("/dryleaves/get/", response_model=List[schemas.DryLeaves], tags=["DryLeaves"])
def get_dry_leaves(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_dry_leaves(db=db, limit=limit)

@app.get("/dryleaves/get/{dry_leaves_id}", response_model=schemas.DryLeaves, tags=["DryLeaves"])
def get_dry_leaves_id(dry_leaves_id: int, db: Session = Depends(get_db)):
    dry_leaves = crud.get_dry_leaves_by_id(db=db, dry_leaves_id=dry_leaves_id)
    if not dry_leaves:
        raise HTTPException(status_code=404, detail="dry leaves not found")
    return dry_leaves

@app.get("/dryleaves/get_by_user/{user_id}", response_model=List[schemas.DryLeaves], tags=["DryLeaves"])
def get_dry_leaves_by_user(user_id: str, db: Session = Depends(get_db)):
    dry_leaves = crud.get_dry_leaves_by_user_id(db, user_id)
    if not dry_leaves:
        raise HTTPException(status_code=404, detail="Dry leaves not found")
    return dry_leaves

@app.delete("/dryleaves/delete/{dry_leaves_id}", response_class=JSONResponse, tags=["DryLeaves"])
def delete_dry_leaves_by_id(dry_leaves_id: int, db: Session = Depends(get_db)):
    delete = crud.delete_dry_leaves_by_id(db=db, dry_leaves_id=dry_leaves_id)
    if delete:
        return {"message": "dry leaves deleted successfully"}
    else:
        return {"message": "dry leaves not found or deletion failed"}

@app.put("/dryleaves/put/{dry_leaves_id}", response_model=schemas.DryLeaves, tags=["DryLeaves"])
def update_dry_leaves(dry_leaves_id: int, dry_leaves: schemas.DryLeavesUpdate, db: Session = Depends(get_db)):
    update_dry_leaves = crud.update_dry_leaves(db=db, dry_leaves_id=dry_leaves_id, dry_leaves_update=dry_leaves)
    if not update_dry_leaves:
        raise HTTPException(status_code=404, detail="dry leaves not found")
    return update_dry_leaves

@app.put("/dryleaves/update_status/{dry_leaves_id}", response_model=schemas.DryLeaves, tags=["DryLeaves"])
def update_dry_leaves_status(dry_leaves_id: int, status_update: schemas.DryLeavesStatusUpdate, db: Session = Depends(get_db)):
    updated_dry_leaves = crud.update_dry_leaves_status(db=db, dry_leaves_id=dry_leaves_id, status_update=status_update)
    if not updated_dry_leaves:
        raise HTTPException(status_code=404, detail="dry leaves not found")
    return updated_dry_leaves

# Flour
@app.post("/flour/post", response_model=schemas.Flour, tags=["Flour"])
def create_flour(flour: schemas.FlourCreate, db: Session = Depends(get_db)):
    return crud.create_flour(db=db, flour=flour)

@app.get("/flour/get", response_model=List[schemas.Flour], tags=["Flour"])
def get_flour(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_flour(db=db, limit=limit)

@app.get("/flour/get/{flour_id}", response_model=schemas.Flour, tags=["Flour"])
def get_flour_by_id(flour_id: int, db: Session = Depends(get_db)):
    flour = crud.get_flour_by_id(db=db, flour_id=flour_id)
    if not flour:
        raise HTTPException(status_code=404, detail="flour not found")
    else:
        return flour

@app.get("/flour/get_by_user/{user_id}", response_model=List[schemas.Flour], tags=["Flour"])
def get_flour_by_user(user_id: str, db: Session = Depends(get_db)):
    flour = crud.get_flour_by_user_id(db, user_id)
    if not flour:
        raise HTTPException(status_code=404, detail="flour not found")
    return flour

@app.delete("/flour/delete/{flour_id}", response_class=JSONResponse, tags=["Flour"])
def delete_flour_by_id(flour_id: int, db: Session = Depends(get_db)):
    delete = crud.delete_flour_by_id(db=db, flour_id=flour_id)
    if delete:
        return {"message": "flour deleted successfully"}
    else:
        return {"message": "flour not found or deletion failed"}

@app.put("/flour/put/{flour_id}", response_model=schemas.Flour, tags=["Flour"])
def update_flour(flour_id: int, flour: schemas.FlourUpdate, db: Session = Depends(get_db)):
    update_flour = crud.update_flour(db=db, flour_id=flour_id, flour_update=flour)
    if not update_flour:
        raise HTTPException(status_code=404, detail="flour not found")
    return update_flour

@app.put("/flour/update_status/{flour_id}", response_model=schemas.Flour, tags=["Flour"])
def update_flour_status(flour_id: int, status_update: schemas.FlourStatusUpdate, db: Session = Depends(get_db)):
    updated_flour = crud.update_flour_status(db=db, flour_id=flour_id, status_update=status_update)
    if not updated_flour:
        raise HTTPException(status_code=404, detail="flour not found")
    return updated_flour

# Shipment
@app.post('/shipment/post', response_model=schemas.Shipment, tags=["Shipment"])
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    return crud.create_shipment(db=db, shipment=shipment)

@app.get('/shipment/get', response_model=List[schemas.Shipment], tags=["Shipment"])
def get_shipment(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_shipment(db=db, limit=limit)

@app.get('/shipment/getid/{shipment_id}', response_model=schemas.Shipment, tags=["Shipment"])
def get_shipment_by_id(shipment_id: int, db: Session = Depends(get_db)):
    shipment = crud.get_shipment_by_id(db=db, shipment_id=shipment_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="shipment not found")
    return shipment

@app.get("/shipment/get_by_user/{user_id}", response_model=List[schemas.Shipment], tags=["Shipment"])
def get_shipment_by_user(user_id: str, db: Session = Depends(get_db)):
    shipment_data = crud.get_shipment_by_user_id(db, user_id)
    if not shipment_data:
        raise HTTPException(status_code=404, detail="shipments not found")
    return shipment_data

@app.get("/shipments/ids", response_model=List[int], tags=["Shipment"])
def get_all_shipment_ids(db: Session = Depends(get_db)):
    shipments = crud.get_all_shipment_ids(db)
    print(f"All shipment IDs: {[shipment.ShipmentID for shipment in shipments]}")
    return [shipment.ShipmentID for shipment in shipments]

# Endpoint to compare shipment IDs
@app.get("/check_shipment_ids", response_model=List[str])
def check_shipment_ids(db: Session = Depends(get_db)):
    shipment_ids = crud.get_shipment_ids_with_date_but_no_checkin(db)
    print(f"Fetched shipment IDs: {shipment_ids}")

    # Example hashed ID to compare
    known_shipment_id = "known_shipment_id"
    hashed_shipment_id = bcrypt.hashpw(known_shipment_id.encode('utf-8'), bcrypt.gensalt())
    print(f"Hashed shipment ID: {hashed_shipment_id}")

    def brute_force_check(shipment_id):
        if bcrypt.checkpw(shipment_id.encode('utf-8'), hashed_shipment_id):
            return shipment_id
        else:
            print(f"No match for shipment ID: {shipment_id}")
            return None

    valid_shipment_ids = [brute_force_check(str(shipment_id)) for shipment_id in shipment_ids]
    valid_shipment_ids = list(filter(None, valid_shipment_ids))  # Filter out None values
    print(f"Valid shipment IDs: {valid_shipment_ids}")
    return valid_shipment_ids

@app.put("/shipment/put/{shipment_id}", response_model=schemas.Shipment, tags=["Shipment"])
def update_shipment(shipment_id: int, shipment_update: schemas.ShipmentUpdate, db: Session = Depends(get_db)):
    db_shipment = crud.update_shipment(db, shipment_id, shipment_update)
    if db_shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return db_shipment

@app.put("/shipment/update_date/{shipment_id}", response_model=schemas.Shipment, tags=["Shipment"])
def update_shipment_date(shipment_id: int, shipment_date_update: schemas.ShipmentDateUpdate, db: Session = Depends(get_db)):
    updated_shipment = crud.update_shipment_date(db=db, shipment_id=shipment_id, shipment_date_update=shipment_date_update)
    if not updated_shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return updated_shipment

@app.put("/shipment/update_check_in/{shipment_id}", response_model=schemas.Shipment, tags=["Shipment"])
def update_shipment_check_in(shipment_id: int, check_in_update: schemas.ShipmentCheckInUpdate, db: Session = Depends(get_db)):
    updated_shipment = crud.update_shipment_check_in(db=db, shipment_id=shipment_id, check_in_update=check_in_update)
    if not updated_shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return updated_shipment

@app.delete('/shipment/delete/{shipment_id}', tags=["Shipment"])
def delete_shipment_by_id(shipment_id: int, db: Session = Depends(get_db)):
    delete = crud.delete_shipment_by_id(db=db, shipment_id=shipment_id)
    if delete:
        return {"message": "shipment deleted successfully"}
    else:
        return {"message": "shipment not found or deletion failed"}

# Location    
@app.post('/location/post', response_model=schemas.Location, tags=["Location"])
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db, location=location)

@app.get('/location/get', response_model=List[schemas.Location], tags=["Location"])
def get_location(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_location(db=db, limit=limit)

@app.get('/location/getid/{location_id}', response_model=schemas.Location, tags=["Location"])
def get_location_by_id(location_id: int, db: Session = Depends(get_db)):
    location = crud.get_location_by_id(db=db, location_id=location_id)
    if not location:
        raise HTTPException(status_code=404, detail="location not found")
    return location

@app.delete('/location/delete/{location_id}', tags=["Location"])
def delete_location_by_id(location_id: int, db: Session = Depends(get_db)):
    delete = crud.delete_location_by_id(db=db, location_id=location_id)
    if delete:
        return {"message": "location deleted successfully"}
    else:
        return {"message": "location not found or deletion failed"}
    
@app.get('/centra/statistics/{user_id}', tags = ["Statistics"])
def retrieve_centra_stats(user_id: str, db: Session = Depends(get_db)):
    sum_wet_leaves = crud.sum_get_wet_leaves_by_user_id(db, user_id)
    sum_dry_leaves = crud.sum_get_dry_leaves_by_user_id(db, user_id)
    sum_flour = crud.sum_get_flour_by_user_id(db, user_id)
    sum_shipment_quantity = crud.sum_get_shipment_quantity_by_user_id(db, user_id)
    return {
        "sum_wet_leaves": format_large_number(sum_wet_leaves),
        "sum_dry_leaves": format_large_number(sum_dry_leaves),
        "sum_flour": format_large_number(sum_flour),
        "sum_shipment_quantity": format_large_number(sum_shipment_quantity)
    }

if __name__ == '__main__':
    uvicorn.run("main:app", host = "0.0.0.0", reload=True)