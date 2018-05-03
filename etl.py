from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.sql import *

engine = create_engine('sqlite:///bi.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

#Definir esquema
class Franja(Base):
    __tablename__ = "franja"
    id = Column('id',Integer,primary_key=True)
    dia = Column('dia',String)#,primary_key=True)
    hora = Column('hora',String)#,primary_key=True)
    minuto = Column('minuto',String)#,primary_key=True)
    duracion = Column('duracion',String)#,primary_key=True)

class Salon(Base):
    __tablename__='salon'
    senhalizacion=Column('senhalizacion',String,primary_key=True)
    edificio = Column('edificio',String)
    capacidad = Column('capacidad',String)
    extension = Column('extension',String)
    area = Column('area',String)
    tiene_movil_express = Column('tiene_movil_express',String)
    tipo_mobiliario = Column('tipo_mobiliario',String)
    es_fijo = Column('es_fijo',String)

class Seccion(Base):
    __tablename__='seccion'
    id=Column('id',String,primary_key=True)
    crn = Column('crn',Integer)
    semestre = Column('semestre',String)
    numero_seccion = Column('numero_seccion',String)
    cupos = Column('cupos',String)
    inscritos = Column('inscritos',String)
    disponibles = Column('disponibles',String)
    profesor1 = Column('profesor1',String)
    profesor2 = Column('profesor2',String)
    profesor3 = Column('profesor3',String)

class Curso(Base):
    __tablename__='curso'
    materia=Column('materia',String,primary_key=True)
    nombre = Column('nombre',Integer)
    creditos = Column('creditos',String)

class Clase(Base):
    __tablename__='clase'
    id=Column('id',Integer,primary_key=True)
    curso_materia=Column('curso',String,ForeignKey('curso.materia'))
    seccion_id=Column('seccion',String,ForeignKey('seccion.id'))
    salon_senhalizacion=Column('salon',String,ForeignKey('salon.senhalizacion'))
    franja_id=Column('franja',Integer,ForeignKey('franja.id'))

    curso = relationship("Curso")
    seccion = relationship("Seccion")
    salon = relationship("Salon")
    franja = relationship("Franja")

Franja.__table__.create(bind=engine,checkfirst=True)
Salon.__table__.create(bind=engine,checkfirst=True)
Seccion.__table__.create(bind=engine,checkfirst=True)
Curso.__table__.create(bind=engine,checkfirst=True)
Clase.__table__.create(bind=engine,checkfirst=True)
#Extraer
"""
import requests
url = 'https://randomuser.me/api/?results=10'
users_json = requests.get(url).json()
url2 = 'https://jsonplaceholder.typicode.com/posts/'
uploads_json = requests.get(url2).json()
"""
#Transformar
"""
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

"""
franjas=[]
franjita={}
franjita['id']=16
franjita['dia']="01"
franjita['minuto']="30"
franjita['hora']="14"
franjita['duracion']="01:20"
franjas.append(franjita)
salones=[]
saloncito={}
saloncito['senhalizacion']="Au_102"
saloncito['edificio']="Au"
saloncito['capacidad']="26"
saloncito['extension']="5601"
saloncito['area']="62,6"
saloncito['tiene_movil_express']="Si"
saloncito['tipo_mobiliario']="Nesa trapezoidal con silla movil"
saloncito['es_fijo']="Movil"
salones.append(saloncito)
secciones=[]
seccioncita={}
seccioncita['id']="2018-01-10127"
seccioncita['crn']=10126
seccioncita['semestre']="2018-01"
seccioncita['numero_seccion']=1
seccioncita['cupos']=121
seccioncita['inscritos']=91
seccioncita['disponibles']=30
seccioncita['profesor1']="DIAZ MATAJIRA LUIS"
seccioncita['profesor2']=""
seccioncita['profesor3']=""
secciones.append(seccioncita)
cursos=[]
curcito = {}
curcito['materia']="ADMI-1102"
curcito['nombre']="FUNDAM.ADMON Y GERENCIA (ADMI)"
curcito['creditos']="3"
cursos.append(curcito)
clases=[]
clasecita={}
clasecita['id']=2
#curso_temp = session.query(Curso).filter_by(materia="ADMI-1101")
#if curso_temp
clasecita['curso']=Curso(materia="ADMI-1101")
clasecita['seccion']=Seccion(id="2018-01-10126")
clasecita['salon']=Salon(senhalizacion="Au_101")
clasecita['franja']=Franja(id=15)
clases.append(clasecita)
#Cargar
"""
Session = sessionmaker(bind=engine)
session = Session()
for user in users:
    row = Users(**user)
    session.add(row)
for upload in uploads:
    row = Uploads(**upload)
    session.add(row)
session.commit()
"""

for f in franjas:
    row = Franja(**f)
    session.add(row)
for s in salones:
    row = Salon(**s)
    session.add(row)
for s in secciones:
    row = Seccion(**s)
    session.add(row)
for c in cursos:
    row = Curso(**c)
    session.add(row)
for c in clases:
    row = Clase(**c)
    session.add(row)
session.commit()
