# Informe del Facilitador-Administrador

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

  - Descripción de la tarea:

      Las tareas de la semana 1 consisten en:
      - Realizar el diseño de la interfaz, uno para móvil y otro para reloj,
        adaptado para la gestión de errores.
      - Seleccionar un patrón arquitectónico adecuado.
      - Realizar el diseño UML estático y dinámico del software en base
        al patrón seleccionado.
    
      A mayores, tendremos que adaptarnos al nuevo entorno de desarrollo
      (Flutter + Dart).
  
  - Asignación de responsables:
      - Adrián: Diseño de la interfaz.
      - Samuel: Selección del patrón y revisión del diseño.
      - Juan: Revisión del diseño.
  
  - Estado de completud:

      Se ha seleccionado el patrón Scoped Model y terminado por completo el diseño
      básico de la interfaz y los diagramas UML correspondientes al diseño estático
      y dinámico empleando el patrón seleccionado como base y usando el lenguaje
      markdown con Mermaid.

  - Conflictos, desviaciones, etc:

      No hubo ningun conflicto y/o desviación notable de lo planificado.

## Estado del repositorio en la semama 1

  En la primera semana se han hecho cambios únicamente dentro de la carpeta /doc,
  correspondientes a todos los documentos del diseño y las documentaciones
  corresponedientes a cada rol para esta semana.
  
  Debido a que, a diferencia de en la Práctica 1, solo había que hacer el diseño
  sin llegar a programarlo, la entrega se hizo mucho más gestionable y menos
  estresante para todos, además de provocar menos conflictos con otras asignaturas.



##  Registro de tareas llevadas a cabo durante la semana 2 y 3
  - Descripción de la tarea:

      Las tareas de la semana 2 y 3 consisten en:
      - Familiarizarnos con Flutter y con su lenguaje Dart. Tanto la sintaxis como la forma de trabajar.
      - Aprender a implementar correctamente el patrón de diseño seleccionado.
      - Implementar la aplicación siguiendo el Diseño hecho en la tarea anterior, tanto para móvil como reloj.
  
  - Asignación de responsables:
      - Adrián: Corrección del diseño y supervisión del desarrollo.
      - Samuel: Implementación de Login y Medicacations. Adaptación de la aplicación a reloj.
      - Juan: Implementación de los Intakes. Revisión de la implementación para reloj.
  
  - Estado de completud:

      Se ha desarrollado la aplicación para móvil sin los casos de uso opcionales relacionados
      a notificaciones siguiendo el patrón y el diseño dentro de lo posible. El desarrollo de
      reloj está casi completado pero faltan pantallas por adaptar correctamente.

  - Conflictos, desviaciones, etc:

      Debido a la carga de trabajos en estas semanas, el tiempo dedicado al trabajo tuvo que
      disminuir y repartirse de forma desigual. No hubo tiempo de implementar las notificaciones.
      Debido principalmente al desconocimiento incial del nuevo entorno de desarrollo, hubo que 
      adaptar los diseños de la Tarea anterior debido a que no eran completamente apropiados.

## Estado del repositorio en la semama 2 y 3

  Se ha trabajado principalmente en la implementación, por lo que la mayoría de cambios se
  encuentran en /src. Se hizo tanto el main como el modelo con las funciones necesarias para
  acceder a la Base de Datos.
  A mayores, se hizo toda la documentación correspondiente a cada rol para estas dos semanas.
  
  Debido a que en estas semanas había que entregar los trabajos de 4 de las asignaturas, no
  se le pudo dedicar tanto tiempo como podría haber necesitado este trabajo.



##  Registro de tareas llevadas a cabo durante la semana 4
  - Descripción de la tarea:

      Las tareas de la semana 4 consisten en:
      - Corregir errores encontrados tras la entrega de la Tarea 2.
      - Adaptación del Main y el Modelo para poder usar Servicios Mock en lugar de acceder a la BD.
      - Implementación de los test para los casos de uso y error de la aplicación.
  
  - Asignación de responsables:
      - Adrián: Supervisión del progreso y mediación.
      - Samuel: Corrección de errores encontrados en la tarea anterior y revisión de esta.
      - Juan: Desarrollo del Model y los test.
  
  - Estado de completud:

      Se han corregido todos los fallos detectados.
      Se ha adaptado por completo el Modelo con los MockService necesarios y se ha cambiado el Main
      para adaptarse a estos cambios.
      Se han desarrollado todos los test para casos de uso y error encontrados.

  - Conflictos, desviaciones, etc:

      Gracias a una menor carga de trabajo por parte de las otras asignaturas, se han podido terminar
      las tareas planificadas sin conflictos ni desviaciones.

## Estado del repositorio en la semama 4

  Se han hecho cambios considerables en el Model, separando la interacción con la BD a las clases Service
  e implementando las clases MockService de cada recurso.
  También hubo notables cambios en el Main, principalmente para poder adaptarse a los cambios producidos
  en el Model.
  Se ha creado el archivo widget_test.dart para la implementación de los test de widget, que revisan
  todos los casos de uso que se pudieron detectar.