# Interfaz Dinámica

## Móvil

```mermaid
flowchart TD;
    CualquierPantalla["CualquierPantalla"] -- Se queda sin conexión a internet --> ErrorSinConexion["ErrorSinConexion"];
    ErrorSinConexion -- vuelve la conexion --> ListaMedicamentos("Lista de Medicamentos");
    ListaMedicamentos -- Clicka en un medicamento --> DetalleMedicamento("Informacion sobre Medicamento");
    DetalleMedicamento -- click atras --> ListaMedicamentos;
    
    DetalleMedicamento -- Clicka añadir toma --> AnadirToma("Añadir toma");
    AnadirToma -- click en guardar o atrás --> DetalleMedicamento;
    AnadirToma -- click en guardar con datos incorrectos --> AnadirToma("Añadir Toma");

    CualquierAplicacion["Cualquier aplicación o pantalla apagada"] -- Salta notificación --> Notificacion
    Notificacion["Mostrar notificación"] -- Selecciona Aceptar (Detiene notificación) --> CualquierAplicacion
```

## Reloj

```mermaid
flowchart TD;
    CualquierPantalla["CualquierPantalla"] -- Se queda sin conexión a internet --> ErrorSinConexion["ErrorSinConexion"];
    ErrorSinConexion -- vuelve la conexion --> ListaMedicamentos("Lista de Medicamentos");
    ListaMedicamentos -- Clicka en un medicamento --> DetalleMedicamento("Informacion sobre Medicamento");
    DetalleMedicamento -- click atras --> ListaMedicamentos;
    
    DetalleMedicamento -- Clicka añadir toma actual --> AnadirToma("Añadir toma");
    AnadirToma -- click en SI o NO --> DetalleMedicamento;

    CualquierAplicacion["Cualquier aplicación o pantalla apagada"] -- Salta notificación --> Notificacion
    Notificacion["Mostrar notificación"] -- Selecciona Aceptar (Detiene notificación) --> CualquierAplicacion
```

# Diagrama de Clases

## Móvil

```mermaid
classDiagram
    class ScopedModel {
        - estadoAplicacion: EstadoAplicacion
        + notificarSuscriptores(): void
    }

    class EstadoAplicacion {
        + listaMedicamentos: List[Medicamento]
        + obtenerMedicamentos(): List[Medicamento]
        + agregarToma(medicamento: Medicamento, fechaHora: Date): void
        + eliminarToma(medicamento: Medicamento, fechaHora: Date): void
        + actualizarToma(medicamento: Medicamento, fechaHora: Date): void
	+ verificarConexion(): boolean
    }

    class Medicamento {
        + nombre: String
        + mostrarTomas: List[Date]
    }

    class PantallaMedicamentos {
        + render(): void
        + subscribeToModel(model: ScopedModel): void
    }

    class PantallaDetalleMedicamento {
        + render(): void
        + subscribeToModel(model: ScopedModel): void
    }

    class PantallaAgregarToma {
        + render(): void
        + validarDatos(): boolean
        + guardarToma(): void
    }

    class Notificacion {
        + mostrarNotificacion(medicamento: Medicamento): void
	+ detenerNotificacion(): void
    }

    class PantallaSinConexion {
        + render(): void
        + mostrarMensaje(): void
    }

    ScopedModel o-- EstadoAplicacion : maneja
    EstadoAplicacion o-- Medicamento : contiene
    PantallaSinConexion --> EstadoAplicacion : verifica conexion
    PantallaMedicamentos --> ScopedModel : suscribe al modelo
    PantallaDetalleMedicamento --> ScopedModel : suscribe al modelo
    PantallaAgregarToma --> ScopedModel : suscribe al modelo
    Notificacion --> EstadoAplicacion : consulta
```

## Reloj

```mermaid
classDiagram
    class ScopedModel {
        - estadoAplicacion: EstadoAplicacion
        + notificarSuscriptores(): void
    }

    class EstadoAplicacion {
        + listaMedicamentos: List[Medicamento]
        + obtenerMedicamentos(): List[Medicamento]
        + agregarToma(medicamento: Medicamento, fechaHora: Date): void
        + establecerProximaToma(medicamento: Medicamento, fechaHora: Date): void
        + verificarConexion(): boolean
    }

    class Medicamento {
        + nombre: String
        + proximaToma: Date
    }

    class PantallaSinConexion {
        + render(): void
        + mostrarMensaje(): void
    }

    class PantallaMedicamentos {
        + render(): void
        + subscribeToModel(model: ScopedModel): void
    }

    class PantallaDetalleMedicamento {
        + render(): void
        + agregarTomaActual(): void
    }

    class PantallaAgregarToma {
        + render(): void
        + mostrarConfirmacion(): void
        + guardarTomaSiConfirmado(): void
    }

    class Notificacion {
        + mostrarNotificacion(medicamento: Medicamento): void
        + detenerNotificacion(): void
    }

    ScopedModel o-- EstadoAplicacion : maneja
    EstadoAplicacion o-- Medicamento : contiene
    PantallaSinConexion --> EstadoAplicacion : verifica conexión
    PantallaMedicamentos --> ScopedModel : suscribe al modelo
    PantallaDetalleMedicamento --> ScopedModel : suscribe al modelo
    PantallaAgregarToma --> ScopedModel : suscribe al modelo
    Notificacion --> EstadoAplicacion : consulta
```

# Diagramas de Secuencia

## Añadir Toma (Móvil)

```mermaid
sequenceDiagram
    participant Usuario
    participant PantallaMedicamentos
    participant PantallaDetalleMedicamento
    participant PantallaAgregarToma
    participant ScopedModel
    participant EstadoAplicacion

    Usuario ->> PantallaMedicamentos: Inicia aplicación
    PantallaMedicamentos -->> PantallaDetalleMedicamento: Selecciona medicamento X
    Usuario ->> PantallaDetalleMedicamento: Toca "Añadir Toma"
    PantallaDetalleMedicamento ->> PantallaAgregarToma: Abre pantalla para confirmar
    PantallaDetalleMedicamento -->> Usuario: Datos Erroneos
    Usuario ->> PantallaAgregarToma: Toca "Guardar"
    PantallaAgregarToma ->> ScopedModel: Invoca guardarTomaSiConfirmado()
    ScopedModel ->> EstadoAplicacion: agregarToma(medicamento, fechaHora)
    EstadoAplicacion ->> ScopedModel: Actualiza estado
    EstadoAplicacion -->> ScopedModel: Error de la BD
    ScopedModel ->> PantallaDetalleMedicamento: Notifica cambio
    PantallaDetalleMedicamento ->> Usuario: Muestra la nueva toma guardada
```

## Añadir Toma (Reloj)
```mermaid
sequenceDiagram
    participant Usuario
    participant PantallaMedicamentosReloj
    participant PantallaDetalleMedicamentoReloj
    participant ScopedModel
    participant EstadoAplicacion

    Usuario ->> PantallaMedicamentosReloj: Inicia aplicación
    PantallaMedicamentosReloj -->> PantallaDetalleMedicamentoReloj: Selecciona medicamento X
    Usuario ->> PantallaDetalleMedicamentoReloj: Toca "Añadir Toma"
    PantallaDetalleMedicamentoReloj ->> ScopedModel: Llama a agregarToma
    ScopedModel ->> EstadoAplicacion: agregarToma(medicamento, fechaHora)
    EstadoAplicacion ->> ScopedModel: Actualiza estado
    EstadoAplicacion -->> ScopedModel: Error de la BD
    ScopedModel ->> PantallaDetalleMedicamentoReloj: Notifica cambio
    PantallaDetalleMedicamentoReloj ->> Usuario: Confirma que la toma fue guardada
```

## Notificar Usuario próxima Toma (Reloj)

```mermaid
sequenceDiagram
    participant Usuario
    participant ScopedModel
    participant EstadoAplicacion
    participant PantallaNotificacionTomarDosis

    Note right of EstadoAplicacion: Verificar tiempo hasta próxima dosis
    EstadoAplicacion ->> ScopedModel: Notificación: Toma de medicamento en 5 minutos
    ScopedModel ->> PantallaNotificacionTomarDosis: Crear notificación de toma de medicamento
    PantallaNotificacionTomarDosis ->> Usuario: Mostrar aviso: Toma de medicamento en 5 minutos
    Usuario ->> ScopedModel: Clic en "Aceptar" notificación
    ScopedModel ->> EstadoAplicacion: Registrar usuario avisado
    EstadoAplicacion ->> ScopedModel: Confirmación de registro completado
    ScopedModel ->> PantallaNotificacionTomarDosis: Cerrar notificación de toma de medicamento
    PantallaNotificacionTomarDosis ->> Usuario: Notificación cerrada
```

## Notificar Usuario próxima Toma (Móvil)

```mermaid
sequenceDiagram
    participant Usuario
    participant ScopedModel
    participant EstadoAplicacion
    participant PantallaNotificacionTomarDosis

    Note right of EstadoAplicacion: Verificar tiempo hasta próxima dosis
    EstadoAplicacion ->> ScopedModel: Notificación: Toma de medicamento en 5 minutos
    ScopedModel ->> PantallaNotificacionTomarDosis: Crear notificación de toma de medicamento
    PantallaNotificacionTomarDosis ->> Usuario: Mostrar aviso: Toma de medicamento en 5 minutos
    Usuario ->> ScopedModel: Clic en "Aceptar" notificación
    ScopedModel ->> EstadoAplicacion: Registrar usuario avisado
    EstadoAplicacion ->> ScopedModel: Confirmación de registro completado
    ScopedModel ->> PantallaNotificacionTomarDosis: Cerrar notificación de toma de medicamento
    PantallaNotificacionTomarDosis ->> Usuario: Notificación cerrada
```
