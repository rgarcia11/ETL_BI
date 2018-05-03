from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.sql import *
import pandas as pd
engine = create_engine('sqlite:///bi.db')
Base = declarative_base()
Session = sessionmaker(bind=engine,autoflush=False)
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

#Lectura del archivo csv de scraping
scraped = pd.read_csv("cursos_scraped_formato.csv",sep=";")
scraped_lista_filas = scraped.to_dict(orient='records')


#Transformar
def seleccionar_datos(row_ejemplo, i,dia,numero_dia):
    franjita={}
    franjita['id']=i
    franjita['dia']=dia
    franjita['minuto']=row_ejemplo['{}Horas'.format(numero_dia)][:4][2:]
    franjita['hora']=row_ejemplo['{}Horas'.format(numero_dia)][:4][:2]
    franjita['duracion']="01:20"
    nueva_franja = Franja(**franjita)

    saloncito={}
    saloncito['senhalizacion']=row_ejemplo['{}Salon'.format(numero_dia)]
    saloncito['edificio']=row_ejemplo['{}Salon'.format(numero_dia)][:2]
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
    if not pd.isnull(row_ejemplo['2Instructor']):
        seccioncita['profesor2']=row_ejemplo['2Instructor']
    else:
        seccioncita['profesor2']=""
    if not pd.isnull(row_ejemplo['3Instructor']):
        seccioncita['profesor3']=row_ejemplo['3Instructor']
    else:
        seccioncita['profesor3']=""
    nueva_seccion = Seccion(**seccioncita)


    curcito = {}
    curcito['materia']=row_ejemplo['Materia']
    curcito['nombre']=row_ejemplo['Titulo']
    curcito['creditos']=row_ejemplo['Creditos']
    nuevo_curso = Curso(**curcito)


    clasecita={}
    clasecita['id']=i
    #curso_temp = session.query(Curso).filter_by(materia="ADMI-1101")
    #if curso_temp
    clasecita['curso_materia']=Curso(materia=curcito['materia'])
    clasecita['seccion_id']=Seccion(id=seccioncita['id'])
    clasecita['salon_senhalizacion']=Salon(senhalizacion=saloncito['senhalizacion'])
    clasecita['franja_id']=Franja(id=franjita['id'])
    nueva_clase = Clase(**clasecita)
    return nueva_franja, nuevo_salon, nueva_seccion, nuevo_curso, nueva_clase

franjas=[]
salones=[]
secciones=[]
cursos=[]
clases=[]

columnas_a_borrar = ['1F. Inicial', '1F. Final', '2F. Inicial', '2F. Final', '3F. Inicial', '3F. Final']
for columna in columnas_a_borrar:
    del scraped[columna]

i = 0
for diccionario in scraped_lista_filas:

    dias1 = str(diccionario['1Dias'])
    dias2 = str(diccionario['2Dias'])
    dias3 = str(diccionario['3Dias'])
    dias = {'1':dias1,'2':dias2,'3':dias3}
    for numero_dia in dias.keys():
        for dia in dias[numero_dia]:
            numero_dia=1
            nueva_franja, nuevo_salon, nueva_seccion, nuevo_curso, nueva_clase = seleccionar_datos(diccionario,i,dia,numero_dia)
            print(nueva_franja,nuevo_salon,nueva_seccion,nuevo_curso,nueva_clase)
            franja_existe = 0
            for f in franjas:
                if nueva_franja.id == f.id:
                    franja_existe = 1
                    f.clases.append(nueva_clase)
                    break
            if not franja_existe:
                if not pd.isnull(nueva_franja.id):
                    nueva_franja.clases.append(nueva_clase)
                    franjas.append(nueva_franja)

            salon_existe = 0
            for s in salones:
                if nuevo_salon.senhalizacion == s.senhalizacion:
                    salon_existe = 1
                    s.clases.append(nueva_clase)
                    break
            if not salon_existe:
                if not pd.isnull(nuevo_salon.senhalizacion):
                    nuevo_salon.clases.append(nueva_clase)
                    salones.append(nuevo_salon)

            seccion_existe = 0
            for s in secciones:
                if nueva_seccion.id == s.id:
                    seccion_existe = 1
                    s.clases.append(nueva_clase)
                    break
            if not seccion_existe:
                if not pd.isnull(nueva_seccion.id):
                    nueva_seccion.clases.append(nueva_clase)
                    secciones.append(nueva_seccion)

            curso_existe = 0
            for c in cursos:
                if nuevo_curso.materia == c.materia:
                    curso_existe = 1
                    c.clases.append(nueva_clase)
                    break
            if not curso_existe:
                if not pd.isnull(nuevo_curso.materia):
                    nuevo_curso.clases.append(nueva_clase)
                    cursos.append(nuevo_curso)

            clase_existe = 0
            for c in clases:
                if nueva_clase.id == c.id:
                    clase_existe = 1
                    break
            if not clase_existe:
                if not pd.isnull(nueva_clase.id):
                    clases.append(nueva_clase)
            i = i + 1


#Cargar
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
