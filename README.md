# Wastewater AI - HTML Frontend

โปรเจกต์นี้ทำโครงสร้างคล้าย `chottomatte` แต่เปลี่ยน Frontend จาก Streamlit เป็น HTML + CSS + JavaScript

## โครงสร้าง

- `backend/` FastAPI + SQLAlchemy + SQLite
- `frontend/` HTML + CSS + JavaScript
- `data/` ฐานข้อมูล SQLite จะถูกสร้างอัตโนมัติ
- `model/` สำหรับใส่ `model.pkl` ภายหลัง

## วิธีติดตั้ง

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## วิธีรัน Backend

จาก root project:

```bash
uvicorn backend.main:app --reload
```

Backend:
`http://127.0.0.1:8000`

## วิธีเปิด Frontend

แนะนำใช้ VS Code + Live Server แล้วเปิด:

`frontend/index.html`
