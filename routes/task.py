from fastapi import APIRouter  , HTTPException
from schmes import UserLogin , UserRegister , TaskCreate , TaskUpdate
from auth import hash_password , varify_password , verify_token , create_token
from database import get_db
from models import User , Task 
from sqlalchemy import select  ,update
from fastapi import Depends
from sqlalchemy.orm import Session 

router = APIRouter()

@router.post("/register")
def create_user(user:UserRegister , db:Session = Depends(get_db) ):
    hashed = hash_password(user. password) # pass will be hashed here 
    new_user = User(name = user.name, email = user.email , password = hashed) # hashed pass will be add in database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def user_login(user:UserLogin , db:Session = Depends(get_db)):
     found_user = db.query(User).filter_by(email = user.email).first()
     if found_user is None :
          raise HTTPException(status_code=404 , detail= " user not found ")
     
     cheack_pass = varify_password(plain_password= user.plan_password , hashed_password= found_user.password)
     if cheack_pass  == True:
          cheack_token = create_token(user.email)
     if cheack_pass == False:
          raise HTTPException(status_code=401 , detail="wrong password")

     return cheack_token  
   

@router.post("/tasks")
def create_task(task:TaskCreate , db : Session = Depends(get_db), get_email : str = Depends(verify_token)):
     found_user = db.query(User).filter_by(email =get_email).first()
     if found_user is None:
          raise HTTPException(status_code=404 , detail="user not found ")
     new_task = Task( title = task.title , description = task.description, user_id = found_user.id )
     db.add(new_task)
     db.commit()
     db.refresh(new_task)
     return new_task
    
@router.get("/tasks")
def get_tasks(get_email : str = Depends(verify_token), db : Session = Depends(get_db)):
     found_user = db.query(User).filter_by(email  = get_email).first()
     task  = db.query(Task).filter_by(user_id = found_user.id).all() # i want all task 
     return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id : int  , db : Session = Depends(get_db), get_email : str = Depends(verify_token)):
     found_task = db.get(Task,task_id)
     if found_task is None:
          raise HTTPException(status_code=404 , detail="no task exist ")
     db.delete(found_task)
     db.commit()
     output = {
          "message":"task deleted "
     } 
     return output

@router.put("/tasks/{task_id}")
def update_task(task_id : int , new_task : TaskUpdate , db: Session= Depends(get_db),get_email : str = Depends(verify_token)):
     found_task = db.get(Task ,task_id)
     if found_task is None:
          raise HTTPException(status_code=404 , detail="task not found ")
     stmt = (
          update(Task)
          .where(Task.id == task_id)
          .values({
               "title":new_task.title,
               "description" : new_task.description,
               "completed":new_task.completed
          })
     )
     db.execute(stmt)
     db.commit()
     return{"message":"task updated "}