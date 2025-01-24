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

  

## Objetivos de aprendizaje de la semana 1

  - Aprender a distribuir roles:
    Cada miembro del equipo asume un rol específico que va rotando según las tareas.
    Debemos hacer una asignación clara de roles, y cada miembro debe aprender a
    ejercer su respectivo rol para progresar adecuadamente.
    La rotación nos permite aprenderemos a reconocer y valorar las contribuciones de cada
    miembro del equipo.
    
  - Aprender programación en Dart:
    El lenguaje de programación Dart; es la primera vez que lo usamos. Esta desarrollado 
    por Google, esta pensando para integrarse de manera completa con la librería flutter
    (también desarrollada por Google) lo que lo convierte en un lenguaje ideal para la 
    programación de aplicaciones móviles tanto en Android como en IOS y dispositivos más
    pequeños como smartWatches o pulseras de actividad. Es un lenguaje de programación orientado
    a objetos; Dart tiene una sintaxis parecida a otros lenguajes como C, Java y JavaScript; 
    el código se tiene que compilar a lenguaje máquina; permite la compilación a nativo y a JavaScript
    (pensando para aplicativos web ya que permite el desarrollo de aplicaciones web), Dart permite
    el desarrollo asíncrono y concurrente gracias a stream y future. Las principales ventajas son:
    buen sistema de tipos seguro, compilación rápida y ejecución en los dispositivos eficiente, 
    programación concurrente fácil, mediante el uso de flutter podemos ejecutar con el mismo código 
    la aplicación tanto en dispositivos Android como IOS.

  - Aprender a usar Flutter en Dart:
    Flutter es un framework para crear aplicaciones gráficas (IU) diseñada principalmente para móviles,
    cosa que nunca habíamos usando previamente. Como principales ventajas tiene el HOT RELOAD (probar los cambios en el 
    código en caliente sin tener que recompilar toda la aplicación, Tiene widgets, temas etc ya hechos como el
    Material Design (para Android) y Cupertino (para IOS). Es un solo código multiplataforma (android, android watches, ios,
    linux, windows, etc).
    
  - Aprender a emplear el patrón de diseño ScopedModel:
    Debemos entender la separación entre sus diferentes partes y los objetivos
    que cumple cada una, evitando mezclar responsabilidades. ScopedModel ayuda a compartir y 
    actualizar datos en varios widgets de una aplicación sin la necesidad de pasar manualmente 
    datos y controladores a través de múltiples niveles de widgets, una técnica conocida como 
    "prop drilling". ScopedModel proporciona un modelo en el que esta un estado y los
    widgets hijos pueden acceder a el. Usa el patron observador en el que los widgets hijos
    escuchan y asi permite actualizarse una vez ven cambios en el modelo. Como principal desventaja
    frente a otros como el Provider, es más dificil de escalar. La biblioteca define tres componentes principales:
        *Model:* Una clase que extiende Model y contiene el estado que deseas compartir en la aplicación.
        *ScopedModel:* Un widget que proporciona un Model a sus hijos.
        *ScopedModelDescendant:* Un widget que escucha y reacciona a los cambios en el Model.
    
## Recursos empleados en la Tarea 1

  - https://dart.dev/guides : Documentación oficial de Dart.
  - https://docs.flutter.dev/ : Documentación oficial de Flutter
  - https://dart.dev/get-dart : Guía Instalacion de Dart
  - https://docs.flutter.dev/get-started/install/linux/android : Guía instalacion Flutter
  - https://developer.android.com/studio/install?hl=es-419 : Guía instalación de AndroidStudio
  - https://developer.android.com/about/versions/14/setup-sdk?hl=es-419 : Guía instalación AndroidSDK
  - https://www.youtube.com/watch?v=3tm-R7ymwhc&themeRefresh=1 : Información sobre patrones que podemos usar
  - https://pub.dev/packages/scoped_model : Información sobre ScopedModel
  - https://codelabs.developers.google.com/codelabs/flutter-codelab-first?hl=es-419#4 : Tutorial Crear aplicación el flutter
  - https://docs.flutter.dev/cookbook : Flutter cookbook, solucion a problemas frecuentes





## Objetivos de aprendizaje de la semana 2

- **Aprender a programar en Dart:**  
  Continuamos profundizando en el lenguaje de programación Dart para mejorar nuestras habilidades. Nos centramos en reforzar conceptos de programación orientada a objetos, uso de asíncronía con `Future` y `Stream`, y en cómo estructurar nuestro código para que sea más eficiente y limpio. Esto nos permitirá implementar nuevas funcionalidades en nuestras aplicaciones de forma ordenada.

- **Aprender el uso de la biblioteca Flutter:**  
  En esta semana, nos enfocamos en ampliar nuestro conocimiento sobre Flutter para construir interfaces gráficas. Exploramos más widgets avanzados, la personalización de elementos visuales y el uso de herramientas como `FloatingActionButton`. Además, empezamos a comprender cómo integrar componentes que mejoren la interacción del usuario, como `showDatePicker` y `showTimePicker`.

- **Creación de emuladores de dispositivos móviles y smartwatch:**  
  Instalamos y configuramos emuladores tanto de dispositivos móviles como de smartwatches para probar nuestras aplicaciones. Esto nos permitió verificar la funcionalidad de nuestras interfaces y ajustar el comportamiento de la aplicación según el dispositivo, asegurando compatibilidad en diferentes plataformas.

- **Uso de la biblioteca `http` en Dart para realizar peticiones al servidor:**  
  Aprendimos a realizar peticiones `GET` y `POST` al servidor utilizando la biblioteca `http`. Esto nos permitió enviar y recibir datos, además de entender cómo manejar respuestas asincrónicas y gestionar errores, lo cual es clave para construir aplicaciones conectadas a servicios backend.

- **Ajustar y programar una interfaz para dispositivos móviles y smartwatch:**  
  Nos enfocamos en diseñar y programar una interfaz adaptable que funcione correctamente tanto en pantallas de móviles como en relojes inteligentes. Estudiamos los principios de diseño responsivo y exploramos cómo personalizar widgets en Flutter para garantizar una experiencia de usuario fluida y consistente en distintos tamaños de pantalla.

---

## Recursos empleados en la Tarea 2

- [Documentación para realizar peticiones HTTP en Flutter](https://docs.flutter.dev/cookbook/networking/send-data)  
- [Uso avanzado de DatePicker en Flutter](https://medium.com/flutter-community/a-deep-dive-into-datepicker-in-flutter-37e84f7d8d6c)  
- [Documentación oficial de showDatePicker](https://api.flutter.dev/flutter/material/showDatePicker.html)  
- [Documentación oficial de FloatingActionButton](https://api.flutter.dev/flutter/material/FloatingActionButton-class.html)  
- [Tutorial sobre TimePicker en Flutter](https://www.kindacode.com/article/working-with-time-picker-in-flutter)  
- [Documentación oficial de showTimePicker](https://api.flutter.dev/flutter/material/showTimePicker.html)




## Objetivos de aprendizaje de la semana 3

- **Aprender sobre Flutter Test y pruebas en Flutter:**  
  En esta semana, nos centramos en el uso de **Flutter Test** para realizar pruebas automatizadas de nuestras aplicaciones. Exploramos cómo escribir pruebas unitarias, de integración y de widgets, lo cual es crucial para garantizar que las aplicaciones funcionen correctamente en diferentes escenarios. Esto nos permitió verificar el comportamiento de la lógica de la aplicación y los componentes visuales, mejorando la calidad y fiabilidad del código.

- **Introducción al uso de `ScaffoldMessenger` para mostrar mensajes:**  
  Aprendimos a utilizar el **`ScaffoldMessenger`** para mostrar mensajes de forma adecuada en nuestras aplicaciones. Esto nos permite gestionar los mensajes en la pantalla, como **snackbars**, de manera eficiente y con una experiencia de usuario coherente. Investigamos cómo manejar cambios importantes en el flujo de trabajo de la interfaz con los cambios introducidos en la nueva versión de Flutter.

- **Uso de `Provider` para gestión de estado:**  
  Profundizamos en el uso de la librería **`provider`**, que es una de las herramientas más comunes en Flutter para la gestión de estado. Aprendimos a compartir y gestionar el estado entre diferentes partes de la aplicación de manera eficiente. Esto facilita la creación de aplicaciones más escalables y mantenibles, especialmente cuando se tienen múltiples componentes que dependen de un mismo estado.

- **Realización de pruebas de widgets con Flutter:**  
  A lo largo de la semana, nos enfocamos en realizar pruebas de widgets utilizando las herramientas de pruebas integradas en Flutter. Investigamos cómo utilizar los **finders** para localizar widgets y realizar acciones de prueba sobre ellos, como interactuar con botones, formularios y otros componentes. Esto nos permitió asegurarnos de que la interfaz de usuario se comporte correctamente ante diversas acciones del usuario.

- **Entender las pruebas de integración:**  
  Comenzamos a comprender la diferencia entre las pruebas unitarias y las pruebas de integración. Aprendimos a escribir pruebas que validen el comportamiento de la aplicación completa, garantizando que todos los componentes interactúen correctamente entre sí.

---

## Recursos empleados en la Tarea 3

- [Documentación sobre cambios importantes en `ScaffoldMessenger`](https://docs.flutter.dev/release/breaking-changes/scaffold-messenger)  
- [Guía sobre pruebas de widgets y finders en Flutter](https://docs.flutter.dev/cookbook/testing/widget/finders)  
- [Paquete `Provider` para gestión de estado en Flutter](https://pub.dev/packages/provider)  
- [Documentación oficial sobre pruebas en Flutter](https://docs.flutter.dev/testing/overview)

