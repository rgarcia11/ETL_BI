from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.sql import *
import pandas as pd
engine = create_engine('sqlite:///bi.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
semestre_actual = "2018-01"
#Definir esquema
class Franja(Base):
    __tablename__ = "franja"
    id = Column('id',Integer,primary_key=True)
    dia = Column('dia',String)#,primary_key=True)
    hora = Column('hora',String)#,primary_key=True)
    minuto = Column('minuto',String)#,primary_key=True)
    duracion = Column('duracion',String)#,primary_key=True)
    clases = relationship('Clase')

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
    clases = relationship('Clase')

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
    clases = relationship('Clase')

class Curso(Base):
    __tablename__='curso'
    materia=Column('materia',String,primary_key=True)
    nombre = Column('nombre',Integer)
    creditos = Column('creditos',String)
    clases = relationship('Clase')

class Clase(Base):
    __tablename__='clase'
    id=Column('id',Integer,primary_key=True)
    curso_materia=Column('curso',String,ForeignKey('curso.materia'))
    seccion_id=Column('seccion',String,ForeignKey('seccion.id'))
    salon_senhalizacion=Column('salon',String,ForeignKey('salon.senhalizacion'))
    franja_id=Column('franja',Integer,ForeignKey('franja.id'))

    #curso = relationship("Curso", backref='person', lazy='dynamic')
    #seccion = relationship("Seccion", backref='person', lazy='dynamic')
    #salon = relationship("Salon", backref='person', lazy='dynamic')
    #franja = relationship("Franja", backref='person', lazy='dynamic')

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

scraped = pd.read_csv("cursos_scraped_formato.csv",sep=";")
scraped_lista_filas = scraped.to_dict(orient='records')
row_ejemplo = scraped_lista_filas[0]

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
salones=[]
secciones=[]
cursos=[]
clases=[]

franjita={}
franjita['id']=1
franjita['dia']=row_ejemplo['1Horas'][:4]
franjita['minuto']=row_ejemplo['1Horas'][:4][2:]
franjita['hora']=row_ejemplo['1Horas'][:4][:2]
franjita['duracion']="01:20"
nueva_franja = Franja(**franjita)

saloncito={}
saloncito['senhalizacion']=row_ejemplo['1Salon']
saloncito['edificio']=row_ejemplo['1Salon'][:2]
saloncito['capacidad']="26"
saloncito['extension']="5601"
saloncito['area']="62,6"
saloncito['tiene_movil_express']="Si"
saloncito['tipo_mobiliario']="Nesa trapezoidal con silla movil"
saloncito['es_fijo']="Movil"
nuevo_salon = Salon(**saloncito)


seccioncita={}
seccioncita['id']='{}-{}'.format(semestre_actual,str(row_ejemplo['CRN']))
seccioncita['crn']=row_ejemplo['CRN']
seccioncita['semestre']=semestre_actual
seccioncita['numero_seccion']=row_ejemplo['Seccion']
seccioncita['cupos']=row_ejemplo['Cupo']
seccioncita['inscritos']=row_ejemplo['Inscritos']
seccioncita['disponibles']=row_ejemplo['Disponible']
seccioncita['profesor1']=row_ejemplo['1Instructor']
seccioncita['profesor2']=""
seccioncita['profesor3']=""
nueva_seccion = Seccion(**seccioncita)


curcito = {}
curcito['materia']=row_ejemplo['Materia']
curcito['nombre']=row_ejemplo['Titulo']
curcito['creditos']=row_ejemplo['Creditos']
nuevo_curso = Curso(**curcito)


clasecita={}
clasecita['id']=2
#curso_temp = session.query(Curso).filter_by(materia="ADMI-1101")
#if curso_temp
clasecita['curso_materia']=Curso(materia=curcito['materia'])
clasecita['seccion_id']=Seccion(id=seccioncita['id'])
clasecita['salon_senhalizacion']=Salon(senhalizacion=saloncito['senhalizacion'])
clasecita['franja_id']=Franja(id=franjita['id'])
nueva_clase = Clase(**clasecita)
nueva_franja.clases.append(nueva_clase)
nuevo_salon.clases.append(nueva_clase)
nueva_seccion.clases.append(nueva_clase)
nuevo_curso.clases.append(nueva_clase)
clases.append(nueva_clase)
franjas.append(nueva_franja)
salones.append(nuevo_salon)
secciones.append(nueva_seccion)
cursos.append(nuevo_curso)
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
    #row = Franja(**f)
    session.add(f)
for s in salones:
    #row = Salon(**s)
    session.add(s)
for s in secciones:
    #row = Seccion(**s)
    session.add(s)
for c in cursos:
    #row = Curso(**c)
    session.add(c)
for c in clases:
    #row = Clase(**c)
    print(c)
    session.add(c)
session.commit()
