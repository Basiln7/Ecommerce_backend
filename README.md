# CRM Backend (FastAPI)

A modular, scalable CRM backend built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.  
This project demonstrates industry-standard backend architecture, authentication, and clean documentation.
The project build for my skill development its an ecommers backend product curd ,cart add and delet,user jwt authentication and email verification.In this project used alembic for migration and database table creation 

---

## 🚀 Features
- User authentication with JWT
- Email OTP authentication
- Modular folder structure
- CRUD operations for customers, products, and cart
---

## Installation
1. Clone repository
```bash
   git clone https://github.com/yourusername/crm-backend.git
   cd crm-backend

```

2. Vertual environment Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run migration(if using Alembic)
```bash
alembic upgrade head
```
## Start the FastAPI server
```bash
uvicorn app.main:app --reload
```
## ENV file(.env)
DATABASE_URL="your db URL"
SECRET_KEY=your_scret_key
ALGORITHM=HS256
TOKEN_EXPIRE_TIME=30
#### Email verification need datas 
MAIL_USERNAME=Your_email@gmmail.com
MAIL_PASSWORD=Yor_app_password
MAIL_FROM=Your_email@gmmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_FROM_NAME=OTP Service