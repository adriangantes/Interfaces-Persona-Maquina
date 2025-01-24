# Informe del Facilitador-Administrador (Adrián Edreira)

  Se considera que este rol facilita la configuración y el
  funcionamiento del grupo. La persona encargada de desempeñar este
  rol actúa como líder del grupo y es responsable de la distribución
  de tareas, la mediación de conflictos, la comprobación del
  cumplimiento de las obligaciones y la motivación y ánimo de sus
  compañeros. Es no solo el encargado de que la tarea se haga, sino de
  que la salud mental del grupo se mantenga en niveles deseables.
  
  Además, se encarga de revisar en el repositorio de _github_ el
  trabajo del grupo.


  > A continuación se ofrece una sugerencia sobre el contenido del
  > informe que debe generar la persona encargada de este role cada
  > semana.


##  Registro de tareas llevadas a cabo durante la semana 1

  - Descripción de la tarea
  
  - Asignación de responsables
  
  - Estado de completud
  
  - Conflictos, desviaciones, etc.
  

## Estado del repositorio en la semama 1

Lo primero que hicimos fue repartirnos los roles, posteriormente corregimos cosas de los diseños de las interfaces de nuestras 
prácticas individuales y escogimos un diseño en común lo más completo y sencillo posible. Tras ello, comenzamos a desarrollar el 
código, creamos el diseño final de la interfaz y los diagramas, el de clases, el de la interfaz y los de secuencia. Además, 
seleccionamos el modelo MVP para tener bien separadas cada una de las partes del programa.

Realizamos reuniones para ir avanzando conjuntamente e ir solucionando errores que nos podían surgir a la hora de crear la 
aplicación. Posteriormente uno de los miembros realizó los diseños UML necesarios en Mermaid y tras una revisión general de los 
diseños como del programa decidimos que estaba listo para enviar.

Debido a la carga de trabajo que suponía esta primera iteración decidimos atrasar la entrega de la primera tarea a la semana 
siguiente. Por otra parte, surgían conflictos de rama en el repositorio de github cuando dos personas querían subir su parte de 
código a github, así que optamos por enviar el código a un compañero y que él se encargara de hacer los push.

Tras dos semanas en las que todo el grupo estuvo saturado y estresado, con unos niveles de salud mental no muy óptimos, consecuencia 
de la carga de trabajo de esta tarea conseguimos llegar al objetivo que nos habíamos marcado para enviar en esta primera tarea.

## Estado del repositorio en la semama 2

Durante la semana 2, decidimos intentar completar tanto la tarea 2 como la 3, con el objetivo de quedar más disponibles de cara a la
segunda práctica y la revisión de fallos de esta primera práctica antes de entregar. En cuanto a la tarea 2, la creación de threads
fue una tarea sencilla junto con la creación de un spinner, necesario para dar el feedback al usuario de que se estaban cargando los
datos desde la base de datos. Todo lo que modificamos se encontraba en nuestro presenter; allí creamos un thread cada vez que
llamábamos a una función del presenter, arrancábamos el spinner y poníamos a funcionar el thread, mientras que con Glib.idle_add
actualizábamos la interfaz una vez que terminaba el thread. También actualizamos los diagramas UML para representar el trabajo de
dichos threads.

En cuanto a la tarea 3, teníamos que internacionalizar nuestra aplicación, cambiar el formato de la interfaz según el país del usuario,
así como el formato de las fechas, además de lo obvio: cambiar el idioma de los textos de nuestra aplicación. Buscamos las líneas de
código que contenían texto o información que se le mostraría al usuario, y mediante la librería gettext con su función gettext metimos
todos los textos dentro de esta función para que se tradujesen según el idioma del usuario final. La traducción del formato de las
fechas nos dio más complicación de lo esperado, pero designando en los archivos de "locale" el formato según si iba primero el día,
el mes o el año, lo pudimos solucionar.

Sin más complicaciones, logramos los objetivos que nos habíamos marcado y decidimos enviar las tareas completadas a revisión para poder 
comenzar la segunda práctica mientras recibíamos el feedback de esta primera práctica para corregir los errores.