from ..core import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey,Enum as SQLEnum

#Declaraciones Enum Generales de la DB
from ..enums import UserRole

class SystemUser(Base):
    __tablename__ = "system_users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password=Column(Text, nullable= False)
    role = Column(SQLEnum(UserRole), nullable=False)

class UserHierarchy(Base):
    __tablename__="hierarchy"
    id = Column(Integer, primary_key=True)
    manager_id=Column(Integer,ForeignKey('system_users.id'), nullable = False) 
    enduser_id = Column(Integer, ForeignKey('system_users.id'), nullable = False)

class Project(Base):
    __tablename__='projects'
    id= Column(Integer, primary_key=True)
    project_name=Column(String(50) , unique = True , nullable = False)
    owner_id=Column(Integer , ForeignKey('system_users.id') , nullable = False)

class ProjectRecipient(Base):
    __tablename__ = "project_recipients"
    id = Column(Integer, primary_key=True)
    recipient_name=Column(String(50), unique=True)
    recipient_email=Column(String(50), unique=True)
    recipient_number=Column(String(50), unique=True)

class ProjectAsignation(Base):
    __tablename__ = "project_assignation"
    id = Column(Integer, primary_key=True)
    recipient_id= Column(Integer, ForeignKey('project_recipients.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))

    