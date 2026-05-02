from fastapi import APIRouter, HTTPException, Response
from app.schemas import User, UserOut
from app.exceptions import CustomExceptionA
from itertools import count
from threading import Lock

router = APIRouter(prefix="/users", tags=["users"])

db: dict[int, dict] = {}
_id_seq = count(start=1)
_id_lock = Lock()

def next_user_id() -> int:
    with _id_lock:
        return next(_id_seq)

class UserIn(User):
    pass

class UserResponse(UserOut):
    id: int

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserIn):
    if user.age < 19:
        raise CustomExceptionA(detail="User must be at least 19 years old")

    user_id = next_user_id()
    db[user_id] = user.model_dump(exclude={'password'})
    return {"id": user_id, **db[user_id]}

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **db[user_id]}

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    if db.pop(user_id, None) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)