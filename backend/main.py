import os
import joblib
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.database import Base, engine, get_db
from backend.models import User, WaterQuality, AIPrediction
from backend.schemas import RegisterRequest, LoginRequest, WaterRequest, PredictionRequest
from backend.auth import hash_password, verify_password

os.makedirs("data", exist_ok=True)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wastewater AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# โหลด AI Model ( Random Forest Regressor )
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "water_treatment_ai_v1.pkl"
)
try:
    ai_model = joblib.load(MODEL_PATH)
    print("AI Model loaded successfully.")
except Exception as e:
    ai_model = None
    print(f"Warning: Could not load AI Model. Fallback formula will be used. Error: {e}")


def user_from_token(authorization: str, db: Session):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Please login"
        )

    username = authorization.replace("Bearer ", "", 1)

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid session"
        )

    return user


@app.get("/")
def root():
    return {"message": "Wastewater AI API is running"}


@app.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(400, "Username already exists")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already exists")
    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    return {"message": "Register successful"}


@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Username or password is incorrect")
    return {
        "message": "Login successful",
        "token": user.username,
        "user": {"id": user.id, "username": user.username, "email": user.email}
    }


@app.get("/me")
def me(authorization: str = Header(default=""), db: Session = Depends(get_db)):
    user = user_from_token(authorization, db)
    return {"id": user.id, "username": user.username, "email": user.email}


@app.post("/water")
def save_water(
    data: WaterRequest,
    authorization: str = Header(default=""),
    db: Session = Depends(get_db)
):
    user = user_from_token(authorization, db)
    status = "Good" if data.current_do >= 4 else "Needs Attention"
    row = WaterQuality(user_id=user.id, status=status, **data.model_dump())
    db.add(row)
    db.commit()
    return {"message": "Water quality saved", "status": status}


@app.get("/water")
def water_history(authorization: str = Header(default=""), db: Session = Depends(get_db)):
    user = user_from_token(authorization, db)
    rows = (
        db.query(WaterQuality)
        .filter(WaterQuality.user_id == user.id)
        .order_by(WaterQuality.created_at.desc())
        .all()
    )
    return [{
        "id": r.id,
        "influent_cod": r.influent_cod,
        "flow_rate": r.flow_rate,
        "water_temp": r.water_temp,
        "current_do": r.current_do,
        "status": r.status,
        "created_at": r.created_at.isoformat()
    } for r in rows]


@app.post("/prediction")
def prediction(
    data: PredictionRequest,
    authorization: str = Header(default=""),
    db: Session = Depends(get_db)
):
    user = user_from_token(authorization, db)

    # นำค่าที่รับเข้ามาประมวลผลผ่าน AI Model
    if ai_model is not None:
        input_data = pd.DataFrame([{
            "influent_cod": data.influent_cod,
            "flow_rate": data.flow_rate,
            "water_temp": data.water_temp,
            "current_do": data.current_do
        }])
        speed = float(ai_model.predict(input_data)[0])
    else:
        # กรณีไม่พบไฟล์โมเดล ให้ใช้สูตรคำนวณสำรอง
        speed = (
            35
            + data.influent_cod * 0.08
            + data.flow_rate * 0.25
            + max(0, 4 - data.current_do) * 8
            + max(0, data.water_temp - 30) * 0.5
        )

    # ควบคุมช่วงค่าคำตอบให้อยู่ระหว่าง 0 - 100
    speed = max(0.0, min(100.0, speed))

    row = AIPrediction(
        user_id=user.id,
        predicted_speed=round(speed, 2),
        **data.model_dump()
    )
    db.add(row)
    db.commit()

    return {
        "predicted_speed": round(speed, 2),
        "message": "Prediction successful"
    }


@app.get("/predictions")
def prediction_history(authorization: str = Header(default=""), db: Session = Depends(get_db)):
    user = user_from_token(authorization, db)
    rows = (
        db.query(AIPrediction)
        .filter(AIPrediction.user_id == user.id)
        .order_by(AIPrediction.created_at.desc())
        .all()
    )
    return [{
        "id": r.id,
        "influent_cod": r.influent_cod,
        "flow_rate": r.flow_rate,
        "water_temp": r.water_temp,
        "current_do": r.current_do,
        "predicted_speed": r.predicted_speed,
        "created_at": r.created_at.isoformat()
    } for r in rows]
