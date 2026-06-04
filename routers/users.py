from auth import get_current_user
from fastapi import Depends,APIRouter
router = APIRouter(prefix="/Me",tags=["Users"])
@router.get("/")
def get_me(current_user=Depends(get_current_user)):
    return current_user
