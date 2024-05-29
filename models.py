from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey,create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from enum import Enum

# Create your models here.
Base = declarative_base()

db_url = f"mysql://root:Anvitha16@127.0.0.1:3306/mydb"
engine = create_engine(db_url)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session()
# Define a sample SQLAlchemy model

class RoleEnum(Enum):
    STUDENT = 'Student'
    TEACHER = 'Teacher'

class Parent_details(Base):
    __tablename__ = 'parent_details'
    id = Column(Integer, primary_key=True)
    Mother_Name = Column(String(20))
    Father_Name = Column(String(20))
    user_id = Column(Integer, ForeignKey('user.id'))

class UserModel(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    password = Column(String(128))
    email = Column(String(100))
    roles = Column(SQLAlchemyEnum(RoleEnum), nullable=True)
    phone_number = relationship("Phone_number",back_populates="user",uselist=False)
    parents = relationship(Parent_details)

class Phone_number(Base):
    __tablename__ = 'phone_number'
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("UserModel", back_populates="phone_number") 
