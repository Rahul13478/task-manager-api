from pydantic import BaseModel

class UserRegister(BaseModel):
    name : str
    email : str
    password : str

class UserLogin(BaseModel):
    email : str
    plan_password : str

class TaskCreate(BaseModel):
    title : str
    description : str

class TaskUpdate(BaseModel):
    title : str 
    description : str 
    completed : bool