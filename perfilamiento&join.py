import pandas as pd
import pandas_profiling
import numpy as np

cartelera = pd.read_csv("./cursos_scraped_full.csv",
                        error_bad_lines=False,
                        sep=";",
                        encoding="UTF-8")
salones = pd.read_csv("./subirsalones_2018-1.csv",
                      error_bad_lines=False,
                      sep=";",
                      encoding="UTF-8")

pf1 = pandas_profiling.ProfileReport(cartelera)
pf2 = pandas_profiling.ProfileReport(salones)

pf1.to_file(outputfile="./cartelera.html")
pf2.to_file(outputfile="./salones.html")

# Create new column for room 1
col_s1 = {'Bloque_s1': [], '1Salon': [], 'Tipo Mobiliario_s1': [],
          'Fijo/Movil_s1': [], 'Capacidad_s1': [], 'Area util_s1': [],
          'Ext_s1': [], 'Movil Express_s1': []
          }

# Create new column for room 2
col_s2 = {'Bloque_s2': [], '2Salon': [], 'Tipo Mobiliario_s2': [],
          'Fijo/Movil_s2': [], 'Capacidad_s2': [], 'Area util_s2': [],
          'Ext_s2': [], 'Movil Express_s2': []
          }

# Create new column for room 2
col_s3 = {'Bloque_s3': [], '3Salon': [], 'Tipo Mobiliario_s3': [],
          'Fijo/Movil_s3': [], 'Capacidad_s3': [], 'Area util_s3': [],
          'Ext_s3': [], 'Movil Express_s3': []
          }

s1 = cartelera['1Salon']
for it in s1:
    data = salones.loc[salones['SEÑALIZACIÓN'] == it]
    if not data.empty:
        col_s1['Bloque_s1'].append(str(data['BLOQUE'].values[0]))
        col_s1['1Salon'].append(it)
        col_s1['Tipo Mobiliario_s1'].append(str(data['TIPO MOBILIARIO'].values[0]))
        col_s1['Fijo/Movil_s1'].append(str(data['FIJO/MOVIL'].values[0]))
        col_s1['Capacidad_s1'].append(str(data['CAPACIDAD '].values[0]))
        col_s1['Area util_s1'].append(str(data['ÁREA ÚTIL'].values[0]))
        col_s1['Ext_s1'].append(str(data['EXT'].values[0]))
        col_s1['Movil Express_s1'].append(str(data['MÓVIL XPRESS'].values[0]))
    else:
        col_s1['Bloque_s1'].append('')
        col_s1['1Salon'].append('')
        col_s1['Tipo Mobiliario_s1'].append('')
        col_s1['Fijo/Movil_s1'].append('')
        col_s1['Capacidad_s1'].append('')
        col_s1['Area util_s1'].append('')
        col_s1['Ext_s1'].append('')
        col_s1['Movil Express_s1'].append('')

s2 = cartelera['2Salon']
for it in s2:
    data = salones.loc[salones['SEÑALIZACIÓN'] == it]
    if not data.empty:
        col_s2['Bloque_s2'].append(str(data['BLOQUE'].values[0]))
        col_s2['2Salon'].append(it)
        col_s2['Tipo Mobiliario_s2'].append(str(data['TIPO MOBILIARIO'].values[0]))
        col_s2['Fijo/Movil_s2'].append(str(data['FIJO/MOVIL'].values[0]))
        col_s2['Capacidad_s2'].append(str(data['CAPACIDAD '].values[0]))
        col_s2['Area util_s2'].append(str(data['ÁREA ÚTIL'].values[0]))
        col_s2['Ext_s2'].append(str(data['EXT'].values[0]))
        col_s2['Movil Express_s2'].append(str(data['MÓVIL XPRESS'].values[0]))
    else:
        col_s2['Bloque_s2'].append('')
        col_s2['2Salon'].append('')
        col_s2['Tipo Mobiliario_s2'].append('')
        col_s2['Fijo/Movil_s2'].append('')
        col_s2['Capacidad_s2'].append('')
        col_s2['Area util_s2'].append('')
        col_s2['Ext_s2'].append('')
        col_s2['Movil Express_s2'].append('')

s3 = cartelera['3Salon']
for it in s3:
    data = salones.loc[salones['SEÑALIZACIÓN'] == it]
    if not data.empty:
        col_s3['Bloque_s3'].append(str(data['BLOQUE'].values[0]))
        col_s3['3Salon'].append(it)
        col_s3['Tipo Mobiliario_s3'].append(str(data['TIPO MOBILIARIO'].values[0]))
        col_s3['Fijo/Movil_s3'].append(str(data['FIJO/MOVIL'].values[0]))
        col_s3['Capacidad_s3'].append(str(data['CAPACIDAD '].values[0]))
        col_s3['Area util_s3'].append(str(data['ÁREA ÚTIL'].values[0]))
        col_s3['Ext_s3'].append(str(data['EXT'].values[0]))
        col_s3['Movil Express_s3'].append(str(data['MÓVIL XPRESS'].values[0]))
    else:
        col_s3['Bloque_s3'].append('')
        col_s3['3Salon'].append('')
        col_s3['Tipo Mobiliario_s3'].append('')
        col_s3['Fijo/Movil_s3'].append('')
        col_s3['Capacidad_s3'].append('')
        col_s3['Area util_s3'].append('')
        col_s3['Ext_s3'].append('')
        col_s3['Movil Express_s3'].append('')

pds1 = pd.DataFrame(col_s1)
pds2 = pd.DataFrame(col_s2)
pds3 = pd.DataFrame(col_s3)

pds1.to_csv('./car_salon1.csv', sep=',')
pds2.to_csv('./car_salon2.csv', sep=',')
pds3.to_csv('./car_salon3.csv', sep=',')
