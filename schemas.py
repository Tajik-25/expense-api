from pydantic import BaseModel,Field,ConfigDict
from typing import Optional
from datetime import datetime
class User(BaseModel):
    email:str
    password:str
class Expense(BaseModel):
    title:str
    amount:int=Field(gt=0)
    category:str
class Expense_Response(BaseModel):
    id:int
    title:str
    amount:int
    category:str
    created_at :datetime
    owner_id :int
    model_config = ConfigDict(from_attributes=True)
class Expense_update(BaseModel):
    amount :Optional[int]=None
    
