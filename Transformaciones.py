from etl import *
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
