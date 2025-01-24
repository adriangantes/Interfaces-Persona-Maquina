#El sig. codigo define un modelo que interactua con una API REST para gestionar las consultas sobre pacientes y medicacion; su enfoque
#es la de realizar consultas HTTP a un servidor que le devolvera la info requerida y el modelo procesara las respuestas para enviarlas
#a la aplicacion

import requests #libreria de python para hacer y recibir HTTP (hacer consultas HTTP)

SERVER_URL="http://localhost:8000" #direcion del servidor; su URL

class ModelException(Exception): #Una clase para el tipi de excepciones que pueden ocurrir en el Modelo
    #es una clase para dar excepciones personalizadas; entre () va Exception porque hereda de la clase Exception
    def __init__(self, msg: str):
        super().__init__(msg) #llama a la clase padre y le pasa la excepcion

class Patient: #clase paciente para modelar un paciente segun los datos obtenidos por el SERVER
    def __init__(self, data=None): # el constructor acepta un dicionario data y asigna dinamicamente sus claves y valores como
        #atributos del objeto Patient usando setattr; es decir; convierte la respuesta JSON del servidor en un objeto tipo Patient
        if data is not None: #si el dicicionario tiene informacion; es decir; no es None
            for key, value in data.items(): #por cada valor del dicionario 
                setattr(self, key, value) # lo convierte en un objeto Patient; donde key sera el campo y value su valor

class Medication: #clase paciente para modelar un paciente segun los datos obtenidos por el SERVER
    def __init__(self, data=None): # el constructor acepta un dicionario data y asigna dinamicamente sus claves y valores como
        #atributos del objeto Patient usando setattr; es decir; convierte la respuesta JSON del servidor en un objeto tipo Patient
        if data is not None: #si el dicicionario tiene informacion; es decir; no es None
            for key, value in data.items(): #por cada valor del dicionario
                setattr(self, key, value)


class Posologie:
    def __init__(self, data=None):
        if data is not None: #si el dicicionario tiene informacion; es decir; no es None
            for key, value in data.items(): #por cada valor del dicionario
                setattr(self, key, value)


'''
class Medication: #clase medicacion par modelar la medicacion segun los datos obtenidos por el server
    def __init__(self, data=None):
        # Inicializa los atributos de la clase
        self.id = None
        self.name = None
        self.dosage = None
        self.start_date = None
        self.treatment_duration = None
        self.patient_id = None
        if data is not None:
            self.id = data.get('id')  # Agregado para incluir el id
            self.name = data.get('name')
            self.dosage = data.get('dosage')
            self.start_date = data.get('start_date')
            self.treatment_duration = data.get('treatment_duration')
            self.patient_id = data.get('patient_id')
'''
#no puedo hacer otro modelo, sera uno compartido ya q en el app se le pasa este modelo al igual q en el view
class PatientModel:
    def __init__(self): #constructor innit; en este caso no hace nada; esta ahi por si en algun futuro pudiera ser de utilidad; no hace
        #nada por eso tiene el pass
        pass

#para saber las consultas etc usar la doc -> http://0.0.0.0:8000/docs
    def get_medications(self, id_patient: int) -> list:
        url = f"{SERVER_URL}/patients/{id_patient}/medications"
        response = requests.get(url) #se lanza la peticion GET al Server con la consulta
        data = response.json() #se convierte la respuesta JSON del server a un dicionario de datos de python
        if response.ok: #si tuvo exito la respuesta (ok)
            #tengo q convertir la lista
            medications = []
            for i in data:
                medications.append(Medication(i))
            #medications = [Medication(item) for item in data]
            return medications #devuelvo la lista
        else: #si no hubo exito
            raise ModelException(data["detail"])

    def get_medication(self, id: int, id_patient: int) ->Medication:
        #funcion para obtener una medicacion
        url = f"{SERVER_URL}/patients/{id_patient}/medications/{id}"
        response = requests.get(url)
        data = response.json()
        if response.ok:
            return Medication(data)
        else:
            raise ModelException(data["detail"])

    def get_posologies(self, id: int, id_patient: int) -> list:
        url = f"{SERVER_URL}/patients/{id_patient}/medications/{id}/posologies"
        response = requests.get(url) #se lanza la peticion GET al Server con la consulta
        data = response.json() #se convierte la respuesta JSON del server a un dicionario de datos de python
        if response.ok: #si tuvo exito la respuesta (ok)
            #tengo q convertir la lista
            posologias = []
            for i in data:
                posologias.append(Posologie(i))
            return posologias #devuelvo la lista
        else: #si no hubo exito
            raise ModelException(data["detail"])

    def get_patients(self, start_index: int, count: int) -> list: #metodo para obtener pacientes desde el servidor
        url = f"{SERVER_URL}/patients" #la url donde solocitar pacientes
        if start_index is not None or count is not None: #si se le proporciona un stat_index o un count (count -> numero pacientes q
            #quiere) o start_index -> desde donde pillarlos; pues agrega estos parametros a la consula añadiendolos a la URL
            url += "?" #? por q vienen parametros de consulta 
            if start_index is not None:
                url += f"start_index={start_index}&" #añade el parametro start_index a la cosnulta
            if count is not None:
                url += f"count={count}" #añade el parametro count a la consulta

        response = requests.get(url) #obtiene la respuesta lanzando la peticion GET al server
        data = response.json() #convierte la respuesta json del servidor en un dicionario de datos de python

        if response.ok: #si la respeusta fue exitosa (ok)
            patient_list = [] #se crea una lista de pacientes
            for item in data: #para cada elemento del dicionario de datos data
                patient_list.append(Patient(item)) #se convierte el elemento del dicionario a un elemento tipo Patient con Patient
                #(item) y lo añade a al lista
            return patient_list #devuelve la lista de pacientes
        else: #si la respuesta no fue exitosa
            raise ModelException(data["detail"]) #lanza una excepcion modelo con el detalle del error data["detail"]
        
    def get_patient(self, id: int) -> Patient: #metodo para obtener un solo paciete; se necesita del id del paciente
        url = f"{SERVER_URL}/patients/{id}" #se forma la URL de la consulta con el id del paciente
       
        response = requests.get(url) #se lanza la peticion GET al Server con la consulta
        data = response.json() #se convierte la respuesta JSON del server a un dicionario de datos de python
        if response.ok: #si tuvo exito la respuesta (ok)
           return Patient(data) #se convierte el dicionario a un objeto tipo Paciente (Patient(data)) y se devuelve
        else: #si no hubo exito
            raise ModelException(data["detail"]) #se lanza una excepcion model con los detalles del error


    def add_medication (self, medicationName: str, dosage: float, start_date: str, treatment_duration: int, idPaciente: int) -> None:
        url = f"{SERVER_URL}/patients/{idPaciente}/medications/" #url para añadir medicacion
        #preparar el json
        payload = {
            "name": medicationName, #nombre del medicamento
            "dosage": dosage, #Dosis
            "start_date": start_date, #fecha inicio
            "treatment_duration": treatment_duration,
        }
        response = requests.post(url, json=payload) #añadir medicacion a ese paciente
        if response.ok:
            #si respuesta es correcta , el server no devuelve nada
            return None
        else:
            #si la respuesta no es correcta nos devuelve info del error
            data = response.json()  # devuelve un error si no, la info del error
            raise ModelException(data["detail"]) #se lanza una excepcion si la respuesta no es ok

    def eliminarMedicamentoPaciente(self, idPaciente: int, idMedicamento: int) -> None:
        #funcion para eliminar un medicamento de un paciente
        url = f"{SERVER_URL}/patients/{idPaciente}/medications/{idMedicamento}" #url para eliminar
        response = requests.delete(url) #elimino la esa medicacion de ese paciente
        if response.ok:
            #si respuesta es correcta , el server no devuelve nada
            return None
        else:
            #si la respuesta no es correcta nos devuelve info del error
            data = response.json()  # devuelve un error si no, la info del error
            raise ModelException(data["detail"]) #se lanza una excepcion si la respuesta no es ok

    def eliminarPosologia(self, patient_id: int, medication_id: int, posologie_id: int) -> None:
        # funcion para eliminar un medicamento de un paciente
        url = f"{SERVER_URL}/patients/{patient_id}/medications/{medication_id}/posologies/{posologie_id}"  # url para eliminar
        response = requests.delete(url)  # elimino esa posologia de ese paciente
        if response.ok:
            # si respuesta es correcta , el server no devuelve nada
            return None
        else:
            # si la respuesta no es correcta nos devuelve info del error
            data = response.json()  # devuelve un error si no, la info del error
            raise ModelException(data["detail"])  # se lanza una excepcion si la respuesta no es ok

    def guardarCambiosMedicamento(self, idMedication: int, medicationName: str, dosage: float, start_date: str,treatment_duration: int, idPaciente: int) -> None:
        #hacer un PATH
        url = f"{SERVER_URL}/patients/{idPaciente}/medications/{idMedication}"
        #preparar el json que se va a enviar
        payload = {
            "name": medicationName,  # Nombre del medicamento
            "dosage": dosage,  # Dosis
            "start_date": start_date,  # Fecha de inicio del tratamiento
            "treatment_duration": treatment_duration  # Duración del tratamiento en días
        }

        #solicitud PATCH
        response = requests.patch(url, json=payload) #se envia la peticion con los campos actualizados
        if response.ok:
            return None
        else:
            data = response.json()
            raise ModelException(data["detail"])

    def guardarCambiosPosologia(self, idMedication: int, idPaciente: int, idPosologia: int, hour: int, minute: int) -> None:
        # hacer un PATH
        url = f"{SERVER_URL}/patients/{idPaciente}/medications/{idMedication}/posologies/{idPosologia}"
        # preparar el json que se va a enviar
        payload = {
            "hour": hour,  # horas
            "minute": minute,  # minutos
        }

        # solicitud PATCH
        response = requests.patch(url, json=payload)  # se envia la peticion con los campos actualizados
        if response.ok:
            return None
        else:
            data = response.json()
            raise ModelException(data["detail"])

    def add_posologie(self, idPaciente: int, idMedication: int, hour: int, minute: int) -> list:
        url = f"{SERVER_URL}/patients/{idPaciente}/medications/{idMedication}/posologies/"  # url para añadir posologia
        # preparar el json
        payload = {
            "hour": hour,  # hour
            "minute": minute,  # minute
        }
        response = requests.post(url, json=payload)  # añadir posologia para ese paciente y medicacion
        if response.ok:
            # si respuesta es correcta , el server no devuelve nada
            return None
        else:
            # si la respuesta no es correcta nos devuelve info del error
            data = response.json()  # devuelve un error si no, la info del error
            raise ModelException(data["detail"])  # se lanza una excepcion si la respuesta no es ok