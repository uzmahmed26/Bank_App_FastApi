from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# In-memory database for users
# In a real application, this would be a proper database
users_db: Dict[str, "UserInDB"] = {}

class User(BaseModel):
    name: str
    pin_number: str
    bank_balance: float = 0.0

class UserInDB(User):
    hashed_pin: str

# For simplicity, let's pre-populate some users (in a real app, this would be registration)
# Hashing the PIN for security (even in-memory)
import hashlib

def get_password_hash(pin: str):
    return hashlib.sha256(pin.encode()).hexdigest()

# Pre-populate users from the provided data
initial_users_data = {
    "uzma": {"pin": 1234, "balance": 5000},
    "ahmed": {"pin": 1111, "balance": 3000},
    "ali": {"pin": 2222, "balance": 10000}
}

for name, data in initial_users_data.items():
    pin_number_str = str(data["pin"])
    users_db[name] = UserInDB(
        name=name,
        pin_number=pin_number_str,
        hashed_pin=get_password_hash(pin_number_str),
        bank_balance=float(data["balance"])
    )

@app.get("/")
async def read_root():
    return {"message": "Bank API running"}

class AuthRequest(BaseModel):
    name: str
    pin_number: str

@app.post("/authenticate")
async def authenticate_user(auth_request: AuthRequest):
    user = users_db.get(auth_request.name)
    if not user:
        return {"error": "Invalid Credentials"}

    hashed_pin = get_password_hash(auth_request.pin_number)
    if hashed_pin != user.hashed_pin:
        return {"error": "Invalid Credentials"}

    return {"name": user.name, "bank_balance": user.bank_balance}

class DepositRequest(BaseModel):
    name: str
    amount: float

@app.post("/deposit")
async def deposit_funds(deposit_request: DepositRequest):
    user = users_db.get(deposit_request.name)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if deposit_request.amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive")

    user.bank_balance += deposit_request.amount
    return {"bank_balance": user.bank_balance}

class TransferRequest(BaseModel):
    sender_name: str
    sender_pin: str
    recipient_name: str
    amount: float

@app.post("/bank-transfer")
async def bank_transfer(transfer_request: TransferRequest):
    sender = users_db.get(transfer_request.sender_name)
    if not sender:
        raise HTTPException(status_code=400, detail="Sender not found")

    recipient = users_db.get(transfer_request.recipient_name)
    if not recipient:
        raise HTTPException(status_code=400, detail="Recipient not found")

    if sender.name == recipient.name:
        raise HTTPException(status_code=400, detail="Cannot transfer to yourself")

    hashed_pin = get_password_hash(transfer_request.sender_pin)
    if hashed_pin != sender.hashed_pin:
        raise HTTPException(status_code=400, detail="Invalid PIN for sender")

    if transfer_request.amount <= 0:
        raise HTTPException(status_code=400, detail="Transfer amount must be positive")

    if sender.bank_balance < transfer_request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    sender.bank_balance -= transfer_request.amount
    recipient.bank_balance += transfer_request.amount

    return {
        "message": "Transfer successful",
        "sender_new_balance": sender.bank_balance,
        "recipient_new_balance": recipient.bank_balance,
    }
