from cubes import StaticModelProvider
from cubes import Workspace

workspace = Workspace()
workspace.register_default_store("sql", url="sqlite:///BI.db")
dicc = {
    "cubes": [
        {
            "name": "clase",
            "label": "Clases",
            "dimensions": ["franja","seccion","salon","curso"]
        }
    ],
    "dimensions": [
        {
            "name": "franja",
            "label": "Franja",
            "attributes": [
                {
                  "name": "dia",
                  "label": "Dia"
                },
                {
                  "name": "hora_inicio",
                  "label": "Hora de inicio",
                },
                {
                  "name": "minuto_inicio",
                  "label": "Minuto de inicio",
                },
                {
                  "name": "hora_fin",
                  "label": "Hora de finalizacion",
                },
                {
                  "name": "minuto_fin",
                  "label": "Minuto de finalizacion",
                },
                {
                  "name": "duracion",
                  "label": "Duracion",
                }
            ]
        },
        {
            "name": "salon",
            "label": "Salon",
            "attributes": [
                {
                  "name": "senhalizacion",
                  "label": "Senhalizacion"
                },
                {
                  "name": "edificio",
                  "label": "Edificio",
                },
                {
                  "name": "capacidad",
                  "label": "Capacidad",
                },
                {
                  "name": "extension",
                  "label": "Extension",
                },
                {
                  "name": "area",
                  "label": "Area",
                },
                {
                  "name": "tiene_movil_express",
                  "label": "Movil Express",
                },
                {
                  "name": "tipo_mobiliario",
                  "label": "Tipo de mobiliario",
                },
                {
                  "name": "es_fijo",
                  "label": "Es fijo",
                }
            ]
        },
        {
            "name": "seccion",
            "label": "Seccion",
            "attributes": [
                {
                  "name": "crn",
                  "label": "CRN"
                },
                {
                  "name": "semestre",
                  "label": "Semestre",
                },
                {
                  "name": "numero_seccion",
                  "label": "Numero seccion",
                },
                {
                  "name": "cupos",
                  "label": "Cupos",
                },
                {
                  "name": "inscritos",
                  "label": "Inscritos",
                },
                {
                  "name": "disponibles",
                  "label": "Disponibles",
                },
                {
                  "name": "profesor1",
                  "label": "Profesor 1",
                },
                {
                  "name": "profesor2",
                  "label": "Profesor 2",
                },
                {
                  "name": "profesor3",
                  "label": "Profesor 3",
                }
            ]
        },
        {
            "name": "curso",
            "label": "Curso",
            "attributes": [
                {
                  "name": "materia",
                  "label": "Materia"
                },
                {
                  "name": "nombre",
                  "label": "Nombre curso",
                },
                {
                  "name": "creditos",
                  "label": "Numero de creditos",
                }
            ]
        },
        {
            "name": "clase",
            "label": "Clase",
            "attributes": [
                {
                  "name": "curso_materia",
                  "label": "Materia"
                },
                {
                  "name": "seccion_id",
                  "label": "Seccion",
                },
                {
                  "name": "salon_senhalizacion",
                  "label": "Salon",
                },
                {
                  "name": "franja_id",
                  "label": "Franja",
                }
            ]
        }
    ]
}

workspace.import_model(dicc)
browser = workspace.browser("clase")
result = browser.aggregate( drilldown=['franja'])
print(result)
