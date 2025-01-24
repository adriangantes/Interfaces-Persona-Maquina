#!/usr/bin/env python3

from model import PatientModel #importa el modelo
from view import PatientView #importa la vista
#from adwview1 import PatientView
# from adwview2 import PatientView
from presenter import PatientPresenter #importa el presenter

if __name__ == "__main__":
    presenter = PatientPresenter(model=PatientModel(), view=PatientView()) #crea el presenter y le pasa el modelo y la vista
    presenter.run(application_id="gal.udc.fic.ipm.PatientList") #llama a run del presenter para que empiece la aplicacion
    #y le pasas el id de la app
