from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class WaterQuality(Base):
    __tablename__ = "water_quality"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    influent_cod = Column(Float, nullable=False)
    flow_rate = Column(Float, nullable=False)
    water_temp = Column(Float, nullable=False)
    current_do = Column(Float, nullable=False)
    status = Column(String(50), default="Normal")
    created_at = Column(DateTime, default=datetime.utcnow)

class AIPrediction(Base):
    __tablename__ = "ai_predictions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    influent_cod = Column(Float, nullable=False)
    flow_rate = Column(Float, nullable=False)
    water_temp = Column(Float, nullable=False)
    current_do = Column(Float, nullable=False)
    predicted_speed = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
