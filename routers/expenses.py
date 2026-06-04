from models import Expenses
from schemas import Expense,Expense_Response,Expense_update
from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
router = APIRouter(prefix="/Expenses",tags=["Expenses"])
@router.post("/",status_code=201)
def create_expense(expense:Expense,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    expense_data = Expenses(
        title = expense.title,
        amount = expense.amount,
        category = expense.category,
        owner_id = current_user.id
    )
    db.add(expense_data)
    db.commit()
    db.refresh(expense_data)
    return expense_data
@router.get("/",response_model=Expense_Response)
def all_expenses(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    expense = db.query(Expenses).filter(Expenses.owner_id == current_user.id).all()
    if not expense:
        raise HTTPException(status_code=404,detail="not found")
    return expense
@router.get("/{expense_id}",response_model=Expense_Response)
def get_expense(expense_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    expense = db.query(Expenses).filter(Expenses.id == expense_id,Expenses.owner_id == current_user.id).first
    if not expense:
        raise HTTPException(status_code=404,detail="expense not found")
    return expense
@router.put("/{expense_id}",response_model=Expense_Response)
def update_expense(expense_id:int,update:Expense_update,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    expense = db.query(Expenses).filter(Expenses.id == expense_id,Expenses.owner_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404,detail="expense not found")
    if update.amount is not None:
        expense.amount = update.amount
    db.commit()
    db.refresh(expense)
    return expense
@router.delete("/{expense_id}")
def delete_expense(expense_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    expense = db.query(Expenses).filter(Expenses.id == expense_id,Expenses.owner_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404,detail="not found")
    db.delete(expense)
    db.commit()
    return {"success":"expense deleted"}