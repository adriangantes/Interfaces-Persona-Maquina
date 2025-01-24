from cProfile import label
from operator import length_hint
from typing import Callable, Protocol, Any  #importar para definir protocolos y las anotaciones
from datetime import datetime #datetime para manejar fechas
import time
import gi
gi.require_version('Gtk', '4.0') #version de GTK necesaria >=
from gi.repository import Gtk, Gio, GObject, GLib #importar Gtk, Gio para manjear acciones GObject clase base de objetos GTK

#Modulo para internacionalizacion
import locale
from lang import gettext as _

# Obtener el formato de fecha según el locale
date_format_locale = locale.nl_langinfo(locale.D_FMT)

# Obtener el formato de fecha en una forma legible
def _get_date_format():
    # Mapeo de formatos de fecha de locale a algo más entendible para el usuario
    format_map = {
        '%Y': 'YYYY',  # Año completo
        '%y': 'YY',    # Año acortado
        '%m': 'MM',    # Mes
        '%d': 'DD'     # Día
    }
    
    # Reemplaza los placeholders por la representación entendible
    user_format = date_format_locale
    for k, v in format_map.items():
        user_format = user_format.replace(k, v)
    
    return user_format

# Revisar que la fecha esté en el formato correcto y convertirla al formato estándar
def _validate_and_convert_date(date_str:str):
    try:
        # Verificar que la fecha está en el formato del locale actual
        user_date = datetime.strptime(date_str, date_format_locale)
        
        # Convertir la fecha a YYYY-MM-DD para la base de datos
        db_date = user_date.strftime('%Y-%m-%d')
        
        return db_date
    except ValueError:
        raise ValueError(f"La fecha '{date_str}' no es válida según el formato {date_format_locale}")

# Convertir las fechas de la BD al formato local
def _date_to_local_format(date_str:str):
    # Convertir a objeto datetime
    date_dt = datetime.strptime(date_str, "%Y-%m-%d")

    # Formatear la fecha al formato local
    date_locale = date_dt.strftime(date_format_locale)

    # Devolver la fecha formateada
    return date_locale

# Formatear horas y minutos en un string
def _format_time(h:int, m:int) -> str:
        ntime = ""
        if h > 23 or m > 59:
            raise Exception(_("Argument is not a valid time"))
        if h<10: ntime = '0'
        ntime += str(h) + ':'
        if m < 10: ntime += '0'
        ntime += str(m)
        return ntime

def run(application_id: str, on_activate: Callable) -> None:  #crea y ejecuta una isntancia de Gtk.Application 
    #(estructura principal de aplicacion de GTK
    app = Gtk.Application(application_id=application_id) #application_id es un id unico para la aplicacion
    app.connect('activate', on_activate) #on_activate es funcion de callback q se ejcuta cuando la app de active
    #lo q se hace es conectar el evento activate (al activar app) con la funcion on_activate que se le pasa para iniciar la interfaz
    app.run() #

class GPatient(GObject.GObject): # clase objeto paciente que hereda de Objeto GTKsrc/locale/es/LC_MESSAGES/MedicalApp.mo
    def __init__(self, id: int, code: str, name: str, surname: str): #, starred: bool = False):
        super().__init__()
        self.id = id #id
        self.code = code  #codigo
        self.name = name  #nombre
        self.surname = surname  #apellido
        #self.starred = starred #paciente marcado como favorito

class GMedication(GObject.GObject):  # Clase objeto para la medicación
    def __init__(self, id: int = None, name: str = None, dosage: float = None, start_date: str = None, treatment_duration: int = None, patient_id: int = None):
        super().__init__()

        # Asignar los valores recibidos a los atributos de la clase
        self.id = id
        self.name = name
        self.dosage = dosage
        self.start_date = start_date
        self.treatment_duration = treatment_duration
        self.patient_id = patient_id

class GPosologie(GObject.GObject): #clase objeto para posologia
    def __init__(self, id: int, hour: int, minute: int, medication_id: int):
        super().__init__()

        #asginar los valores
        self.id = id
        self.hour = hour
        self.minute = minute
        self.medication_id = medication_id

class PatientViewHandler(Protocol): #Protocolo para manejar los eventos relacionados con la vista de pacientes; los metodos son:
    def on_patient_selected(self, id: int) -> None: pass  #selecionar un paciente
    #def on_patient_toggle_starred(self, id: int) -> None: pass  #marcar como favorito un paciente
    def on_load_page(self, idx: int) -> None: pass #cargar pagina paciente
    def on_load_next_page(self) -> None: pass #cargar siguiente pagina paciente
    def on_load_previous_page(self) -> None: pass #cargar pagina anterior cliente

class MedicationViewHandler(Protocol): #protocolo para manejar los eventos relacionados con la vista de medicamentos; los metodos son:
    #manejadores para la lista de recetas de un paciente
    def on_medication_selected(self, id: int, id_patient: int) -> None: pass

class PatientView:  #define la vista de los pacientes; es donde empieza a construirse la interfaz; tambien la vista del resto de la aplicacion
    def __init__(self): #estado inicial de la vista (interfaz) 
        self.handler = None #en principio ningun manejador
        self.data = Gio.ListStore(item_type=GPatient) # un ListStore () que almacena los pacientes
        self.medicationList = Gio.ListStore(item_type=GMedication) #un ListStore para almacenar los medicamentos que tiene asignados un determinado paciente
        self.PosologiesList = Gio.ListStore(item_type=GPosologie)
        self.spinner = Gtk.Spinner()
        self.current_pageMedication= 0 #pagina actual de medicamentos
        self.current_page = 0
        #info de lo q es liststore The GtkListStore object is a list model for use with a GtkTreeView widget. It implements the 
        #GtkTreeModel interface, and consequentialy, can use all of the methods available there. It also implements the 
        #GtkTreeSortable interface so it can be sorted by the view. Finally, it also implements the tree drag and drop interfaces
        #mas info en -> https://docs.gtk.org/gtk4/class.ListStore.html

    def on_activate(self, app: Gtk.Application) -> None: #se ejecuta cuando la aplicacion se inicia (recibe a si mismo objeto interfaz
        # y tambien recibe la aplicacion)
        self._build_ui(app) #manda construir la UI (userInterface)
        self.handler.init_list() #llama a handler para iniciar la lista de pacientes

    def set_handler(self, handler: PatientViewHandler) -> None: #para establecer el handler que manejara los eventos de la vista; 
        #problabemente el presentador al ser un patron ModelViewPresenter
        self.handler = handler

    def _build_ui(self, app: Gtk.Application) -> None: #constructor de la UI; construye la interfaz grafica de usuario; aqui es 
        #donde se define la ventana principal conectada a la accion de cierre (cierre de la ventana)
        self.window = win = Gtk.ApplicationWindow( 
            title=_("Medical Application"), hexpand=True) #window es win q es una ventana gtk con titulo lista pacientes
        app.add_window(win) #se añade la ventana a la aplicacion
        win.connect("destroy", lambda win: win.close()) #si se destruye la ventana se cierra

        # Header

        header = Gtk.HeaderBar(hexpand=True) # crea una barra de encabezado
        about_action = Gio.SimpleAction.new("about", None) #crea una accion para mostrar una informacion 'Acerca de '
        about_action.connect("activate", self._show_about) #si se activa q ejecute show_about
        win.add_action(about_action) #añade esta accion a la ventana

        # Create a new menu, containing that action #crear un menu 
        menu = Gio.Menu.new() #crea un menu 
        menu.append("About", "win.about") # añade about y la accion de la ventana (about) al menu; tendra etiqueta 'About' y si se le 
        #da; ejecutara la accion de la ventana llamada about

        #Spinner
        self.sbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.sbox.set_halign(Gtk.Align.END)  # Alinear a la derecha
        self.sbox.set_valign(Gtk.Align.END)    # Alinear al fondo
        # Añadir márgenes al spinner
        self.sbox.set_margin_top(20)
        self.sbox.set_margin_bottom(20)
        self.sbox.set_margin_start(20)
        self.sbox.set_margin_end(20)

        # Ajustar el tamaño de la caja del spinner (no del spinner en sí)
        self.sbox.set_size_request(100, 100)  # Ancho, Alto ; tamaño minimo de la caja donde va el spinner
        #ajustar tamaño spinner
        self.spinner.set_size_request(30,30)
        # Agregar el spinner a la caja
        self.sbox.append(self.spinner)
        #añadimos la caja del spinner a la caja principal; main_box (hecho abajo linea -> 427)
        #tener la caja del spinner desactivada al principio
        self.set_sensitive_spinnerBox(False)

        # Create a popover, que es un menu desplegable flotante
        popover = Gtk.PopoverMenu()  # Create a new popover menu
        popover.set_menu_model(menu) #el menu creado antes se conecta como popover asi el menu anterior pasa a ser un menu flotante 
        #despegable; por tanto las opciones dentro del menu en este caso about se mostraran dentro del popoveri

        # Create a menu button # crea un boton de menu; le llama estilo hamburguesa (el que tiene 3 rayas q se suele usar de ajustes 
        #etc) porque es el q luego con el set_icon_name le va a dar esa forma; es un boton de menu y le llama hamburguer por la forma
        #que le va a dar (una estandar en interfaces graficas que tiene ese nombre; no hay q darle mas vuelta)
        hamburger = Gtk.MenuButton() #hamburguer es el boton menu
        hamburger.set_popover(popover) #el popover se pone al hamburger por tanto este boton servira para mostrar el popover
        hamburger.set_icon_name("open-menu-symbolic")  # establece el icono del boton, en este caso uno estandar q se suele usar
    
        header.pack_end(hamburger) #coloca el boton al final de la cabecera (header) (al final es a la derecha) (cabecera-> arriba)

        win.set_titlebar(header) #esta linea es para decirle a gtk q establezca una barra de encabezado para la ventana win 
        #personalizada; por eso le pasa header; porque quiere q la barra de encabezado q use sea esa para la ventana

        # Content
        # Listbox
        
        # Function to create each row from a list item; crea una lista de pacientes y define como se muestra cada fila
        def on_create_row(item: GPatient, user_data: Any) -> Gtk.Widget: #funcion q crea un widget fila para cada paciente (Gpatient)
            #en la lista; item es un paciente de la lista con sus datos (id, code, etc..); user_data es cualquier dato adicional pasado
            # a la funcion y fijarse q es Any por tanto no se usa en este caso
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                          margin_start=4, margin_end=4, margin_top=10, margin_bottom=10) # crea una caja (contenedor) GTK oriencation
            #horizontal con esos margenes q salen; al ser horinzontal los elementos se añadiran uno detras de otro; ej E1 E2 E3..
            #los margenees es para separar los elementos entre ellos y al principio y final de la caja
            box.append(Gtk.Label(label=item.code,
                       hexpand=True, halign=Gtk.Align.CENTER)) # añade a la caja (contenedor) una etiqueta con el code del paciente 
            #hexpand a True para que la etiqueta ocupe todo el espacio posible horizontalmente
            #if item.starred: #si el paciente esta marcado como favorito
            #    button = Gtk.Button.new_from_icon_name("starred-symbolic") #si paciente favorito; se muestra un icono estrella marcada
            #else:
            #    button = Gtk.Button.new_from_icon_name("non-starred-symbolic") #no -> se muestra boton forma icono estrella desmarcado
            #button.connect(
            #    "clicked", lambda _: self.handler.on_patient_toggle_starred(item.id)) # conecta/enlaza una señal 'clicked' a el boton 
            #con q si el boton es clickado active la funcion lambda que alterna el estado de la estella del paciente
            #self.handler... es un metodo del controlador handler (abstracto q en nuestro caso sera el Presenter; se pone abstracto 
            #para poder independizar el codigo view de lo demas y poder poner por ej controlador y no presenter) que le pasa como
            #parametro el id del item; en este caso el paciente
            #button.set_has_frame(False) #indica a gtk con False para decir que el boton (con forma de estrella) no le ponga un marco;
            #asi el boton se muestra solo y no con un marco/borde (queda mejor esteticamente)
            #box.append(button) # el boton se añade a la caja creada antes que tiene como etiqueta el codigo del paciente
            return box #devuelve la caja creada


        def on_create_rowMedicationList(item: GMedication, user_data: Any) -> Gtk.Widget: #funcion q crea un widget fila por medicamento(GMedication)
            # a la funcion y fijarse q es Any por tanto no se usa en este caso
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                          margin_start=1, margin_end=1, margin_top=4, margin_bottom=2, hexpand=True) # crea una caja (contenedor) GTK oriencation
            #horizontal con esos margenes q salen; al ser horinzontal los elementos se añadiran uno detras de otro; ej E1 E2 E3..
            #los margenees es para separar los elementos entre ellos y al principio y final de la caja
            box.append(Gtk.Label(label=item.name, hexpand=True, vexpand=True, halign=Gtk.Align.START)) # añade a la caja (contenedor) una etiqueta con el nombre del paciente
            #hexpand a True para que la etiqueta ocupe todo el espacio posible horizontalmente
            return box #devuelve la caja creada

        #funcion para crear fila posologia de la lista de posologias
        def on_create_rowPosologieList(item: GPosologie, user_data: Any) -> Gtk.Widget: #funcion q crea un widget fila por medicamento(GMedication)
            # a la funcion y fijarse q es Any por tanto no se usa en este caso
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                          margin_start=1, margin_end=1, margin_top=1, margin_bottom=1, hexpand=True) # crea una caja (contenedor) GTK oriencation
            #horizontal con esos margenes q salen; al ser horinzontal los elementos se añadiran uno detras de otro; ej E1 E2 E3..
            #los margenees es para separar los elementos entre ellos y al principio y final de la caja
            #box.append(Gtk.Label(label=item.hour, hexpand=True, vexpand=True, halign=Gtk.Align.CENTER, margin_top=8)) # añade a la caja (contenedor) una etiqueta con el nombre del paciente
            #hexpand a True para que la etiqueta ocupe todo el espacio posible horizontalmente
            #box.append(Gtk.Label(label=" : ", hexpand=True, vexpand=True, halign=Gtk.Align.CENTER, margin_top=8))
            #box.append(Gtk.Label(label=item.minute, hexpand=True, vexpand=True, halign=Gtk.Align.CENTER, margin_top=8))

            #añade un label con el tiempo bien formateado
            box.append(Gtk.Label(label=_format_time(item.hour, item.minute), hexpand=True, vexpand=True, halign=Gtk.Align.CENTER, margin_top=8))
            return box #devuelve la caja creada

        self.listbox = Gtk.ListBox(hexpand=True, vexpand=True) #se crea una Gtk.listBox (un widget de GTK q muestra elementos en una
        #lista); se indica q ocupe todo el espacio disponible horizontalmente y verticalmente
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE) # indica que en la lista que el modo seleccion sea SINGLE que 
        #significa que solo puede ser seleccionado una fila por cada vez; solo se pude selecionar una fila a la vez
        # Each time a item is inserted in or removed from self.data, on_create_row is executed
        self.listbox.bind_model(self.data, on_create_row, None)  #vincula el modelo de datos self.date (q a su vez es un Gio.ListStore
        # que tenia los pacientes ) con la funcion on_create_row (la de crear una caja por item pasado a la funcion) esto se hace para
        #que cada vez que se inserte o elimine un paciente en self.data, GTK llame a on_create_row (la funcion ) y le pase el item
        #en este caso el paciente para que cree una nueva fila con el.
        self.listbox.connect("row-activated", lambda _,
                             row: self.handler.on_patient_selected(self.data[row.get_index()].id))
        #conecta la lista creada con la señal row-activated que indica que cuando una fila sea clickada (activada) se ejecute 
        #el metodo on_patient_selected del manejador, al cual se le pasa el id del paciente que esta en esa columna
        #ejecuta el manejador de eventos de paciente selecionado
       
        # Enable scroll in the ListBox
        scrolledwindow = Gtk.ScrolledWindow() #crea un objeto tipo ScrolledWindow de GTK; que es UNA VENTANA CON DESPLAZAMIENTO (SCROL)
        scrolledwindow.set_size_request(150,90) #tamaño minimo de la lista scroll de los codigos de paciente
        #esta ventana envuelve la lista de pacientes (por tanto la lista de pacientes es hijo de esta ventana con scroll) el scroll
        #sera solo si la lista es mas larga q la ventana claro
        scrolledwindow.set_child(self.listbox) #marca como hijo del objeto scroll la lista de pacientes para que se pueda hacer scroll
        
        #botones siguiente y anterior; son botones de paginacion para navegar para adelante y para atras en las paginas de pacientes

        # Next/previous buttons
        self.next_button = Gtk.Button.new_from_icon_name("go-next-symbolic") #crea un boton GTK con el icono siguiente
        self.next_button.connect("clicked", lambda _: self.handler.on_load_page(self.current_page+1)) #enlaza la señal clickar con
        #el boton y si es clickado llama al manejador de eventos con la funcion on_load_page y le pasa la actual pagina +1
        #la funcion internamente hara que se avance a la siguiente pagina
        self.page_label = Gtk.Label(label=f"{self.current_page + 1}", margin_start=8, margin_end=8) #crea una etiqueta que muestra el
        #numero de pagina actual y ajusta sus margenes horizontales para que se vean bien
        self.prev_button = Gtk.Button.new_from_icon_name(
            "go-previous-symbolic") # crea un boton con el icono anterior
        self.prev_button.connect("clicked", lambda _: self.handler.on_load_page(self.current_page-1)) #lo mismo para siguiente pero 
        #ahora anterior
        self.prev_button.set_sensitive(False) # pone en el boton anterior a False el set_sensitive para que inicialmente el boton este
        #desactivado ya que al iniciar la aplicacion el user estara en la primera pagina y por tanto el boton por defecto al prinicipio
        #estara desactivado; ya nos escargaremos mas adelante (al pasar de pagina siguiente) de activar este boton

        #creacion de una caja para los botonex next y prev
        button_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER, homogeneous=False, margin_bottom=10, margin_top=14) # crea una caja para el boton anterior
        #horizontal;caja de botones alineada al centro y lo de homogeneous=False es para permitir que los elementos dentro de la caja
        #no tengan el mismo tamaño
        #se añaden a la caja el boton next y prev; tambien la etiqueta q indicaba el numero de pagina en la lista de clientes
        button_box.append(self.prev_button)
        button_box.append(self.page_label)
        button_box.append(self.next_button)
            
        #lista de medicamentos
        self.listboxMedication = Gtk.ListBox(hexpand=True, vexpand=False) #creo el listbox de medicamentos
        #self.listboxMedication.set_size_request(300,-1) #para que ocupe como minimo de ancho 30 pixeles; recibe como parametros (ancho,alto) en pixeles o un -1 en uno de ellos para que no lo tenga en cuenta (desactivado)
        #no hace falta ya que se ajusta automaticamente con el de q ocupe el maximo espacio posible
        self.listboxMedication.set_selection_mode(Gtk.SelectionMode.SINGLE) #solo se puede selecionar un medicamento a la vez
        self.listboxMedication.bind_model(self.medicationList, on_create_rowMedicationList, None) # lo vinculo con el modelo de datos y con on_create_row para que se actualize al añadir/eliminar medicamento
        self.listboxMedication.connect("row-activated", lambda _,
                                                     row: self.handler.on_medication_selected(
            self.medicationList[row.get_index()].id, self.medicationList[row.get_index()].patient_id)) #si se clicka en el medicamento

        #OJO; hay q poner aqui tambien el hexpand y vexpand ya q al ser la padre de la q vamos a meter dentro si no aunque la hija tenga esas propiedas activadas; si esta no las tiene NO FUNCIONA
        #MANDA MAS LA PADRE Q LA HIJA
        scrolledwindowMedicationList = Gtk.ScrolledWindow(vexpand=False, hexpand=True) #para que la lista de medicamentos tenga scroll
        scrolledwindowMedicationList.set_size_request(350, 245) #Ajustar el ancho y alto minimo
        scrolledwindowMedicationList.set_child(self.listboxMedication) #hago q la lista de medicamentos ea su hijo para q tenga scroll
        # queda mejor que la lista de medicamentos no tenga scroll ya q era scroll horizontal; pero que si lo tenga por si el nombre del medicamento fuera muy largo y estuviera ya a tope
        scrolledwindowMedicationList.set_margin_top(14) #añadir separacion con la label List of Medication

        self.listboxPosologies = Gtk.ListBox(hexpand=True, vexpand=True)
        self.listboxPosologies.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listboxPosologies.bind_model(self.PosologiesList, on_create_rowPosologieList, None)
        self.listboxPosologies.connect("row-activated", lambda _,row: self.handler.on_posologie_selected(self.get_selected_patient_id(),self.PosologiesList[row.get_index()].id, self.PosologiesList[row.get_index()].medication_id))
        self.listboxPosologies.set_size_request(50,125)
        scrolledwindowPosologieList = Gtk.ScrolledWindow(vexpand=False, hexpand=True)
        scrolledwindowPosologieList.set_size_request(50, 125)
        scrolledwindowPosologieList.set_child(self.listboxPosologies)
        scrolledwindowPosologieList.set_margin_top(10)

        # la caja vertical servira para contener la lista de pacientes y la caja de botones next/prev
        left_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, homogeneous=False, vexpand=True, hexpand=False) #crea una caja con orientacion vertical
        #homogeneous=False permite q elementos dentro de la caja puedan tener distintos tamaños; vexpand a true para que ocupe el 
        #maximo espacio vertical posible y el spacing es para que establezca un espaciado de 16 pixeles entre los widgets de dentro
        #de la caja
        left_box.append(scrolledwindow) # a la caja le mete la ventana con scroll (la q tiene lista de pacientes)
        left_box.append(button_box) #tambien añadimos la caja de botones next/prev


        #ahora en otra caja voy a crear otra lista con scroll para la lista de medicamentos debajo del formulario de pacientes

        #Configuracion de un formulario basico para ver y editar la informacion de los pacientes
        # Basic form
        form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, halign=Gtk.Align.START,
                           homogeneous=False, vexpand=True, hexpand=False, margin_start=16, margin_end=16) # crea una caja con orientacion vertical;
        #alineaada al principio (fijarse q pone principio por la internacionalizacion; no es izqd es izqd si es español e ira a la
        #derecha en arabe); demas valores ya vistos antes
        title_label = Gtk.Label(
            label=_("Selected patient"), halign=Gtk.Align.START, margin_top=14) #etiqueta
        title_label.add_css_class("title-2") #le añade un CSS a la etiqueta; con el CSS podemos aplicar estilos, distintos tipos de 
        #fuente, tamaño, color etc
        form_box.append(title_label) #añade a la caja la etiqueta, etiqueta titulo
        form_box.append(
            Gtk.Label(label=_("Code"), halign=Gtk.Align.START, margin_top=12)) #añada a la caja otra etiqueta, etiqueta code
        self.code_entry = Gtk.Entry() #crea un campo de entrada de texo en este caso para el code
        self.code_entry.set_margin_top(8)
        #para que no deje escribir en el code entry desactivamos la entrada
        self.set_sensitive_entry(self.code_entry, False)
        form_box.append(self.code_entry) #añade la entrada de texto a la caja
        form_box.append(
            Gtk.Label(label=_("Name"), halign=Gtk.Align.START, margin_top=12)) #añade a la caja otra etiqueta, etiqueta nombre
        self.name_entry = Gtk.Entry() #entrada de texto para el nombre
        self.name_entry.set_margin_top(8)
        self.set_sensitive_entry(self.name_entry, False)
        form_box.append(self.name_entry) #añade a la caja la entrada de texto
        form_box.append(Gtk.Label(label=_("Surname"),
                        halign=Gtk.Align.START, margin_top=12)) #etiqueta para apellido
        self.surname_entry = Gtk.Entry() #entrada texto para apellido
        self.surname_entry.set_margin_top(8)
        self.set_sensitive_entry(self.surname_entry, False)
        form_box.append(self.surname_entry) #mete en la caja la entrada de texto para el apellido
        #añado una etiquepa para la lista de medicamentos de ese paciente
        listOfMedication_label = Gtk.Label(label=_("List of Medications"), halign=Gtk.Align.START, margin_top=16)
        listOfMedication_label.add_css_class("title-4")
        form_box.append(listOfMedication_label)

        #añado a la caja la lista de pacientes
        form_box.append(scrolledwindowMedicationList) #la lista con scroll cuyo hija es la lista de medicamentos

        #añadimos dos botones; uno para añadir medicamentos y otro para eliminar medicamentos que tendran que estar
        #desacctivados si no hay selecionado un paciente claro
        self.anadirMedicamentoButton = Gtk.Button(label=_("Add Medication"))
        self.eliminarMedicamentoButton = Gtk.Button(label=_("Delete Medication"))
        self.eliminarMedicamentoButton.get_style_context().add_class("destructite-action") #tenga css destructivo
        self.anadirMedicamentoButton.set_sensitive(False) #el boton por defecto desactivado
        self.eliminarMedicamentoButton.set_sensitive(False) #el boton por defecto desactivado

        #conectamos ambos botones con la señal click con 2 eventos
        self.anadirMedicamentoButton.connect("clicked", lambda _: self.on_activate_addMedication()) #se le pasa el id del paciente
        self.eliminarMedicamentoButton.connect("clicked", lambda _: self.delete_window_confirm(self.get_selected_patient_id(), self.get_selected_medication_id())) #se le pasa el id del paciente y de la medicacion
        self.eliminarMedicamentoButton.get_style_context().add_class("destructive-action")

        #caja para contener los botones de añadir y borrar medicamentos
        self.boxButtonsMedication = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6, margin_top=14, margin_bottom=10, halign=Gtk.Align.CENTER)
        self.boxButtonsMedication.append(self.eliminarMedicamentoButton)
        self.boxButtonsMedication.append(self.anadirMedicamentoButton)
        form_box.append(self.boxButtonsMedication) #metemos la caja de botones en la caja del formulario

        # Crear la caja para el formulario de medicamentos donde se muestra el medicamento y la opcion para editarlo
        self.medication_form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=False, hexpand=False, halign=Gtk.Align.START, margin_end=16)
        tituloMedicationBox = Gtk.Label(label=_("Selected Medication"), halign=Gtk.Align.START, margin_top=14)
        tituloMedicationBox.add_css_class("title-2")
        self.medication_form_box.append(tituloMedicationBox)
        self.medication_form_box.append(Gtk.Label(label=_("Medication Name") + " (*)", halign=Gtk.Align.START, margin_top=12))
        self.medication_name_entry = Gtk.Entry()  # Entrada para el nombre del medicamento
        self.medication_name_entry.set_margin_top(8) #añadir separacion
        self.medication_name_entry.connect("changed", lambda widget: self.remove_entry_error(widget)) #conecta que si se clicka en ella se quite el estilo css de erroneo
        self.medication_form_box.append(self.medication_name_entry)
        self.medication_form_box.append(Gtk.Label(label=_("Dosage"), halign=Gtk.Align.START, margin_top=12))
        self.medication_dosage_entry = Gtk.Entry()  # Entrada para la dosis del medicamento
        self.medication_dosage_entry.connect("changed", lambda widget: self.remove_entry_error(widget))
        self.medication_dosage_entry.set_margin_top(8)
        self.medication_form_box.append(self.medication_dosage_entry)
        self.medication_form_box.append(Gtk.Label(label=_("Start Date Treatment") + " ("+_get_date_format()+") " + "(*)", halign=Gtk.Align.START, margin_top=12))
        self.medication_start_date_treatment_entry = Gtk.Entry()  # Entrada para la fecha inicio tratamiento del medicamento
        self.medication_start_date_treatment_entry.connect("changed", lambda widget: self.remove_entry_error(widget))
        self.medication_start_date_treatment_entry.set_margin_top(8)
        self.medication_form_box.append(self.medication_start_date_treatment_entry)
        self.medication_form_box.append(
            Gtk.Label(label=_("Treatment Duration (days)"), halign=Gtk.Align.START, margin_top=12))
        self.medication_treatment_duration_entry = Gtk.Entry()  # Entrada para la duracion  del medicamento
        self.medication_treatment_duration_entry.connect("changed", lambda widget: self.remove_entry_error(widget))
        self.medication_treatment_duration_entry.set_margin_top(8)
        self.medication_form_box.append(self.medication_treatment_duration_entry)

        #boton para guardar cambios
        self.guardarCambiosMedicamentoButton = Gtk.Button(label=_("Save Changes")) #boton para guardar cambios
        self.guardarCambiosMedicamentoButton.set_margin_top(20)# con una separacion de la anterior etqiueta
        self.guardarCambiosMedicamentoButton.connect("clicked", lambda _: self.guardarCambiosMedicamento()) #se le pasa el propio self
        #la funcion lambda anterior es para no modificar la funcion de gaurdar cambios y que me ignore el seguno parametro q connect le pasa a la funcion ya q
        #connect le pasa (self (interfaz) y button ) el propio boton; lo de lambda x: siendo x el argumento q lambda no permite pasarle a la funcion ; podemos usar _ para usarlo como comodin (como se hacia en el Ocaml)
        self.medication_form_box.append(self.guardarCambiosMedicamentoButton)
        
        #Lista de posologias
        listOfPosologies_label = Gtk.Label(label=_("List of Posologies"), halign=Gtk.Align.START, margin_top=14)
        listOfPosologies_label.add_css_class("title-4")
        self.medication_form_box.append(listOfPosologies_label)
        self.medication_form_box.append(scrolledwindowPosologieList) #añadir la lista de posologias
        self.posologiaDeleteButton = Gtk.Button(label=_("Delete Posologie"))
        #self.posologiaDeleteButton.set_margin_top(20)
        self.posologiaDeleteButton.get_style_context().add_class("destructive-action")
        self.set_sensitive_eliminar_posologiaButton(False) #hasta que no se selecione una posologia
        self.posologiaDeleteButton.connect("clicked", lambda _: self.eliminarPosologia())
        self.posologiaAddButton = Gtk.Button(label=_("Add Posologie"))
        #self.posologiaAddButton.set_margin_top(20)
        self.set_sensitive_anadir_posologiaButton(True) #activado
        self.posologiaAddButton.connect("clicked", lambda _: self.on_activate_addPosologia())

        #caja para contener los botones de añadir y borrar posologias
        self.boxButtonsPosologias = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6, margin_top=14, margin_bottom=10, halign=Gtk.Align.CENTER)
        self.boxButtonsPosologias.append(self.posologiaDeleteButton)
        self.boxButtonsPosologias.append(self.posologiaAddButton)
        self.medication_form_box.append(self.boxButtonsPosologias)  # añadir caja botones al formulario del medicamento

        # Al inicio, oculta la caja del formulario de medicamento
        self.medication_form_box.set_visible(False)

        self.medicationAddBox = self.medication_anadirWindow() #funcion para crear la vetana la caja con los componentes del formulario para añadir medicamentos
        # Al inicio, oculta la caja del formulario de medicamento
        self.set_sensitive_MedicationAddBox(False)
        #Pantalla posologias
        self.medicationPosologieBox = self.medicationPosologie_getWindow() #obtener ventana posologias de un medicamento
        self.set_sensitive_MedicationPosologieBox(False) #al principio la caja de la posologia de un medicamento esta desactivada
        self.addPosologieBox = self.addPosologie_getWindow() #ventana de añadir posologias
        self.set_sensitive_AddPosologieBox(False)
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        #main_box = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL, margin_start=8, margin_top=8, margin_end=8, margin_bottom=8) # crea un Contenedor Principal (Panel Dividido)
        #Crea un Panel Dividio (Gtk.Paned) llamado main_box que usara para organizar las cajas antes creadas tanto la q contiene la
        #lista de pacientes con los botones next/prev como la caja que contiene las etiquetas codigo, nombre y apellido de cada 
        #paciente con sus entradas de texto correspondientes; la horietacion es horinzontal por tanto; sus hijos se organizaran uno
        #detras de otro; asi de ej Hijo1 Hijo2

        #el problema de que main_box sea un paned es q solo son 2 diviido a la mitad y yo quiero mas
        #main_box.set_start_child(left_box) #añade la caja izqd como hijo (lista de pacientes y botonex next/prev
        main_box.append(left_box)
        #start child es que sera el primer hijo (en español a la izqd)
        #main_box.set_end_child(form_box) #añade la caja formulario (campos entrada de texto y etiquetas correspondientes a cada
        main_box.append(form_box)
        #campo del tipo de dato de cada paciente
        #añado la caja formulario de medicamento oculta en un principio al final del todo
        main_box.append(self.medication_form_box)  # Añades el formulario de medicamentos al final
        #end child hace que sea el ultimo hijo (en español a la derecha (final))
        main_box.append(self.medicationAddBox) #se añade el formulario de añadir medicamento al final
        main_box.append(self.medicationPosologieBox) #añadir formulario con info de la posologia
        main_box.append(self.addPosologieBox) #añadir ventana de añadir posologia a la caja principal
        main_box.append(self.sbox) #añadir la caja del spinner
        win.set_child(main_box) #hace que la caja esta sea hijo de la ventana principal

        win.present() # presentar la ventana es hacer que se muestre en pantalla; el usuario ya puede andar con ella

        #define la funcion de informacion sobre la aplicacion; el about
        #el Acerca De tipico

    def _show_about(self, action: Gio.SimpleAction, param: Any) -> None: #self (instancia actual) action (un objetipo tipo Gio.sim..
        #que sera un manejador de acciones de GTK, param en este caso no es usado (puede ser de cualquier tipo usado normalmente para
        #pasar datos adicionales a la funcion)

        about = Gtk.AboutDialog() #crea un cuadro de dialogo Acerca de llamado about; se usa para mostrar informacion sobre la 
        #aplicacion
        # Makes the dialog always appear in from of the parent window
        about.set_transient_for(self.window) # establece que el cuadro de acerca de sea temporal respecto a la ventana principal
        #, es decir, el cuadro dialogo se mostrara delante de la ventana principal (una ventana extra)
        
        # Makes the parent window unresponsive while dialog is showing
        about.set_modal(self.window) #no se puede interactuar con la ventana principal hasta que se cierre esta ventana dialogo

        about.set_program_name("Medication APP") # establece el nombre del programa
        about.set_authors(["Juan Vázquez", "Adrián Edreira", "Samuel Varela"])#establece los autores del programa [autor1] [autor2]...
        about.set_copyright("Copyright 2024 Group ZZTOP") #establece el copyright
        about.set_license_type(Gtk.License.GPL_3_0) # establece el tipo de licencia
        about.set_website("https://github.com/GEI-IPM-614G010222425/ipm-2425-p_escritorio-zz-top") #la pagina web
        about.set_website_label("Github") # la etiqueta de la pagina web de tal forma que; Etiqueta y al pulsar sobre ella te lleva 
        #al link q esta en el website
        about.set_version("1.0") # la version
        # The icon will need to be added to appropriate location
        about.set_logo_icon_name("org.gtk.Demo4") # el logo del icono que sale en el acerca de
        # E.g. /usr/share/icons/hicolor/scalable/apps/org.gtk.Demo4.svg # indica el ej de ruta donde puede ser almacenado el icono
        #donde encontrara la aplicacion el icono

        about.set_visible(True) # hace que sea visible el cuadro de dialogo acerca de 

    def get_current_page(self) -> int: #metodo para obtener la pagina actual
        return self.current_page

    def set_current_page(self, page: int) -> None: #metodo para establecer la pagina actual
        self.current_page = page
        #a parte de cambiar el valor; tambien hay q actualizar la vista
        self.page_label.set_text(f"{self.current_page + 1}") #actualiza la etiqueta donde pone la pagina actual
        if self.current_page == 0:
            self.set_sensitive_previous(False) # si la pagina actual es la primera, hay q desactivar el boton de ir a la anterior 
            #pagina

    def set_patients(self, patients: list) -> None: #metodo para añadir pacientes (todos de una)
        self.data.remove_all() #elimina todos los actuales
        for patient in patients: #para cada paciente de la lista de pacientes pasada como parametro
            self.data.append(GPatient(patient.id, patient.code,
                             patient.name, patient.surname)) #lo añade a la lista de pacientes guardados con sus respectivos campos

    #funcion para establecer la lista de medicamentos dada una lista de medicamentos
    def set_medications(self, medications: list) -> None:
        self.medicationList.remove_all() #elimina todos los medicamentos actuales
        for medication in medications:
            self.medicationList.append(GMedication(medication.id, medication.name,
                                    medication.dosage, medication.start_date, medication.treatment_duration, medication.patient_id))
        self.set_sensitive_eliminar_medicationButton(False)

    def set_posologies(self, posologias: list) -> None:
        self.PosologiesList.remove_all()  # elimina todos las posologias actuales
        for posologia in posologias:
            self.PosologiesList.append(GPosologie(posologia.id, posologia.hour, posologia.minute, posologia.medication_id))
            self.ordenarListboxPosologias() #ordenar posologias segun la hora
        self.set_sensitive_eliminar_posologiaButton(False)

    def set_patient(self, code: str, name: str, surname: str) -> None: #metodo para añadir un paciente desde la entrada de texto 
        #que hay junto en los campos de la informacion del paciente
        self.code_entry.get_buffer().set_text(code, -1) #llama al metodo get_buffer() que coje la info del campo de entrada code
        #y lo establece con set_text a la etiqueta code y el -1 es para que el texto se establezca hasta el final; remplazando
        #cualquier texto anterior
        self.name_entry.get_buffer().set_text(name, -1) #idem a lo anterior
        self.surname_entry.get_buffer().set_text(surname, -1) #idem a lo anterior

    def show_message(self, msg: str) -> None: #metodo para mostrar un mensaje que se pasa como parametro, un string
        dialog = Gtk.Window(
            title=_("Warning"), modal=True, resizable=False, transient_for=self.window) # abre una ventana nueva Gtk con el titulo
        #Warning, modal=True para que no se pueda interactuar con la ventana principal hasta que se cierre la nueva ventana abierta
        #resizable=False para que no pueda redimensionar esta nueva ventana de dialogo/advertencia
        #transient_for=self.windows hace que esta ventana de dialogo sea transintoria para 'self.window' es decir, se muestra sobre
        #la ventana principal (self.window)
        if len(msg) > 200:
            dialog.set_default_size(120,120) #si la longitud del mensaje es mayor a 200 establece la ventana de dialogo un tamaño 
            #mayor para que el mensaje se pueda leer bien (120*120 pixeles); ya que si es muy pequeña saldrian demasiados lineas

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16,
                      margin_top=24, margin_bottom=24, margin_start=48, margin_end=48) #creamos una caja con orientacion vertical 
        #con esos margenes
        box.append(Gtk.Label(label=msg, wrap=True)) # se añade a la caja una etiqueta que contiene el mensaje que queremos mostrar
        #y wrap es para permitir que el texto de la etiqueta se pueda ajustar a multiples lineas si es demasiado largo para caber
        #en una sola linea

        accept_button = Gtk.Button.new_with_label(_("Accept")) #se crea un boton de aceptar con esa etiqueta q ponga aceptar
        accept_button.connect("clicked", lambda _: dialog.close()) #se conecta la señal clickar del boton con la funcion de close 
        #de la vetana de dialogo para que cuando se pulse el boton aceptar; se cierre la ventana dialogo

        box.append(accept_button) #se añade el boton a la caja
        dialog.set_child(box) #se pone la caja como hija de la ventana de dialogo
        dialog.present() # se muestra por pantalla la vetana de dialogo y por tanto, el usuario ya puede interacturar con ella
    
    def delete_window_confirm(self, patient_id: int, medication_id: int) -> None: 
        #self.set_default_size(200, 100)
        dialog = Gtk.Window(
            title=_("Delete Medication"), modal=True, resizable=False, transient_for=self.window)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16,
                      margin_top=24, margin_bottom=24, margin_start=48, margin_end=48)

        box.append(Gtk.Label(label=_("Confirm medication deletion?"), wrap=True)) 

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8, halign=Gtk.Align.CENTER)
        
        
        # Botón de Cancelar
        accept_button = Gtk.Button(label=_("Cancel"))
        accept_button.connect("clicked", lambda _: dialog.close())  # Cerrar el diálogo
        
        # Botón de Eliminar
        delete_button = Gtk.Button(label=_("Delete"))
        delete_button.get_style_context().add_class("destructive-action")  # Clase de estilo para botón rojo
        delete_button.connect("clicked", lambda _: (self.handler.on_medication_eliminarButton(patient_id, medication_id), dialog.close()))  # Cerrar el diálogo
        button_box.append(delete_button)  # Añadir el botón de eliminar a la caja de botones

        button_box.append(accept_button)  # Añadir el botón de aceptar a la caja de botones

        box.append(button_box)

        dialog.set_child(box)  
        dialog.show()

    def set_sensitive_next(self, is_sensitive: bool) -> None: #metodo para establecer si el boton next esta o no habilitado
        self.next_button.set_sensitive(is_sensitive) #la funcion recibe un booleano que se la pasa para activar/desactivar el boton

    def set_sensitive_previous(self, is_sensitive: bool) -> None: #lo mismo que antes pero para boton anterior
        self.prev_button.set_sensitive(is_sensitive)

    def set_sensitive_eliminar_posologiaButton(self, is_sensitive: bool) -> None:
        self.posologiaDeleteButton.set_sensitive(is_sensitive)

    def set_sensitive_MedicationPosologieBox(self, is_sensitive: bool) -> None: #funcion para activar/desactivar la caja de la posologia de la medicacion
        self.medicationPosologieBox.set_visible(is_sensitive) #activar/desactivar la caja

    def set_sensitive_AddPosologieBox(self, is_sensitive: bool) ->None:
        self.addPosologieBox.set_visible(is_sensitive)

    def set_sensitive_anadir_posologiaButton(self, is_sensitive: bool) ->None:
        self.posologiaAddButton.set_sensitive(is_sensitive) #activar/desactivar boton añadir posologia

    def set_sensitive_save_posologiaButton(self, is_sensitive: bool) -> None:
        self.confirmarGuardarPosologiaButton.set_sensitive(is_sensitive)

    def set_sensitive_eliminar_medicationButton(self, is_sensitive: bool) -> None:
        self.eliminarMedicamentoButton.set_sensitive(is_sensitive)

    def set_sensitive_anadir_medicationButton(self, is_sensitive: bool) -> None:
        self.anadirMedicamentoButton.set_sensitive(is_sensitive)

    def set_sensitive_confirmar_anadir_medicationButton(self, is_sensitive: bool) -> None:
        self.confirmarAnadirMedicamentoButton.set_sensitive(is_sensitive)

    def set_sensitive_confirmar_anadir_posologiaButton(self, is_sensitive: bool) -> None:
        self.confirmarAnadirPosologiaButton.set_sensitive(is_sensitive)

    def set_sensitive_modificar_medicationButton(self, is_sensitive: bool) -> None:
        self.guardarCambiosMedicamentoButton.set_sensitive(is_sensitive)

    def set_sensitive_entry(self, entry: Gtk.Entry, is_sensitive: bool) -> None:
        #entry.set_editable(is_sensitive) #para que no se pueda modificar la entry
        entry.set_can_focus(is_sensitive) #para que no se pueda modificar la entry; es mejor que el anterior que le deja clickar (queda mejor)

    def set_sensitive_spinnerBox(self, is_sensitive: bool) ->None:
        self.sbox.set_sensitive(is_sensitive) #activar/desactivar caja spinner

    def set_sensitive_spinner(self, is_sensitive: bool) -> None:
        self.set_sensitive_spinnerBox(is_sensitive)
        if is_sensitive:
            self.spinner.start()
        else:
            self.spinner.stop()
        #funcion para activar/desactivar caja spinner y encender/parar spinner

    def desmarcarFilasListaPacientes(self) -> None:
        self.listbox.unselect_all() #desmarcar las filas escogidas de la lista de pacientes

    def desmarcarFilasListaMedicamentos(self) -> None:
        self.listboxMedication.unselect_all() #desmarcar las filas escogidas de la lista de medicamentos

    def desmarcarFilasListaPosologias(self) -> None:
        self.listboxPosologies.unselect_all() #desmarcar las filas escogidas de la lista de posologias

    #def toggle_starred(self, id: int) -> None: #este metodo alterna el estado 'favorito', la estrella, del paciente
    #    for idx in range(len(self.data)): #se le pasa el id del paciente y para cada id de paciente con los id de la lista de pacientes
    #        #guardada, si el id de coincide pues entonces
    #        if self.data[idx].id == id:
    #            updated_patient = GPatient(self.data[idx].id, self.data[idx].code, self.data[idx].name, self.data[idx].surname, 
    #                                       not self.data[idx].starred) # se actualiza ese paciente dandole el valor contrario al campo
    #            #de la estrella; de esta forma cuando se clicka sobre la estrella se activa esta funcion que al dar el valor contrario
    #            #al de favorito que tenia antes; vale tanto para activar como desactivar el favorito
    #            #el updated_pacient es un nuevo objeto paciente con los campos del paciente encontrado menos el de favorito q es el 
    #            #valor contraio al que tenia
    #            self.data.remove(idx) #elimina el paciente antiguo
    #            self.data.insert(idx, updated_patient) #añade el nuevo paciente en la posicion del paciente antiguo; por tanto, 
    #            #queda actualizado
    #            break #hace un break del bucle para no seguir recorriendolo ya que ya hemos encontrado el paciente buscado

    def cargar_datos_medicamento(self, medication: GMedication) -> None:
        self.medication_name_entry.set_text(medication.name) #rellenar los campos con los datos
        self.medication_dosage_entry.set_text(str(medication.dosage))
        self.medication_start_date_treatment_entry.set_text(_date_to_local_format(medication.start_date))
        self.medication_treatment_duration_entry.set_text(str(medication.treatment_duration))

        #hacer visible el boton de guardar cambios
        self.set_sensitive_modificar_medicationButton(True)
        # mandar señal al boton de eliminar medicamento para que se active
        self.set_sensitive_eliminar_medicationButton(True)
        #boton eliminar posologia po defecto desactivado
        self.set_sensitive_eliminar_posologiaButton(False)
        #mostrar los campos normal ; no en rojo; por si quedaron de antes
        self.remove_entry_error(self.medication_name_entry)
        self.remove_entry_error(self.medication_dosage_entry)
        self.remove_entry_error(self.medication_start_date_treatment_entry)
        self.remove_entry_error(self.medication_treatment_duration_entry)

        #la hacemos visible
        self.medication_form_box.set_visible(True)

    def cargar_datos_posologia(self,posologia: GPosologie) -> None:
        self.medication_posologie_form_hour_entry.set_text(str(posologia.hour))  # rellenar los campos con los datos
        self.medication_posologie_form_minute_entry.set_text(str(posologia.minute))

        # hacer visible el boton de guardar cambios
        self.set_sensitive_save_posologiaButton(True)
        # mandar señal al boton de eliminar posologia para que se active
        self.set_sensitive_eliminar_posologiaButton(True)
        # mostrar los campos normal ; no en rojo; por si quedaron de antes
        self.remove_entry_error(self.medication_posologie_form_hour_entry)
        self.remove_entry_error(self.medication_posologie_form_minute_entry)

        # la hacemos visible
        self.set_sensitive_MedicationPosologieBox(True)

    def set_sensitive_MedicationInformationBox(self, state: bool) -> None:
        #para desactivar la caja de la informacion con la medicacion
        self.medication_form_box.set_visible(state)

    def set_sensitive_MedicationAddBox(self, state:bool) ->None:
        #desactivar la caja de añadir medicacion
        self.medicationAddBox.set_visible(state)

    def get_selected_patient_id(self) ->int: #metodo para sacar el id del paciente selecionado en la lista de pacientes
        fila = self.listbox.get_selected_row()
        if fila:
            index = fila.get_index()
            return self.data[index].id
        else:
            return None

    def get_row_medication(self) -> int:
        fila = self.listboxMedication.get_selected_row() #obtener fila
        if fila:
            index = fila.get_index() #obtener el indice
            return index
        else:
            return None

    def get_row_posologia(self) -> int:
        fila = self.listboxPosologies.get_selected_row()  # obtener fila
        if fila:
            index = fila.get_index()  # obtener el indice
            return index
        else:
            return None

    def get_selected_medication_id(self) -> int:  # metodo para sacar el id del paciente selecionado en la lista de pacientes
        fila = self.listboxMedication.get_selected_row()
        if fila:
            index = fila.get_index()
            return self.medicationList[index].id
        else:
            return None

    def get_selected_posologie_id(self) -> int:
        fila = self.listboxPosologies.get_selected_row()
        if fila:
            index = fila.get_index()
            return self.PosologiesList[index].id
        else:
            return None

    def guardarCambiosMedicamento(self) -> None: #metodo para validar los datos y guardar los cambios del medicamento
        idMedication = self.get_selected_medication_id()
        idPaciente = self.get_selected_patient_id()
        if idMedication is None or idPaciente is None: #campos invalidos
            self.set_sensitive_modificar_medicationButton(False) # boton guardar cambios no activo
            self.mostrar_notificacion_temporal(self.guardarCambiosMedicamentoButton, _("ID patient/medication is null"))
            return None
        self.set_sensitive_modificar_medicationButton(True) #boton guardar cambios activo
        #validar si los campos estan vacios y si es asi y es opcional poner el valor por defecto y si no dar error
        medicationName = self.medication_name_entry.get_text() #obligatorio
        if not medicationName:
            self.set_entry_error(self.medication_name_entry)
            self.mostrar_notificacion_temporal(self.medication_name_entry, _("Medication 's name can not be empty"))
            return None
        dosage_text = self.medication_dosage_entry.get_text() or "1" #voluntario
        
        # Verificar y convertir el formato de la fecha
        start_date = self.medication_start_date_treatment_entry.get_text()
        try:
            start_date = _validate_and_convert_date(start_date)
        except ValueError:
            self.set_entry_error(self.medication_start_date_treatment_entry)
            self.mostrar_notificacion_temporal(self.medication_start_date_treatment_entry, _("Start Date format incorrect"))
            return None

        treatment_duration_text = self.medication_treatment_duration_entry.get_text() or "1"

        try:
            dosage = float(dosage_text)
        except ValueError as e:
            self.set_entry_error(self.medication_dosage_entry)
            self.mostrar_notificacion_temporal(self.medication_dosage_entry, _("Dosage must be a number"))
            return None
        try:
            treatment_duration = int(treatment_duration_text)
        except ValueError as e:
            self.set_entry_error(self.medication_treatment_duration_entry)
            self.mostrar_notificacion_temporal(self.medication_treatment_duration_entry, _("Treatment duration must be a number"))
            return None

        self.handler.guardarCambiosMedicamento(idMedication, medicationName, dosage, start_date, treatment_duration, idPaciente)


    def guardarCambiosPosologia(self) -> None:
        idMedication = self.get_selected_medication_id()
        idPaciente = self.get_selected_patient_id()
        idPosologia = self.get_selected_posologie_id()
        if idMedication is None or idPaciente is None or idPosologia is None:  # campos invalidos
            self.set_sensitive_save_posologiaButton(False)  # boton guardar cambios no activo
            self.mostrar_notificacion_temporal(self.confirmarGuardarPosologiaButton, _("ID patient/medication/posologie is null"))
            return None
        self.set_sensitive_save_posologiaButton(True)  # boton guardar cambios activo
        # validar si los campos estan vacios y si es asi y es opcional poner el valor por defecto y si no dar error
        hour_text = self.medication_posologie_form_hour_entry.get_text()  # obligatorio
        minute_text = self.medication_posologie_form_minute_entry.get_text()  # obligatorio
        if not hour_text:
            self.set_entry_error(self.medication_posologie_form_hour_entry)
            self.mostrar_notificacion_temporal(self.medication_posologie_form_hour_entry, _("Hour can not be empty"))
            return None
        if not minute_text:
            self.set_entry_error(self.medication_posologie_form_minute_entry)
            self.mostrar_notificacion_temporal(self.medication_posologie_form_minute_entry, _("Minute can not be empty"))
            return None

        try:
            hour = float(hour_text)
            if hour < 0 or hour > 23:
                self.set_entry_error(self.medication_posologie_form_hour_entry)
                self.mostrar_notificacion_temporal(self.medication_posologie_form_hour_entry, _("Hour must be a number between 0 and 23"))
                return None
        except ValueError as e:
            self.set_entry_error(self.medication_posologie_form_hour_entry)
            self.mostrar_notificacion_temporal(self.medication_posologie_form_hour_entry, _("Hour must be a number"))
            return None

        try:
            minute = float(minute_text)
            if minute < 0 or minute > 59:
                self.set_entry_error(self.medication_posologie_form_minute_entry)
                self.mostrar_notificacion_temporal(self.medication_posologie_form_minute_entry,
                                                   _("Minute must be a number between 0 and 59"))
                return None
        except ValueError as e:
            self.set_entry_error(self.medication_posologie_form_minute_entry)
            self.mostrar_notificacion_temporal(self.medication_posologie_form_minute_entry, _("Minute must be a number"))
            return None

        self.handler.guardarCambiosPosologia(idMedication,idPaciente, idPosologia, hour, minute)

    def medicationPosologie_getWindow(self) -> Gtk.Widget:  # obtener ventana posologias de un medicamento
        #formulario para ver las posologias y para modificarlas
        self.posologia_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=False, hexpand=False, halign=Gtk.Align.START, margin_end=16)
        titleBox = Gtk.Label(label=_("Posologie"), halign=Gtk.Align.START, margin_top = 14)
        titleBox.add_css_class("title-2")
        self.posologia_box.append(titleBox)
        self.posologia_box.append(Gtk.Label(label=_("Hour") + " " + "(*)", halign=Gtk.Align.START, margin_top=12))
        self.medication_posologie_form_hour_entry = Gtk.Entry()
        self.posologia_box.append(self.medication_posologie_form_hour_entry)
        self.posologia_box.append(Gtk.Label(label=_("Minute")+ " "+ "(*)", halign=Gtk.Align.START, margin_top=12))
        self.medication_posologie_form_minute_entry = Gtk.Entry()
        self.medication_posologie_form_hour_entry.connect("changed", lambda widget: self.remove_entry_error(widget))
        self.medication_posologie_form_minute_entry.connect("changed", lambda widget: self.remove_entry_error(widget))
        self.medication_posologie_form_hour_entry.set_margin_top(8)
        self.medication_posologie_form_minute_entry.set_margin_top(8)
        self.posologia_box.append(self.medication_posologie_form_minute_entry)

        # boton para confirmar y cancelar
        self.confirmarGuardarPosologiaButton = Gtk.Button(label=_("Save"))  # boton para guardar cambios
        self.confirmarGuardarPosologiaButton.set_margin_top(8)  # con una separacion vertical de la caja
        self.confirmarGuardarPosologiaButton.connect("clicked", lambda
            _: self.guardarCambiosPosologia())

        # crear una caja para poner los botones
        self.boxButtonsSavePosologie = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER,
                                               spacing=6,
                                               margin_top=8)  # caja para meter tanto el boton de añadir/eliminar posologia
        self.boxButtonsSavePosologie.append(self.confirmarGuardarPosologiaButton)

        # añadir caja botones al formulario añadir posologia caja
        self.posologia_box.append(
            self.boxButtonsSavePosologie)  # añadir caja de posologias al formulario caja
        # el desactivar la venrana se hace donde se deuelve la funcion y no ahora por q el objeto aunm no esta inicializado ya q la funcion se hace con el self.MedicationAddBox
        # devolver la caja
        return self.posologia_box

    def addPosologie_getWindow(self) -> Gtk.Widget:  # obtener ventana posologias de un medicamento
        #formulario para añadir una posologia
        self.add_posologia_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=False, hexpand=False, halign=Gtk.Align.START, margin_end=16)
        titleBox = Gtk.Label(label=_("Add Posologie"), halign=Gtk.Align.START, margin_top = 14)
        titleBox.add_css_class("title-2")
        self.add_posologia_box.append(titleBox)
        self.add_posologia_box.append(Gtk.Label(label=_("Hour")+" (*)", halign=Gtk.Align.START, margin_top=12))
        self.add_posologia_form_hour_entry = Gtk.Entry()
        self.add_posologia_box.append(self.add_posologia_form_hour_entry)
        self.add_posologia_box.append(Gtk.Label(label=_("Minute") +" (*)", halign=Gtk.Align.START, margin_top=12))
        self.add_posologia_form_minute_entry = Gtk.Entry()
        self.add_posologia_form_hour_entry.connect("changed", lambda widget: self.remove_entry_error(widget))
        self.add_posologia_form_minute_entry.connect("changed", lambda widget: self.remove_entry_error(widget))
        self.add_posologia_form_hour_entry.set_margin_top(8)
        self.add_posologia_form_minute_entry.set_margin_top(8)
        self.add_posologia_box.append(self.add_posologia_form_minute_entry)

        # boton para confirmar y cancelar
        self.confirmarAnadirPosologiaButton = Gtk.Button(label=_("Add"))  # boton para guardar cambios
        self.confirmarAnadirPosologiaButton.set_margin_top(8)  # con una separacion vertical de la caja
        self.confirmarAnadirPosologiaButton.connect("clicked", lambda
            _: self.on_activate_confirm_add_posologiaButton())
        self.cancelarAnadirPosologiaButton = Gtk.Button(label=_("Cancel"))
        self.cancelarAnadirPosologiaButton.set_margin_top(8)
        self.cancelarAnadirPosologiaButton.connect("clicked", lambda _: self.set_sensitive_AddPosologieBox(False)) #desactivar la caja de añadir posologia

        # crear una caja para poner los botones
        self.boxButtonsAddPosologia = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER,
                                               spacing=6,
                                               margin_top=8)  # caja para meter tanto el boton de añadir/eliminar posologia
        self.boxButtonsAddPosologia.append(self.confirmarAnadirPosologiaButton)
        self.boxButtonsAddPosologia.append(self.cancelarAnadirPosologiaButton)

        # añadir caja botones al formulario añadir posologia caja
        self.add_posologia_box.append(
            self.boxButtonsAddPosologia)  # añadir caja de posologias al formulario caja
        # el desactivar la venrana se hace donde se deuelve la funcion y no ahora por q el objeto aunm no esta inicializado ya q la funcion se hace con el self.MedicationAddBox
        # devolver la caja
        return self.add_posologia_box

    def medication_anadirWindow(self) -> Gtk.Widget: #metodo para cargar la ventana de añadir medicamento
        # formulario para añadir medicamento
        # Crear la caja para el formulario de deñadir medicamentos
        self.medication_Add_form_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=False, hexpand=False,
                                               halign=Gtk.Align.START, margin_end=16)
        tituloAnadirMedicamento = Gtk.Label(label=_("New Medication"), halign=Gtk.Align.START, margin_top = 14)
        tituloAnadirMedicamento.add_css_class("title-2") #para que salga en negrita y asi mas tamaño
        self.medication_Add_form_box.append(tituloAnadirMedicamento)
        self.medication_Add_form_box.append(Gtk.Label(label=_("Medication Name")+" (*)", halign=Gtk.Align.START, margin_top=12))
        self.medication_Add_name_entry = Gtk.Entry()  # Entrada para el nombre del medicamento

        self.medication_Add_name_entry.connect("changed", lambda widget: self.remove_entry_error(widget)) #conecta que si se clicka en ella se quite el estilo css de erroneo

        self.medication_Add_name_entry.set_margin_top(8)  # añadir separacion
        self.medication_Add_form_box.append(self.medication_Add_name_entry)
        self.medication_Add_form_box.append(Gtk.Label(label=_("Dosage"), halign=Gtk.Align.START, margin_top=12))
        self.medication_Add_dosage_entry = Gtk.Entry()  # Entrada para la dosis del medicamento
        self.medication_Add_dosage_entry.connect("changed", lambda widget: self.remove_entry_error(widget))

        self.medication_Add_dosage_entry.set_margin_top(8)
        self.medication_Add_form_box.append(self.medication_Add_dosage_entry)
        self.medication_Add_form_box.append(
            Gtk.Label(label=_("Start Date Treatment")+ " (" + _get_date_format() + ") " + "(*)", halign=Gtk.Align.START, margin_top=12))
        self.medication_Add_start_date_treatment_entry = Gtk.Entry()  # Entrada para las instrucciones del medicamento
        self.medication_Add_start_date_treatment_entry.connect("changed", lambda widget: self.remove_entry_error(widget))

        self.medication_Add_start_date_treatment_entry.set_margin_top(8)
        self.medication_Add_form_box.append(self.medication_Add_start_date_treatment_entry)
        self.medication_Add_form_box.append(
            Gtk.Label(label=_("Treatment Duration (days)"), halign=Gtk.Align.START, margin_top=12))
        self.medication_Add_treatment_duration_entry = Gtk.Entry()  # Entrada para las instrucciones del medicamento
        self.medication_Add_treatment_duration_entry.connect("changed", lambda widget: self.remove_entry_error(widget))

        self.medication_Add_treatment_duration_entry.set_margin_top(8)
        self.medication_Add_form_box.append(self.medication_Add_treatment_duration_entry)

        # boton para confirmar y cancelar
        self.confirmarAnadirMedicamentoButton = Gtk.Button(label=_("Confirm"))  # boton para guardar cambios
        self.confirmarAnadirMedicamentoButton.set_margin_top(8)  # con una separacion vertical de la caja
        self.cancelarAnadirMedicamentoButton = Gtk.Button(label=_("Cancel"))  # boton para guardar cambios
        self.cancelarAnadirMedicamentoButton.set_margin_top(8)  # con una separacion vertical de la caja
        
        self.confirmarAnadirMedicamentoButton.connect("clicked", lambda
            _: self.on_activate_confirm_add_medicationButton())
        
        self.cancelarAnadirMedicamentoButton.connect("clicked", lambda _: self.set_sensitive_MedicationAddBox(False)) #desactivas el formulario

        # crear una caja para poner los botones
        self.boxButtonsAddMedication = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER, spacing=12, margin_top=8)  # caja para meter tanto el boton de añadir medicamento como eliminar
        self.boxButtonsAddMedication.append(self.confirmarAnadirMedicamentoButton)
        self.boxButtonsAddMedication.append(self.cancelarAnadirMedicamentoButton)
        
        #añadir caja botones al formulario añadir medicamento caja
        self.medication_Add_form_box.append(self.boxButtonsAddMedication) #añadir caja de medicaciones al formulario caja
        #el desactivar la venrana se hace donde se deuelve la funcion y no ahora por q el objeto aunm no esta inicializado ya q la funcion se hace con el self.MedicationAddBox
        #devolver la caja
        return self.medication_Add_form_box

    def on_activate_addMedication(self):
        #primero vaciar todas las casillas, ponerlas vacias por si se quedo algo de otra vez de texto
        self.medication_Add_name_entry.set_text("")
        self.medication_Add_dosage_entry.set_text("")
        self.medication_Add_start_date_treatment_entry.set_text("")
        self.medication_Add_treatment_duration_entry.set_text("")

        #hay que mostrar la pantalla formulario de añadir medicamento con textos de ej
        self.medication_Add_name_entry.set_placeholder_text(_("Ex: Ibuprofeno Normon")) #se le añade un placeholder (texto fantasma o texto segerencia)
        self.medication_Add_dosage_entry.set_placeholder_text(_("Ex: 2, (default 1)"))
        self.medication_Add_start_date_treatment_entry.set_placeholder_text(_("Ex: ") + _get_date_format())
        self.medication_Add_treatment_duration_entry.set_placeholder_text(_("Ex: 10, (default 1)"))
        #cerrar ventana informacion medicamentos
        self.set_sensitive_MedicationInformationBox(False)
        #cerrar ventana informacion posologias
        self.set_sensitive_MedicationPosologieBox(False)
        self.set_sensitive_AddPosologieBox(False) #cerrar vetana añadir posologia
        #quitar la selecion de la lista de medicamentos de ese paciente
        self.desmarcarFilasListaMedicamentos() #desmarcas la lista de medicamentos (para que no se vea la fila del medicamento marcada)
        #quitar el boton de eliminar medicamento
        self.set_sensitive_eliminar_medicationButton(False)

        #mostrar los campos normal; no en rojo; por si quedaron de antes
        self.remove_entry_error(self.medication_Add_name_entry)
        self.remove_entry_error(self.medication_Add_dosage_entry)
        self.remove_entry_error(self.medication_Add_start_date_treatment_entry)
        self.remove_entry_error(self.medication_Add_treatment_duration_entry)

        #mostrar la ventana
        self.set_sensitive_MedicationAddBox(True)

    def on_activate_addPosologia(self) -> None:
        # primero vaciar todas las casillas, ponerlas vacias por si se quedo algo de otra vez de texto
        self.add_posologia_form_hour_entry.set_text("")
        self.add_posologia_form_minute_entry.set_text("")

        # hay que mostrar la pantalla formulario de añadir posologia con textos de ej
        self.add_posologia_form_hour_entry.set_placeholder_text(_("Ex: 17"))  # se le añade un placeholder (texto fantasma o texto segerencia
        self.add_posologia_form_minute_entry.set_placeholder_text(_("Ex: 54"))  # se le añade un placeholder (texto fantasma o texto segerencia
        # cerrar ventana informacion posologias
        self.set_sensitive_MedicationPosologieBox(False)
        # quitar la selecion de la lista de posologias de ese paciente
        self.desmarcarFilasListaPosologias()  # desmarcas la lista de posologias (para que no se vea la fila de la posologia marcada)
        # quitar el boton de eliminar posologias
        self.set_sensitive_eliminar_posologiaButton(False)

        # mostrar los campos normal; no en rojo; por si quedaron de antes
        self.remove_entry_error(self.add_posologia_form_minute_entry)
        self.remove_entry_error(self.add_posologia_form_hour_entry)
        # mostrar la ventana
        self.set_sensitive_AddPosologieBox(True)

    def on_activate_confirm_add_medicationButton(self):
        #recoger los campos
        idPaciente = self.get_selected_patient_id()
        if idPaciente is None:  # campos invalidos
            self.set_sensitive_confirmar_anadir_medicationButton(False)  # boton guardar cambios no activo
            self.mostrar_notificacion_temporal(self.confirmarAnadirMedicamentoButton, _("ID patient can not be null"))
            return None
        self.set_sensitive_confirmar_anadir_medicationButton(True)  # boton confirmar añadir medicamento nuevo activo
        # validar si los campos estan vacios y si es asi y es opcional poner el valor por defecto y si no dar error
        
        # Nombre
        medicationName = self.medication_Add_name_entry.get_text()  # obligatorio
        if not medicationName:
            self.set_entry_error(self.medication_Add_name_entry)
            self.mostrar_notificacion_temporal(self.medication_Add_name_entry, _("Medication 's name can not be empty")) #nombre de medicamento no puede ser vacio
            return None

        # Verificar el formato de la fecha y convertirla al estándar
        start_date = self.medication_Add_start_date_treatment_entry.get_text() #obligatorio
        try:
            start_date = _validate_and_convert_date(start_date)
        except ValueError:
            self.set_entry_error(self.medication_Add_start_date_treatment_entry)
            self.mostrar_notificacion_temporal(self.medication_Add_start_date_treatment_entry,_("Start Date format incorrect"))
            return None
        
        # Dosis
        dosage_text = self.medication_Add_dosage_entry.get_text() or "1"  # voluntario
        try:
            dosage = float(dosage_text)
        except ValueError as e:
            self.set_entry_error(self.medication_Add_dosage_entry)
            self.mostrar_notificacion_temporal(self.medication_Add_dosage_entry, _("Dosage must be a number"))
            return None
        
        # Duración del tratamiento
        treatment_duration_text = self.medication_Add_treatment_duration_entry.get_text() or "1"
        try:
            treatment_duration = int(treatment_duration_text)
        except ValueError as e:
            self.set_entry_error(self.medication_Add_treatment_duration_entry)
            self.mostrar_notificacion_temporal(self.medication_Add_treatment_duration_entry, _("Treatment duration must be a number or empty"))
            return None

        self.handler.on_medication_confirmAddButton(idPaciente, medicationName, dosage, start_date, treatment_duration)

    def on_activate_confirm_add_posologiaButton(self) ->None:
        # recoger los campos
        idPaciente = self.get_selected_patient_id()
        idMedication = self.get_selected_medication_id()
        if idPaciente is None or idMedication is None:  # campos invalidos
            self.set_sensitive_confirmar_anadir_posologiaButton(False)  # boton guardar cambios no activo
            self.mostrar_notificacion_temporal(self.confirmarAnadirPosologiaButton, _("ID patient/ ID medication can not be null"))
            return None
        self.set_sensitive_confirmar_anadir_posologiaButton(True)  # boton confirmar añadir posologia nuevo activo
        # validar si los campos estan vacios y si es asi y es opcional poner el valor por defecto y si no dar error
        hour_text = self.add_posologia_form_hour_entry.get_text()  # obligatorio
        minute_text = self.add_posologia_form_minute_entry.get_text()  # obligatorio
        if not hour_text:
            self.set_entry_error(self.add_posologia_form_hour_entry)
            self.mostrar_notificacion_temporal(self.add_posologia_form_hour_entry,
                                               _("Posologie's hour can not be empty"))
            return None
        if not minute_text:
            self.set_entry_error(self.add_posologia_form_minute_entry)
            self.mostrar_notificacion_temporal(self.add_posologia_form_minute_entry,
                                               _("Posologie's minute can not be empty"))
            return None

        try:
            hour = int(hour_text)
            if hour < 0 or hour >23:
                self.set_entry_error(self.add_posologia_form_hour_entry)
                self.mostrar_notificacion_temporal(self.add_posologia_form_hour_entry, _("Hour must be a number between 0 and 23"))
        except ValueError as e:
            self.set_entry_error(self.add_posologia_form_hour_entry)
            self.mostrar_notificacion_temporal(self.add_posologia_form_hour_entry, _("Hour must be a number"))
            return None

        try:
            minute = int(minute_text)
            if minute <0 or minute >59:
                self.set_entry_error(self.add_posologia_form_minute_entry)
                self.mostrar_notificacion_temporal(self.add_posologia_form_minute_entry, _("Minute must be a number between 0 and 59"))
        except ValueError as e:
            self.set_entry_error(self.add_posologia_form_minute_entry)
            self.mostrar_notificacion_temporal(self.add_posologia_form_minute_entry, _("Minute must be a number"))
            return None

        self.handler.on_posologia_confirmAddButton(idPaciente, idMedication, hour, minute)

    def modificarMedicamentoListaMedicamentos(self, medication) -> None:
        #metodo para modificar un medicamento de la lista de medicamentos
        #sacar el indice del medicamento selecionado (el q se va a modificar)
        indexMedicamento = self.get_row_medication()  # obtener el indice del medicamento para luego modificar el medicamento
        #primero hay q actualizar esa lista de medicamentos y luego la listBoxMedicamentos modificando el de la fila correspondiente su widget; modificar el widget
        #camiamos el medicamento en la medicationList para ello eliminamos la fila antigua y metemos la nueva
        self.medicationList.remove(indexMedicamento)
        #parseamos el medicamento a Gmedicamento
        medicamentoG = GMedication(medication.id, medication.name, medication.dosage, medication.start_date, medication.treatment_duration, medication.patient_id)
        self.medicationList.insert(indexMedicamento, medicamentoG)
        fila = self.listboxMedication.get_row_at_index(indexMedicamento)
        #ahora no hace falta actualizar la listbox, ya se hace solo
        #para que quede la fila selecionada como antes de modificar la selecionamos
        self.listboxMedication.select_row(fila) #selecionamos la fila
        #enviamos la señal row_activated como si un usuario hubeira clickado sobre ella
        #al recibir la señal va a quedar selecionada y tambien se va a cargar los datos del medicamento actualizados en este caso
        fila.activate()

    def modificarPosologiaListaPosologias(self, posologia) -> None:
        #metodo para modificar una posologia de la lista de posologias
        #sacar el indice de la posologia selecionado (el q se va a modificar)
        idPosologiaSelecionada = self.PosologiesList.get_item(self.get_row_posologia()).id  # obtener el indice de la posologia de la LISTA DE POSOLOGIAS (ya que si lo hago de la listbox al ordenarlas luego me fastiaida y me seleciona otra)
        indexPosologia = self.get_row_posologia() #sacar el indice

        #primero hay q actualizar esa lista de posologias y luego la listBoxPosologies modificando el de la fila correspondiente su widget; modificar el widget
        #camiamos el posologia en la PosologieList para ello eliminamos la fila antigua y metemos la nueva
        self.PosologiesList.remove(indexPosologia)
        #parseamos la posologia a Gposologie
        posologiaG = GPosologie(posologia.id, posologia.hour, posologia.minute, posologia.medication_id)
        self.PosologiesList.insert(indexPosologia, posologiaG)
        self.ordenarListboxPosologias() #ordenamos la lista de posologias

        #sacar el indice del elemento de la lista de posologias el e antes para ello habra que buscarlo
        new_index = next((i for i in range(self.PosologiesList.get_n_items()) if
                          self.PosologiesList.get_item(i).id == idPosologiaSelecionada), None)

        fila = self.listboxPosologies.get_row_at_index(new_index)
        #ahora no hace falta actualizar la listbox, ya se hace solo
        #para que quede la fila selecionada como antes de modificar la selecionamos
        self.listboxPosologies.select_row(fila) #selecionamos la fila
        #enviamos la señal row_activated como si un usuario hubeira clickado sobre ella
        #al recibir la señal va a quedar selecionada y tambien se va a cargar los datos del medicamento actualizados en este caso
        fila.activate()

    def cerrar_notificacion_temporal(self, popover: Gtk.Widget) -> bool:
        popover.hide()
        return False # para que el timeout se ejecute sola una vez

    def mostrar_notificacion_temporal(self, padre: Gtk.Widget, message: str) -> None:
        #crear el popover
        popover = Gtk.Popover.new() #se crea el popover
        # Asignar el widget padre al popover
        popover.set_parent(padre) #asociado al widget padre (sera normalmente para los botones que van a mandar feedback al user)
        label = Gtk.Label(label=message) #etiqueta con el mensaje q mostrara el popover
        popover.set_child(label) #añadimos la etiqueta al popover
        popover.show() #mostrar el popover
        # Establecer un timeout para que el popover se cierre automáticamente después de 2 segundos (200 ms)
        GLib.timeout_add(2000, self.cerrar_notificacion_temporal, popover)

    def set_entry_error(self, entry: Gtk.Entry) -> None: #metodo para poner una entrada con el css de error
        entry.get_style_context().add_class("error")

    def remove_entry_error(self, entry: Gtk.Entry) -> None:  # metodo para quitar una entrada con el css de error
        entry.get_style_context().remove_class("error")

    def eliminarPosologia(self) ->None:
        #eliminar posologia
        self.delete_posologie_window_confirm(self.get_selected_patient_id(), self.get_selected_medication_id(), self.get_selected_posologie_id())

    def delete_posologie_window_confirm(self, patient_id: int, medication_id: int, posologie_id) -> None:
        # self.set_default_size(200, 100)
        dialog = Gtk.Window(
            title=_("Delete Posologie"), modal=True, resizable=False, transient_for=self.window)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16,
                      margin_top=24, margin_bottom=24, margin_start=48, margin_end=48)

        box.append(Gtk.Label(label=_("Confirm posologie deletion?"), wrap=True))

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8, halign=Gtk.Align.CENTER)

        # Botón de Cancelar
        accept_button = Gtk.Button(label=_("Cancel"))
        accept_button.connect("clicked", lambda _: dialog.close())  # Cerrar el diálogo

        # Botón de Eliminar
        delete_button = Gtk.Button(label=_("Delete"))
        delete_button.get_style_context().add_class("destructive-action")  # Clase de estilo para botón rojo
        delete_button.connect("clicked", lambda _: (
        self.handler.on_posologie_delete_button(patient_id, medication_id, posologie_id), dialog.close()))  # Cerrar el diálogo
        button_box.append(delete_button)  # Añadir el botón de eliminar a la caja de botones

        button_box.append(accept_button)  # Añadir el botón de aceptar a la caja de botones

        box.append(button_box)

        dialog.set_child(box)
        dialog.show()

    def ordenarListboxPosologias(self) -> None: #no devuelve nada
        #no podemos suar sort() directamente en el GiolistStore por tanto habra q extraer los elementos a una lista python
        #ordenarlos y luego volverlos a meter en la lista; ya q el listStore no admite sort() con argumento key;  :(
        # Extraer todos los elementos de la lista de posologias a una lista normal python
        posologias = [self.PosologiesList.get_item(i) for i in range(self.PosologiesList.get_n_items())]

        # Ordenar la lista de python creada; posologias según la hora y luego los minutos (si la hora coincide, pues se ordena por minutos)
        posologias.sort(key=lambda posologie: (int(posologie.hour), int(posologie.minute)))

        # Vaciar la lista de posologias
        self.PosologiesList.remove_all()

        # Añadir los elementos ordenados a la lista de posologias
        for posologia in posologias:
            self.PosologiesList.append(posologia)

        # El modelo se actualiza automáticamente en la ListBox debido al bind_model
