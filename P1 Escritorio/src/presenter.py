#Codigo del presenter; (el que se comunica entre view y model)

from typing import Any #libreria para hacer anotaciones
from view import PatientView, run #importas la view 
from model import PatientModel, ModelException #importas el modelo
import threading
from gi.repository import GLib

#traduciones
from lang import gettext as _

COUNT = 15 #valor usado para obtener pacientes; numero de pacientes que se quiere obtener en el init_list() mas adelanta explicado

#la Clase PatientPresenter sera en intermediario entre PatientView y PatientModel
class PatientPresenter:
    def __init__(self, model: PatientModel, view: PatientView): #metodo init; constructor que inicializa el objeto de PatientPresenter
        #se le pasa un modelo y una vista y los asigna
        self.model = model
        self.view = view

    def run(self, application_id: str): #metodo que inicia la aplicacion conectando la vista y el modelo
        self.view.set_handler(self) #en la vista establece que el manejador sera el mismo, el presenter
        run(application_id,
            on_activate=self.view.on_activate) #llama a la funcion run y le pasa el application id y la funcion on_activate definina
            #en la vista
    		
	
    def _waiting(self, thread: threading) -> None:
        self.view.set_sensitive_spinner(True) #activamos spinner
        thread.start() #no es adecuado hacer thread_join ya que me espera a que el hilo acabe de ejecutar y esto bloquearia la interfaz grafica
        # el spinner se lo pedimos parar a la libreria desde la funcion background que tiene que hacer el thread
        #lo haremos con Glib.idle_add lo que nos permite poner una tarea al loop de eventos de Gtk (hilo prinicpal de la interfaz)

    def on_patient_selected(self, id: int) -> None: #define el on_patient_selected; este metodo maneja la seleccion de un paciente de 
        #la lista
        #funcion  para el thread
        def worker():
            try:
                patient = self.model.get_patient(id) #intenta quitar el paciente del q le pasan el id llamando al modelo y pasandole el
                # si se selecciona un paciente tengo q obtener y actualizar toda la lista de medicamentos de ese paciente
                medications = self.model.get_medications(id)  # se le pasa el id del paciente

                #paciente
                GLib.idle_add(self.view.set_patient, patient.code, patient.name, patient.surname) #establece el paciente en la vista con los campos de
                #si hay paciente selecionado activo boton añadir medicamento
                GLib.idle_add(self.view.set_sensitive_anadir_medicationButton, True)
                #este
                #si se seleciona un medicamento y se estaba por cualquier motivo creadno un medicamento aun no hecho; hay q desactivar la caja de añadir medicamento
                GLib.idle_add(self.view.set_sensitive_MedicationAddBox, False)
                #actualizo la vista de medicamentos
                GLib.idle_add(self.view.set_medications, medications) #se le pasa la lista de medicamentos
                #hacer que la caja de informacion de medicamento este desactivada (por si de un paciente y en su medicacion), pulsa en otro paciente
                GLib.idle_add(self.view.set_sensitive_MedicationInformationBox, False)
            except Exception as e:
                GLib.idle_add(self.view.show_message, str(e)) #si ocurre alguna excepcion, lanza una ventana de dialogo (se encarga la vista) con el
                #mensaje de la excepcion
            finally: #codigo que simepre se ejecutra (desactivar el spinner)
                GLib.idle_add(self.view.set_sensitive_spinner, False)
        thread = threading.Thread(target=worker) #si añades daemon=True; si el hilo principal se cierra van los detras en cascada a cerrarse sin esperar a q acaben
        self._waiting(thread)
    '''
    NO SE USA LA ESTRELLA
    def on_patient_toggle_starred(self, id: int) -> None: #metodo para marcar lo de favorito el paciente
        # Do something in the model (not supported by the current backend) #no soportado por el actual backend asi que 
        self.view.toggle_starred(id) #de momento no marca nada en el backend y solo actualiza la vista llamando al metodo toggleStarred
    '''
    def init_list(self) -> None: #metodo para iniciar la lista que usa la view en on_activate
        def worker():
            try:
                patients = self.model.get_patients(0, COUNT) #inicializa la lista de pacientes; cargando los primeros COUNT pacientes desde
                #el modelo
                if len(patients) > 0: #si hay al menos un paciente
                    GLib.idle_add(self.view.set_patients, patients) #se establecen los pacientes en la vista para que se muestren; se les pasa esos COUNT
                    #pacientes a la vista para que los muestre por pantalla
                    GLib.idle_add(self.view.set_current_page, 0) #establece en la vista que la pagina actual es la 0
                else:
                    GLib.idle_add(self.view.set_sensitive_next, False) #si no hay pacientes pues el boton next se desactiva
                    GLib.idle_add(self.view.show_message, _("No more patients")) #se muestra una ventana de dialogo diciendo que no hay mas pacientes
            except Exception as e:
                GLib.idle_add(self.view.show_message, str(e)) #si hay alguna excepcion, se abre una ventana de dialogo mostrando el error de la excepcion
            finally: #codigo que simepre se ejecutra (desactivar el spinner)
                GLib.idle_add(self.view.set_sensitive_spinner, False)

        # Lanzar el hilo
        thread = threading.Thread(target=worker)
        self._waiting(thread)

    def on_load_page(self, idx: int) -> None: #metodo para manejar la carga de pacientes en funcion de la pagina solicitada
        #idx es la pagina solicitada y esta funcion es llamada por la vista cuando el boton sig pagina o anterior es clickado q se 
        #le pasa a esta funcion como parametro la actual pagina +1 o -1 (next/prev) y por tanto la pagina a mostrar es el parametro idx
        def worker():
            if idx >= 0: #si la pagina no es negativa logicamente
                try: #intenta
                    patients = self.model.get_patients(COUNT * idx, COUNT) #quita otros COUNT pacientes desde COUNT*idx ya que en cada
                    #pagina se pueden mostrar COUNT pacientes; por tanto, quita los pacientes desde inicio y a fin de la pagina que se
                    #pasa por idx
                    if len(patients) > 0: #si devuelve paceintes el modelo; es que hay pacientes para esa pagina
                        GLib.idle_add(self.view.set_patients, patients) #se le dice a la view que actualize la lista de pacientes con los nuevos pacientes
                        GLib.idle_add(self.view.set_sensitive_previous, True) #se activa el boton para atras en la vista
                        GLib.idle_add(self.view.set_sensitive_next, True) #se activa el boton next (para adelante) en la vista
                        GLib.idle_add(self.view.set_current_page, idx) #se establece la actual pagina en la vista a idx
                    else: #si no hay pacientes es que es la ultima lista
                        GLib.idle_add(self.view.set_sensitive_next, False) #se pone en la vista que se descative el boton siguiente (no hay mas pacientes)
                        GLib.idle_add(self.view.show_message, _("No more patients")) #se muestra en la vista una ventana de dialogo diciendo que no hay mas
                        #pacientes (es la ultima pagina)
                except Exception as e:
                    GLib.idle_add(self.view.show_message, str(e)) #si ocurre una excepcion durante la ejecucion del try pues que se establece en la vista
                    #que abra una ventana de dialogo y muestre el mensaje de error recogido en la excepcion
                finally:  # codigo que simepre se ejecutra (desactivar el spinner)
                    GLib.idle_add(self.view.set_sensitive_spinner, False)

            else: #si la pagina que se pide es -1 es porque la actual era 0 por tanto no hay mas paginas atras posibles
                GLib.idle_add(self.view.set_sensitive_previous, False) #se descativa el boton previous
                GLib.idle_add(self.view.show_message, _("No more patients")) #se muestra una ventana de dialogo diciendo que no hay mas pacientes
                #es la primera pagina (no se puede ir mas para atras)
                GLib.idle_add(self.view.set_sensitive_spinner, False)

        # Lanzar el hilo
        thread = threading.Thread(target=worker)
        self._waiting(thread)


    def on_medication_selected(self, id: int, id_patient: int) -> None:
        def worker():
            try:
                #si se clicka en un medicamento tenemos que recuperar la informacion de ese medicamento y recargar la pagina
                medication = self.model.get_medication(id, id_patient) #obtenemos la medicacion
                #ahora toca actualizar la vista
                '''FUNCION PARA AÑADIR LA VISTA ; llamar a una funcion (q hay q crear) de la vista para que cambie de pantalla'''
                GLib.idle_add(self.view.set_sensitive_MedicationAddBox, False) #si estaba añiendo y pulsa en un medicamento, que se desactive la caja de añadir medicamento
                GLib.idle_add(self.view.set_sensitive_MedicationPosologieBox, False) #desacativar la vista de la caja de posologias
                GLib.idle_add(self.view.set_sensitive_AddPosologieBox, False) #desactivar la vista de añadir posologias
                GLib.idle_add(self.view.cargar_datos_medicamento, medication) #que carge los datos del medicamento
                #sacar las posologias
                posologias = self.model.get_posologies(id, id_patient)
                #mostrar las posologias
                GLib.idle_add(self.view.set_posologies,posologias)
            except Exception as e:
                GLib.idle_add(self.view.show_message, str(e))  # si hay alguna excepcion, se abre una ventana de dialogo mostrando el error de la excepcion
            finally:  # codigo que simepre se ejecutra (desactivar el spinner)
                GLib.idle_add(self.view.set_sensitive_spinner, False)
        
        # Lanzar el hilo
        thread = threading.Thread(target=worker)
        self._waiting(thread)

    def on_medication_confirmAddButton(self,idPaciente: int, medicationName: str, dosage: float, start_date: str, treatment_duration: int) -> None:
        def worker():
            try:
                #funcion para añadir medicacion
                self.model.add_medication(medicationName, dosage, start_date, treatment_duration, idPaciente)
                #sacar la nueva lista de medicamentos
                medications = self.model.get_medications(idPaciente) #sacar lista de medicamentos
                #ahora toca actualizar la vista
                '''FUNCION PARA AÑADIR LA VISTA ; llamar a una funcion (q hay q crear) de la vista para que cambie de pantalla'''
                GLib.idle_add(self.view.set_sensitive_MedicationAddBox, False) #desactivar la pantalla de añadir medicacion
                #actualizar vista de medicamentos
                GLib.idle_add(self.view.set_medications, medications)
            except Exception as e:
                GLib.idle_add(self.view.show_message, str(e))  # si hay alguna excepcion, se abre una ventana de dialogo mostrando el error de la excepcion
            finally:  # codigo que simepre se ejecutra (desactivar el spinner)
                GLib.idle_add(self.view.set_sensitive_spinner, False)
        # Lanzar el hilo
        thread = threading.Thread(target=worker)
        self._waiting(thread)


    def on_medication_eliminarButton(self, idPaciente: int, idMedicamento: int) -> None:
        def worker():
            try:
                #funcion para elimiar el medicamento selecionado
                self.model.eliminarMedicamentoPaciente (idPaciente, idMedicamento)
                #Actualizar vista
                #el modelo ahora le pido que me muestre los medicamentos
                medications = self.model.get_medications(idPaciente)
                #actualizo la vista
                #desactivar vista formulario medicamento eliminado
                GLib.idle_add(self.view.set_sensitive_MedicationInformationBox, False)
                GLib.idle_add(self.view.set_medications, medications) #le pasamos la lista de medicamentos
            except Exception as e:
                GLib.idle_add(self.view.show_message, str(e))  # si hay alguna excepcion, se abre una ventana de dialogo mostrando el error de la excepcion
            finally:  # codigo que simepre se ejecutra (desactivar el spinner)
                GLib.idle_add(self.view.set_sensitive_spinner, False)
        # Lanzar el hilo
        thread = threading.Thread(target=worker)
        self._waiting(thread)

    def guardarCambiosMedicamento(self, idMedication: int, medicationName: str, dosage: float, start_date: str, treatment_duration: int, idPaciente: int) ->None :
        def worker():
            try:
                #guardar cambios del medicamento
                self.model.guardarCambiosMedicamento(idMedication, medicationName, dosage, start_date, treatment_duration, idPaciente)
                #sacar el medicamento
                medication = self.model.get_medication(idMedication,idPaciente)
                #actualiar la vista
                #self.view.cargar_datos_medicamento(medication) #no hace falta cargar ahora los datos del medicamento ya q en modificar... al selecionar la fila se va a ejeuctar lo de cargar datos del medicamento
                GLib.idle_add(self.view.modificarMedicamentoListaMedicamentos, medication) #actualizar la lista de medicamentos con el medicamento nuevo
                #mostrar mensaje de cambios guardados
                GLib.idle_add(self.view.mostrar_notificacion_temporal, self.view.guardarCambiosMedicamentoButton, _("Changes Saved"))
            except Exception as e:
                GLib.idle_add(self.view.show_message,str(e))  # si hay alguna excepcion, se abre una ventana de dialogo mostrando el error de la excepcion
            finally:  # codigo que simepre se ejecutra (desactivar el spinner)
                GLib.idle_add(self.view.set_sensitive_spinner, False)
        # Lanzar el hilo
        thread = threading.Thread(target=worker)
        self._waiting(thread)

    def on_posologie_selected(self, idPatient: int, idPosologie: int, idMedication: int) -> None:

        def worker():
            try:
                #selecionar posologia y mostrarla; como no hay un metodo en el model pedimos todas las posologias y buscamos la q sea
                posologias = self.model.get_posologies(idMedication, idPatient)
                #mostrar boton eliminar posologia activado
                GLib.idle_add(self.view.set_sensitive_eliminar_posologiaButton, True)
                posologia = None
                for i in posologias:
                    if i.id == idPosologie:
                        posologia = i
                        break #salir del bucle
                if posologia is None:
                    #no se encontro
                    GLib.idle_add(self.view.show_message, _("Error, Posologie not found"))
                #desactivar caja añadir posologia
                GLib.idle_add(self.view.set_sensitive_AddPosologieBox, False)
                #mostrar datos actualizados posologia
                GLib.idle_add(self.view.cargar_datos_posologia, posologia)
            except Exception as e:
                GLib.idle_add(self.view.show_message,str(e))  # si hay alguna excepcion, se abre una ventana de dialogo mostrando el error de la excepcion
            finally:  # codigo que simepre se ejecutra (desactivar el spinner)
                GLib.idle_add(self.view.set_sensitive_spinner, False)
        # Lanzar el hilo
        thread = threading.Thread(target=worker)
        self._waiting(thread)

    def on_posologie_delete_button(self, patient_id: int, medication_id: int, posologie_id: int) ->None:
        
        def worker():
            try:
                # funcion para elimiar la posologia selecionada
                self.model.eliminarPosologia (patient_id, medication_id, posologie_id)
                # Actualizar vista
                # el modelo ahora le pido que me muestre las posologias
                posologias = self.model.get_posologies(medication_id, patient_id)
                # actualizo la vista
                # desactivar vista formulario posologia eliminada
                GLib.idle_add(self.view.set_sensitive_MedicationPosologieBox, False)
                GLib.idle_add(self.view.set_posologies, posologias)  # le pasamos la lista de posologias
            except Exception as e:
                GLib.idle_add(self.view.show_message, str(e))  # si hay alguna excepcion, se abre una ventana de dialogo mostrando el error de la excepcion
            finally:  # codigo que simepre se ejecutra (desactivar el spinner)
                GLib.idle_add(self.view.set_sensitive_spinner, False)
        # Lanzar el hilo
        thread = threading.Thread(target=worker)
        self._waiting(thread)

    def guardarCambiosPosologia(self, idMedication: int, idPaciente: int, idPosologia: int, hour: int, minute: int) -> None:

        def worker():
            try:
                #guardar cambios posologia
                self.model.guardarCambiosPosologia (idMedication, idPaciente, idPosologia, hour, minute)
                #sacar la posologia
                posologias = self.model.get_posologies(idMedication,idPaciente)
                #encontrar la posologia
                posologia = None
                for i in posologias:
                    if i.id == idPosologia:
                        posologia = i
                        break  # salir del bucle
                if posologia is None:
                    # no se encontro
                    GLib.idle_add(self.view.show_message, _("Error, Posologie not found"))

                #actualiar la vista
                GLib.idle_add(self.view.modificarPosologiaListaPosologias, posologia) #actualizar la lista de posologias con el posologia nuevo
                #mostrar mensaje de cambios guardados
                GLib.idle_add(self.view.mostrar_notificacion_temporal, self.view.confirmarGuardarPosologiaButton, _("Changes Saved"))
            except Exception as e:
                GLib.idle_add(self.view.show_message,str(e))  # si hay alguna excepcion, se abre una ventana de dialogo mostrando el error de la excepcion
            finally:  # codigo que simepre se ejecutra (desactivar el spinner)
                GLib.idle_add(self.view.set_sensitive_spinner, False)
        # Lanzar el hilo
        thread = threading.Thread(target=worker)
        self._waiting(thread)

    def on_posologia_confirmAddButton(self, idPaciente: int, idMedication: int, hour: int, minute: int) -> None:

        def worker():
            try:
                # funcion para añadir posologia
                self.model.add_posologie (idPaciente, idMedication, hour, minute)
                # sacar la nueva lista de posologias
                posologies = self.model.get_posologies(idMedication, idPaciente) #sacar lista de posologias
                # ahora toca actualizar la vista
                GLib.idle_add(self.view.set_sensitive_AddPosologieBox, False)  # desactivar la pantalla de añadir posologia
                # actualizar vista de posologias
                GLib.idle_add(self.view.set_posologies, posologies)
            except Exception as e:
                GLib.idle_add(self.view.show_message, str(e))  # si hay alguna excepcion, se abre una ventana de dialogo mostrando el error de la excepcion
            finally:  # codigo que simepre se ejecutra (desactivar el spinner)
                GLib.idle_add(self.view.set_sensitive_spinner, False)

        # Lanzar el hilo
        thread = threading.Thread(target=worker)
        self._waiting(thread)