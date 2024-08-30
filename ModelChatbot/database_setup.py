from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# สร้างฐานข้อมูล SQLite
engine = create_engine('sqlite:///chatbot.db')
Base = declarative_base()

# สร้างตาราง User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    info = relationship("UserInformation", back_populates="user")

# สร้างตาราง UserInformation
class UserInformation(Base):
    __tablename__ = 'user_information'
    id = Column(Integer, primary_key=True)
    nickname = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="info")

# สร้างตารางในฐานข้อมูล
Base.metadata.create_all(engine)

# สร้าง session สำหรับการทำงานกับฐานข้อมูล
Session = sessionmaker(bind=engine)
session = Session()
