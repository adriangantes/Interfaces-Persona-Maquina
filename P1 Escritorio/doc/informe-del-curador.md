# Informe del Curador-Traductor

  El traductor debe definir -con sus propias palabras- los objetivos
  de aprendizaje de la práctica.

  El curador buscará los recursos online que ayuden al equipo a
  completar de mejor manera su tarea.
  
  Además, el curador es el responsable de recopilar y organizar de
  forma esquemática, todas las fuentes adicionales de información que
  el grupo ha utilizado para desarrollar la actividad.

  Finalmente, el curador tiene la tarea de presentar y explicar a sus
  compañeros los recursos indentificados.

  > A continuación se ofrece una sugerencia sobre el contenido del
  > informe que debe generar la persona encargada de este role cada
  > semana.

  

## Objetivos de aprendizaje de la Tarea 1

  - Aprender a distribuir roles:
    Cada miembro del equipo asume un rol específico que va rotando según las tareas.
    Debemos hacer una asignación clara de roles, y cada miembro debe aprender a
    ejercer su respectivo rol para progresar adecuadamente.
    La rotación nos permite aprenderemos a reconocer y valorar las contribuciones de cada
    miembro del equipo.
    
  - Aprender programación en Python:
    Python es un lenguaje de programación versátil y "sencillo", pero es la primera vez
    que lo empleamos en una práctica larga y por tanto debemos aprender desde los
    conceptos básicos hasta conceptos más avanzados. Además, debemos acostumbrarnos
    a su flexibilidad y adaptarnos a ella, pues venimos de usar lenguajes bastante
    más restrictivos (C, Java, Ocaml)
    
  - Aprender a usar GTK+ y Adwaita en Python:
    GTK+ es una biblioteca para crear interfaces gráficas, cosa que nunca habíamos
    usando previamente. Debemos familiarizarnos con ella y con su implementación en
    Python. El principal reto que tenemos es acostrumbrarlos a la programación
    guiada por eventos.
    
  - Aprender a emplear el patrón de diseño Model-View-Presenter (MVP):
    Debemos entender la separación entre sus diferentes partes y los objetivos
    que cumple cada una, evitando mezclar responsabilidades de forma incorrecta
    y mantendiendo el código bien estructurado.
    
  - Aprender a diseñar una aplicación con interfaz:
    Si bien ya habíamso diseñado una aplicación anteriormente, nunca habíamos llegado a
    desarrollarla. Por tanto, debemos profundizar más en la experiencia del usuario y
    la funcionalidad general además de ser capaces de implementar el diseño en código.

## Recursos empleados en la Tarea 1

  - https://docs.gtk.org/gtk4/class.ListStore.html : Documentación oficial de GTK sobre el objeto ListStore.
  - https://blog.hubspot.es/website/menu-hamburguesa : Qué es un menú hamburguesa.
  - https://docs.gtk.org/gtk4/class.ScrolledWindow.html : Documentación de GTK sobre la ventana deslizable.
  - https://docs.gtk.org/gtk4/class.TreeView.html : Info sobre la vista de Arbol. La lista se mete dentro. Es scrolleable.
  - https://github.com/Taiko2k/GTK4PythonTutorial/blob/main/README.md : Tutorial básico de uso de GTK4 con Python.
  - https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/ : Doc de Adwaita.
  - https://docs.gtk.org/gtk4/class.InfoBar.html : InfoBar, mensaje temporal para informar que desaparece (deprecated).
  - https://stackoverflow.com/questions/39236245/gtk-widget-destroy-is-necessary-on-python: Sobre la destrucción de widgets.
  - https://discourse.gnome.org/t/gtkmm-4-0-how-to-check-if-a-gtk-entry-has-focus/11035/5: Sobre el focus en una entry.
  - https://docs.gtk.org/gtk4/class.Popover.html : Sobre el Popover widget para notificaciones temporales.
  + https://docs.gtk.org/gtk4/?q=entry#classes : Entry widget. Importante.
  + https://api.gtkd.org/gtk.Entry.Entry.html : Más sobre Entry.
  + https://pygobject.gnome.org/tutorials/gtk4/controls/entries.html : Todavía más sobre entries y sus muchos tipos.
  - https://docs.gtk.org/gtk4/class.SearchEntry.html : Sobre search entry para barras de búsqueda.

## Objetivos de aprendizaje de la Tarea 2 y 3

  - Comprender la necesidad y uso de concurrencia:
    La concurrencia es esencial en una interfaz para que responda correctamente a las acciones
    del usuario. Entendimos que es especialmente esencial cuando se trata de E/S, por lo que
    es muy importante aprender a aplicarlo donde toca y de forma correcta, por lo que debemos
    aprender a implementarlos en Python.
    
  - Aprender a gestionar errores de E/S:
    Capturar los errores de entrada salida y ofrecer un feedback adecuado al usuario es necesario
    para que el usuario pueda interactuar correctamente con la interfaz, por lo que debemos
    aprender a gestionar errores en Python y entender donde hay que colocarlos y como mandar
    los mensajes al usuario de forma adecuada, empleando GTK, para que entienda lo que está
    ocurreiendo.

  - Entender el uso de locale en Python para la Internacionalización de la interfaz:
    Poder internacionalizar una aplicación es muy improtante para que usuarios de diferentes
    lenguas la puedan usar correctamente. Para implementarlo, debemos entender el funcionamiento
    de locale en Python y aprender a implementarlo de forma correcta, para lo que será necesario
    aprender también a usar gettext junto a las herramientas de creación de archivos de traducción.

## Recursos empleados en la Tarea 2 y 3

  - https://stackoverflow.com/questions/11923008/threading-in-gtk-python : Sobre el uso de threading en Python
  - https://pygobject.gnome.org/guide/threading.html : Documentación de PyGObject sobre el uso de threads con GTK
  - https://docs.python.org/3/library/threading.html : Documentación de Python sobre la librería threading
  - https://docs.python.org/3/library/locale.html : Documentación de Python sobre el módulo locale
  - https://docs.python.org/3/library/gettext.html : Documentación de Python sobre gettext
  - https://lokalise.com/blog/translating-apps-with-gettext-comprehensive-tutorial/ : Tutorial sobre el uso de gettext
