from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *

engine = create_engine('sqlite:///data.db')
Base = declarative_base()

#Definir esquema
class Users(Base):
    __tablename__ = "users"
    UserId = Column(Integer, primary_key=True)
    Title = Column(String)
    FirstName = Column(String)
    LastName = Column(String)
    Email = Column(String)
    Username = Column(String)
    DOB = Column(DateTime)

class Uploads(Base):
    __tablename__ = "uploads"
    UploadId = Column(Integer, primary_key=True)
    UserId = Column(Integer)
    Title = Column(String)
    Body = Column(String)
    Timestamp = Column(DateTime)

Users.__table__.create(bind=engine, checkfirst=True)
Uploads.__table__.create(bind=engine, checkfirst=True)

#Extraer
import requests
url = 'https://randomuser.me/api/?results=10'
users_json = requests.get(url).json()
url2 = 'https://jsonplaceholder.typicode.com/posts/'
uploads_json = requests.get(url2).json()

#Transformar
from datetime import datetime, timedelta
from random import randint
users, uploads = [], []
for i, result in enumerate(users_json['results']):
    row = {}
    row['UserId'] = i
    row['Title'] = result['name']['title']
    row['FirstName'] = result['name']['first']
    row['LastName'] = result['name']['last']
    row['Email'] = result['email']
    row['Username'] = result['login']['username']
    dob = datetime.strptime(result['dob'],'%Y-%m-%d %H:%M:%S')
    row['DOB'] = dob.date()

    users.append(row)
for result in uploads_json:
    row = {}
    row['UploadId'] = result['id']
    row['UserId'] = result['userId']
    row['Title'] = result['title']
    row['Body'] = result['body']
    delta = timedelta(seconds=randint(1,86400))
    row['Timestamp'] = datetime.now() - delta
    uploads.append(row)

#Cargar
Session = sessionmaker(bind=engine)
session = Session()
for user in users:
    row = Users(**user)
    session.add(row)
for upload in uploads:
    row = Uploads(**upload)
    session.add(row)
session.commit()
