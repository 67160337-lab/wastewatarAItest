from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class WaterRequest(BaseModel):
    influent_cod: float
    flow_rate: float
    water_temp: float
    current_do: float

class PredictionRequest(BaseModel):
    influent_cod: float
    flow_rate: float
    water_temp: float
    current_do: float
