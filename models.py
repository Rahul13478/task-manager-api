from database import Base
from sqlalchemy import String , Column , Integer , Boolean , ForeignKey

class User(Base):
    __tablename__ = "users"
    id  = Column(Integer, primary_key=True)
    name  = Column(String)
    email = Column(String)
    password = Column(String)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer , primary_key=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean ,  default=False , nullable=False )
    user_id = Column(Integer , ForeignKey(User.id))