from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import engine, Base, SessionLocal

from app.models.user import User
from app.models.asset import Asset
from app.models.allocation import Allocation
from app.models.audit import Audit

from app.auth import create_access_token, verify_token, require_role
from app.security import hash_password, verify_password

Base.metadata.create_all(bind=engine)

app = FastAPI()


# ---------------- DB SESSION ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "System Running Successfully"}


# ---------------- USERS ----------------
@app.post("/users")
def create_user(
    full_name: str,
    email: str,
    password: str,
    role: str,
    db: Session = Depends(get_db)
):

    user = User(
        full_name=full_name,
        email=email,
        password=hash_password(password),
        role=role
    )

    db.add(user)
    db.commit()

    return {"message": "User Created Successfully"}


@app.get("/users")
def get_users(db: Session = Depends(get_db), user=Depends(verify_token)):
    return db.query(User).all()


# ---------------- LOGIN ----------------
@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"message": "User not found"}

    if not verify_password(password, user.password):
        return {"message": "Invalid password"}

    token = create_access_token({
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    })

    return {"access_token": token, "token_type": "bearer"}


# ---------------- ASSETS ----------------
@app.post("/assets")
def create_asset(
    asset_name: str,
    category: str,
    status: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):

    asset = Asset(
        asset_name=asset_name,
        category=category,
        status=status
    )

    db.add(asset)
    db.commit()

    return {"message": "Asset Added Successfully"}


@app.get("/assets")
def get_assets(db: Session = Depends(get_db)):
    return db.query(Asset).filter(Asset.is_deleted == False).all()


# ---------------- ALLOCATE ASSET ----------------
@app.post("/allocate")
def allocate_asset(
    user_id: int,
    asset_id: int,
    db: Session = Depends(get_db)
):

    # check duplicate allocation
    existing = db.query(Allocation).filter(
        Allocation.asset_id == asset_id
    ).first()

    if existing:
        return {"message": "Asset already assigned"}

    # create allocation
    allocation = Allocation(
        user_id=user_id,
        asset_id=asset_id,
        assigned_at=datetime.utcnow()
    )

    db.add(allocation)
    db.commit()

    # audit log
    audit = Audit(
        action="ASSIGNED",
        user_id=user_id,
        asset_id=asset_id,
        timestamp=datetime.utcnow()
    )

    db.add(audit)
    db.commit()

    return {
        "message": "Asset Assigned Successfully",
        "allocation_id": allocation.id
    }


# ---------------- RETURN ASSET ----------------
@app.post("/return-asset")
def return_asset(
    allocation_id: int,
    db: Session = Depends(get_db)
):

    allocation = db.query(Allocation).filter(
        Allocation.id == allocation_id
    ).first()

    if not allocation:
        return {"message": "Allocation not found"}

    allocation.returned_at = datetime.utcnow()

    db.commit()

    audit = Audit(
        action="RETURNED",
        user_id=allocation.user_id,
        asset_id=allocation.asset_id,
        timestamp=datetime.utcnow()
    )

    db.add(audit)
    db.commit()

    return {"message": "Asset Returned Successfully"}


# ---------------- AUDIT ----------------
@app.get("/audit")
def get_audit(db: Session = Depends(get_db)):
    return db.query(Audit).all()