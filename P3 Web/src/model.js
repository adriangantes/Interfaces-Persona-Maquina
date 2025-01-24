// Simulación de una lista de pacientes
/*
const pacientes = [
  { id: "1", nombre: "Juan Pérez" },
  { id: "2", nombre: "María López" },
  { id: "3", nombre: "Carlos Ramírez" },
  { id: "4", nombre: "Ana Fernández" },
  { id: "5", nombre: "Luis Torres" },
];
*/

const BASEURL = "http://localhost:8000/"; //URL API peticion

// Esperar a que cargue el DOM y las hojas de estilo (solo las que vayan antes del script)
document.addEventListener("DOMContentLoaded", main)

function main() { //funcion principal del JS

  pacienteIdSeguro = null;

  var patientsIndex = 0;
  const patientsPerLoad = 10

  // Referencias a los elementos del DOM
  const searchInput = document.getElementById("search-input"); // Campo de texto para busqueda de paciente
  const searchButton = document.getElementById("search-button"); // Boton de busqueda de lupa
  const listPatientsButton = document.getElementById("load-all-patients-button"); //boton de busqueda para mostrar lista con todos los pacientes
  const resultList = document.getElementById("result-list"); // Lista de resultados de los pacientes
  const medicationListPatientPage = document.getElementById("medications-list");
  const posologiesListMedicationPage = document.getElementById("posologies-list");
  const posologiesList = document.getElementById("posologies-intakes-list");
  const intakesList = document.getElementById("intakes-list");

  function obtenerURL(ruta, parametros = {}) {
    const url = new URL(BASEURL);
    url.pathname += `${ruta}`;
    //añadir parametros de consulta a la URL si existen

    //añadir parametros de consulta a la ruta
    for(const key in parametros){
      url.searchParams.append(key, parametros[key]);
    }

    return url.toString();
  }


  // Funcion para buscar pacientes
  async function buscarPacientes(query) {
    try{
      // Filtra los pacientes que coincidan con la búsqueda
      const url = obtenerURL(`patients`,{code: query});
      
      const response = await fetch(url);

      //mirar si la respuesta fue exitosa o no
      if(!(response.ok)){
        //no fue guay asi q error
        throw new Error(`HTTP error; status returned ${response.status}`);
      }

      //parseamos la respuesta a JSON
      const data = await response.json();
      
      // Muestra los resultados en la lista
      mostrarResultados(data);

    } catch(error){
      //distinguir entre hay conexion o no con la BD
      if(error instanceof TypeError){
        // Errores de red o problemas de conexión
        console.error("Error de red o conexión:", error.message);
        mostrarError("Error: No se pudo conectar al servidor. Por favor, revisa tu conexión a Internet.");
      }else{
        console.error("Error al buscar pacientes: ", error.message); //mostrar error en la consola de depuracion

        resultList.innerHTML = "<li>No se encontraron pacientes</li>"; // Mensaje de error
      }
    }
  }


  async function buscarTodosLosPacientes(){
    try{

      // Filtra los pacientes que coincidan con la búsqueda
      const url = obtenerURL(`patients`);

      const response = await fetch(url);

      //mirar si la respuesta fue exitosa o no
      if(!(response.ok)){
        //no fue guay asi q error
        throw new Error(`HTTP error; status returned ${response.status}`);
      }

      //parseamos la respuesta a JSON
      const data = await response.json();
      
      // Muestra los resultados en la lista
      mostrarPacientes(data);

    }catch (error){
      //distinguir entre hay conexion o no con la BD
      if(error instanceof TypeError){
        // Errores de red o problemas de conexión
        console.error("Error de red o conexión:", error.message);
        mostrarError("Error: No se pudo conectar al servidor. Por favor, revisa tu conexión a Internet.");
      }else{
        console.error("Error al buscar todos los pacientes: ", error.message); //mostrar error en la consola de depuracion

        resultList.innerHTML = "<li>No se encontraron pacientes</li>"; // Mensaje de error
      }
    }
  }

  /*
  async function buscarNPacientes(i, n){
    try{
      // Filtra los pacientes que coincidan con la búsqueda
      const url = obtenerURL(`patients`, {start_index: i, count: n});

      const response = await fetch(url);

      //mirar si la respuesta fue exitosa o no
      if(!(response.ok)){
        //no fue guay asi q error
        throw new Error(`HTTP error; status returned ${response.status}`);
      }

      //parseamos la respuesta a JSON
      const data = await response.json();
      
      // Muestra los resultados en la lista
      agregarPacientes(data);

    }catch (error){
      //distinguir entre hay conexion o no con la BD
      if(error instanceof TypeError){
        // Errores de red o problemas de conexión
        console.error("Error de red o conexión:", error.message);
        mostrarError("Error: No se pudo conectar al servidor. Por favor, revisa tu conexión a Internet.");
      }else{
        console.error("Error al buscar todos los pacientes: ", error.message); //mostrar error en la consola de depuracion

        resultList.innerHTML = "<li>No se encontraron pacientes</li>"; // Mensaje de error
      }
    }
  }
  */

  // Función para mostrar los resultados en la lista
  function mostrarResultados(resultados) {
    resultList.innerHTML = ""; // Limpia la lista de resultados anteriores

    const li = document.createElement("li"); //crear un nuevo elemento de la lista

    // Si no se encuentran resultados
    // Cambiar esto por algo más accesible
    if (resultados.length === 0) { 
      li.textContent = "No se encontraron pacientes";
      //resultList.innerHTML = "<li>No se encontraron pacientes</li>"; // Mensaje de error
    } else {
      //sacar informacion
      li.textContent = `${resultados.name} ${resultados.surname}`;
      li.dataset.id = resultados.id; //agrega un atributo personalizado con el ID
    }

    //li.setAttribute("role", "button");
    li.setAttribute("tabindex", "0");
    resultList.appendChild(li); //añadir el nuevo elemento a la lista
    li.focus();
  }


  // Función para mostrar los resultados en la lista de todos los pacientes
  function mostrarPacientes(resultados) {
    resultList.innerHTML = ""; // Limpia la lista de resultados anteriores

    // Si no se encuentran resultados
    if (resultados.length === 0) { 
      resultList.innerHTML = "<li>No se encontraron pacientes</li>"; // Mensaje de error
      return; // Sale de la función
    }

    var tabindex = 0;
    //sacar informacion
    resultados.forEach(paciente =>{
      const li = document.createElement("li"); //crear un nuevo elemento de la lista
      li.setAttribute("tabindex", tabindex.toString());
      tabindex += 1;
      li.setAttribute("role", "button");
      li.textContent = `${paciente.name} ${paciente.surname}`;
      li.dataset.id = paciente.id; //agrega un atributo personalizado con el ID
      resultList.appendChild(li); //añadir el nuevo elemento a la lista
    });

    resultList.querySelector('li:first-child').focus();
  }

  // Función para añadir un determinado número de pacientes a la lista
  /*
  function agregarPacientes(resultados) {
    // Si no se encuentran resultados desaparece el botón de cargar más
    if (resultados.length === 0 || resultados.length < patientsPerLoad) {
      listPatientsButton.classList.add("visually-hidden")
      return; // Sale de la función
    }

    //sacar informacion
    resultados.forEach(paciente =>{
      const li = document.createElement("li"); //crear un nuevo elemento de la lista
      li.textContent = `${paciente.name} ${paciente.surname}`;
      li.dataset.id = paciente.id; //agrega un atributo personalizado con el ID
      resultList.appendChild(li); //añadir el nuevo elemento a la lista
    });
  }
  */

  // Funcion para buscar pacientes por ID
  async function buscarPacienteID(id) {
    try{
      // Filtra los pacientes que coincidan con la búsqueda
      const url = obtenerURL(`patients/${id}`);
      
      const response = await fetch(url);

      //mirar si la respuesta fue exitosa o no
      if(!(response.ok)){
        if (response.status === 404){
          throw new Error("Error Not-Found. Codigo Error: 404")
        }else{
          throw new Error(`HTTP error; status returned ${response.status}`);
        }
      }

      //parseamos la respuesta a JSON
      const dataPatient = await response.json();

      // Muestra los resultados en la lista
      mostrarInformacionPaciente(dataPatient);

    } catch(error){
        //distinguir entre hay conexion o no con la BD
        if(error instanceof TypeError){
          // Errores de red o problemas de conexión
          console.error("Error de red o conexión:", error.message);
          mostrarError("Error: No se pudo conectar al servidor. Por favor, revisa tu conexión a Internet.");
        }else{
          console.error("Error al buscar pacientes por id: ", error.message); //mostrar error en la consola de depuracion
          mostrarError(error.message); //pantalla de error
        }
      }
  }


  function mostrarInformacionPaciente(paciente){

    //recibe la data que esta en JSON
    //sacamos donde va la info de paciente del html
    const patientName = document.getElementById("patient-name");
    const patientCode = document.getElementById("patient-code");
    const patientSurname = document.getElementById("patient-surname");

    //actualizamos la informacion del paciente
    patientName.textContent = paciente.name;
    patientSurname.textContent = paciente.surname;
    patientCode.textContent = paciente.code;

    //ponemos la pagina visualmente visible y ocultamos la otra
    document.getElementById("search-page").classList.add("media-hidden");
    document.getElementById("results-page").classList.add("visually-hidden");
    document.getElementById("patient-page").classList.remove("visually-hidden");
  }


  function mostrarError(mensaje) {
    // Oculta todas las pantallas activas
    document.getElementById("search-page").classList.add("visually-hidden");
    document.getElementById("patient-page").classList.add("visually-hidden");
    document.getElementById("medication-page").classList.add("visually-hidden");
  
    // Muestra la pantalla de error
    const errorPage = document.getElementById("error-page");
    errorPage.classList.remove("visually-hidden");
  
    // Actualiza el mensaje de error
    const errorMessage = document.getElementById("error-message");
    errorMessage.textContent = mensaje || "Ha ocurrido un error inesperado.";
  }
  
  function esconderListPatientsButton() {
    listPatientsButton.classList.add("visually-hidden")
    listPatientsButton.setAttribute("aria-expanded", true)
  }

  function mostrarListPatientsButton() {
    listPatientsButton.classList.remove("visually-hidden")
    listPatientsButton.setAttribute("aria-expanded", false)
  }

  // EVENTOS

  //Evento para detectar clicks en el boton de mostrar todos los pacientes
  listPatientsButton.addEventListener("click", () => {
    /*
    if (patientsIndex === 0)
      resultList.innerHTML = ""
    buscarNPacientes(patientsIndex,patientsPerLoad); //buscar todos los pacientes
    patientsIndex+=10;
    */
    // Esconder el botón
    esconderListPatientsButton()

    buscarTodosLosPacientes()
  });

  // Expresión regular para validar el formato xxx-xx-xxxx
  const regex = /^\d{3}-\d{2}-\d{4}$/;

  //evento para el boton de buscar paciente (lupa) para detectar el click y que busque pacientes
  searchButton.addEventListener("click", () => {

    const query = searchInput.value.trim(); // pillar el texto ingresado en el input

    //mirar si esta vacio
    if (!query) {
      // Si el query está vacío
      resultList.innerHTML = "<li>Error: El campo de búsqueda no puede estar vacío.</li>";
      return; // Sale de la función
    }


    // Comprobar si el query cumple con el formato
    if (!regex.test(query)) {
     resultList.innerHTML = "<li>Error: El formato del código no es válido. Debe ser xxx-xx-xxxx.</li>";
      return; // Sale de la función
    }

    // Marcar que hemos cerrado los pacientes cargados
    //patientsIndex = 0;
    mostrarListPatientsButton()

    buscarPacientes(query); // buscar el paciente introducido
  });

  //evento para el input para detectar si hace enter y buscar
  searchInput.addEventListener("keyup", (e) => {
    if (e.key === "Enter") { // Detecta si se presionó la tecla Enter
      const query = searchInput.value.trim(); // pilla el texto ingresado
      //mirar si esta vacio
      if (!query) {
        // Si el query está vacío
        resultList.innerHTML = "<li>Error: El campo de búsqueda no puede estar vacío.</li>";
        return; // Sale de la función
      }

      // Comprobar si el query cumple con el formato
      if (!regex.test(query)) {
      resultList.innerHTML = "<li>Error: El formato del código no es válido. Debe ser xxx-xx-xxxx.</li>";
      return; // Sale de la función
      }

      buscarPacientes(query); // busca el paciente introducido
    }
  });

  //EVENTO para detectar click en la lista de pacientes que sale
  resultList.addEventListener("click", (e) => {
    //verificamos que el click ocurriera en un li
    const elementoClickado = e.target;

    if(elementoClickado.tagName === "LI"){
      const pacienteID = elementoClickado.dataset.id; //scamos el id del paciente seleccionado
      pacienteIdSeguro = pacienteID;
      //hacer la pagina de informacion del paciente
      buscarPacienteID(pacienteID);
    }
  });

  resultList.addEventListener("keyup", (e) =>{
    if(e.key == "Enter"){
      const elementoClickado = e.target;

      if(elementoClickado.tagName === "LI"){
        const pacienteID = elementoClickado.dataset.id;
        pacienteIdSeguro = pacienteID;
        buscarPacienteID(pacienteID);
      }
    }
  });

  //evento para cerrar el informe
  const cerrarButton = document.getElementById("cerrar-informe-button");
  cerrarButton.addEventListener("click", () => {
    document.getElementById("results-page").classList.add("visually-hidden");
  })

  //evento para el boton de volver de la pantalla de error
  const backErrorButton = document.getElementById("back-button");
  backErrorButton.addEventListener("click", () => {
    //ocultar pantalla de error y mostrar la pagina de busqueda
    document.getElementById("error-page").classList.add("visually-hidden");
  });

  //Evento para el boton de volver atras de la pagina detalles de un paciente
    const backPatientButton = document.getElementById("back-button-patient-page");
    backPatientButton.addEventListener("click", () => {
      //ocultar pantalla de informacion de paciente y mostrar la pagina de busqueda
      document.getElementById("patient-page").classList.add("visually-hidden");
      document.getElementById("results-page").classList.add("visually-hidden");
      document.getElementById("search-page").classList.remove("media-hidden");
    });


    //evento para filtrar por fechas las intakes

    // Obtener todos los radio buttons
    const timeFilterRadios = document.querySelectorAll('input[name="time-filter"]');

    // Obtener los inputs de ultimos n dias y de start y end date
    const lastDaysInput = document.getElementById('last-days-input');
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');

    // Agregar un event listener a los radio buttons para detectar cambios
    timeFilterRadios.forEach(radio => {
      radio.addEventListener('change', function() {
        // primero deshabilitamos todos los campos
        lastDaysInput.disabled = true;
        startDateInput.disabled = true;
        endDateInput.disabled = true;

        // ahora vamos a verificar que se ha seleccionado para habilitar el campo correspondiente
        switch (this.value) {
          case 'last-month':
            // No es necesario ningun input, solo hay que buscar por el ultimo mes
            break;

          case 'last-n-days':
            lastDaysInput.disabled = false;  // habilitar el input de last n days 
            break;

          case 'date-range':
            startDateInput.disabled = false; // habilitar el input de fecha inicio
            endDateInput.disabled = false;   // habilitar el input de fecha final
            break;
        }
      });
    });




    //ahora toca que cuando se pulse el boton de buscar miremos los valores del filtro correspondiente y llamemmos a la funcion para buscar

    const filtrarButton = document.getElementById("apply-filter-button");

    filtrarButton.addEventListener("click", () => {
      const patientID = pacienteIdSeguro;
      document.getElementById("results-page").classList.remove("visually-hidden");
      filtrarBusqueda(patientID);

      /*
      const timeFilter = document.querySelector('input[name="time-filter"]:checked').value;

      let filterValue = "";
      if (timeFilter === "last-month") {
        // Obtener los datos del último mes (calculado automáticamente)
        filterValue = "last-month";
      } else if (timeFilter === "last-n-days") {
        const lastDays = lastDaysInput.value;  // Obtener el número de días
        if (!lastDays) {
          alert("Por favor, ingrese un número válido de días.");
          return;
        }
        filterValue = `last-${lastDays}-days`;
      } else if (timeFilter === "date-range") {
        const startDate = startDateInput.value; // Obtener la fecha de inicio
        const endDate = endDateInput.value;     // Obtener la fecha de fin
        if (!startDate || !endDate) {
          alert("Por favor, ingrese un intervalo de fechas válido.");
          return;
        }
        filterValue = `date-range:${startDate}:${endDate}`;
      }
      //const patientID = intakesButton.dataset.patientId;

      // funcion de bsuqueda de intakes
      //filtrarBusqueda(patientID, filterValue);*/
    });

    function formatearTiempo(hora, minuto) {
      return `${hora < 10 ? `0` : ``}${hora}:${minuto < 10 ? `0` : ``}${minuto}`
    }

    async function mostrarInfoMedicamento(responsePosologies, responseIntakes, medicamento, filterValue) {
      try {
        // Obtener datos de las respuestas JSON
        const posologies = await responsePosologies.json();
        const intakes = await responseIntakes.json();
    
        // Crear contenedor principal para el medicamento
        const container = document.getElementById('medications-container');
        const medicationSection = document.createElement('div'); // Div para el medicamento específico
        medicationSection.setAttribute("aria-live", "assertive")
        medicationSection.classList.add('medication-section');
        
        // Crear información básica del medicamento

        medicationSection.innerHTML = `
        <section class="medication-info" aria-live="assertive">
          <h3>Medicamento: <span class="medication-name">${medicamento.name}</span></h3>
          <dl>
            <dt>Dosis:</dt>
            <dd>${medicamento.dosage}</dd>
            <dt>Duración del tratamiento:</dt>
            <dd>${medicamento.treatment_duration}</dd>
            <dt>Fecha Comienzo Tratamiento:</dt>
            <dd>${medicamento.start_date}</dd>
          </dl
        </section>
        <hr class="separator">
      `;
    
        // Crear lista para Posologías
        const posologySection = document.createElement('section');
        posologySection.classList.add('posology-section');
        posologySection.setAttribute("aria-live","assertive");
        posologySection.innerHTML = `<h4>Posologías</h4>`;
        const posologiesList = document.createElement('ul');
        posologiesList.classList.add('posologies-list');
    
        // Verificar si hay posologías
        if (posologies.length === 0) {
          const li = document.createElement("li");
          li.textContent = "This medication has no posologies.";
          posologiesList.appendChild(li);
        } else {
          posologies.forEach(posology => {
            const li = document.createElement("li");
            li.textContent = formatearTiempo(posology.hour, posology.minute);
            posologiesList.appendChild(li);
          });
        }
        posologySection.appendChild(posologiesList);
    
        // Crear contenedor para las Tomas
        const intakeSection = document.createElement('section');
        intakeSection.setAttribute("aria-live", "assertive");
        intakeSection.classList.add('intakes-section');
        intakeSection.innerHTML = `<h4>Tomas</h4>`;
    
        // Crear lista de Intakes con clase scrollable
        const intakesContainer = document.createElement('div'); // Contenedor para las tomas
        intakesContainer.setAttribute("aria-live","assertive");
        intakesContainer.classList.add('intakes-container'); // Clase para manejar el scroll
        intakesContainer.classList.add('lista-intakes'); // Clase para manejar el scroll
        const intakesList = document.createElement('ul');
        intakesList.classList.add('intakes-list', 'scrollable'); // Clase para scroll
        
        
        
        let intakesFiltrados = [];

            switch (true) {
              case filterValue === "last-month":
                const lastMonthDate = new Date();
                lastMonthDate.setMonth(lastMonthDate.getMonth() - 1); // Fecha hace 1 mes a la actual 
                intakesFiltrados = intakes.filter(intake => new Date(intake.date) > lastMonthDate);
                break;

              case /^last-\d+-days$/.test(filterValue):
                const daysAgo = parseInt(filterValue.match(/^last-(\d+)-days$/)[1]); //sacamos el numero que esta entre el last y el days
                const daysAgoDate = new Date(); //fecha actual
                daysAgoDate.setDate(daysAgoDate.getDate() - daysAgo); // Fecha hace N días
                intakesFiltrados = intakes.filter(intake => new Date(intake.date) > daysAgoDate);
                break;

              case filterValue.startsWith("date-range:"):
                const [, startDate, endDate] = filterValue.split(":"); //sacar tanto la fecha inicial como final
                const startDateObj = new Date(startDate);
                const endDateObj = new Date(endDate);
                //filtrar intakes que la fecha sea mayor o igual a cuando empieza y menor o igual al fin
                intakesFiltrados = intakes.filter(intake => {
                  const intakeDate = new Date(intake.date);
                  return (intakeDate >= startDateObj) && (intakeDate <= endDateObj);
                });
                break;

                default:
                  console.error("Valor no reconocido para filterValue:", filterValue);
                  break;
            }
            
        intakesFiltrados.sort((a, b) => {
          const dateA = new Date(a.date.getDate);
          const dateB = new Date(b.date.getDate);
          return dateA - dateB; // Ascendente: más antiguo a más reciente
        });


        // Verificar si hay tomas
        if (intakesFiltrados.length === 0) {
          return
        } else {
          posologies.forEach (posologie => {
            intakesFiltrados.forEach(intake => {
              const li = document.createElement("li");

              const intakeDate = new Date(intake.date);
              const intakeHour = intakeDate.getHours();
              const intakeMinute = intakeDate.getMinutes();

              const posologieHour = posologie.hour;
              const posologieMinute = posologie.minute;

              if (posologieHour === intakeHour || posologieHour === intakeHour+1 || posologieHour === intakeHour-1){
                const timeDifference = Math.abs ((intakeHour - posologieHour) * 60 + (intakeMinute - posologieMinute));

                const emoji = timeDifference > 30 ? "❌" : "✅";

                li.textContent = `${emoji}\t${intakeDate.toLocaleDateString()} ${formatearTiempo(intakeDate.getHours(), intakeDate.getMinutes())}`;
                intakesList.appendChild(li);
              }
            });
          });
        }


        // Agregar lista de tomas al contenedor y contenedor a la sección
        intakesContainer.appendChild(intakesList);
        intakeSection.appendChild(intakesContainer);
    
        // Agregar todas las secciones al contenedor principal
        medicationSection.appendChild(posologySection);
        medicationSection.appendChild(intakeSection);
        container.appendChild(medicationSection);
        
    
      } catch (error) {
        console.error("Error mostrando información del medicamento:", error);
      }
    }
    
    

        // Funcion para buscar medicamentos por ID del paciente y del medicamento
        async function buscarInfoMedicamento(patientID, medicamentoID, medicamento, filterValue) {
          try{
            
            const urlPosologias = obtenerURL (`patients/${patientID}/medications/${medicamentoID}/posologies`);
            const urlTomas = obtenerURL (`patients/${patientID}/medications/${medicamentoID}/intakes`);

            const responsePosologias = await fetch(urlPosologias);
            const responseTomas = await fetch(urlTomas);

            if(!(responsePosologias.ok) || !(responseTomas.ok)){
              if (responsePosologias.status === 404 || responseTomas.status === 404){
                throw new Error("Error Not-Found. Codigo Error: 404")
              }else{
                if(!(responsePosologias.ok)){
                  throw new Error(`HTTP error; status returned ${responsePosologias.status}`);
                }else{
                  throw new Error(`HTTP error; status returned ${responseTomas.status}`);
                }
              }
            }

            mostrarInfoMedicamento(responsePosologias, responseTomas, medicamento, filterValue);
      
          } catch(error){
              //distinguir entre hay conexion o no con la BD
              if(error instanceof TypeError){
                // Errores de red o problemas de conexión
                console.error("Error de red o conexión:", error.message);
                mostrarError("Error: No se pudo conectar al servidor. Por favor, revisa tu conexión a Internet.");
              }else{
                console.error("Error al buscar informacion medicamento por id: ", error.message); //mostrar error en la consola de depuracion
                mostrarError(error.message); //pantalla de error
              }
            }
        }



        // Funcion para buscar intakes y posologias por ID del paciente y del medicamento para ver desviaciones
        async function filtrarBusqueda(patientID){
          const container = document.getElementById('medications-container');
          const timeFilter = document.querySelector('input[name="time-filter"]:checked').value;


          container.innerHTML = '';
          try{
            const urlMedicamentos = obtenerURL(`patients/${patientID}/medications`);

            const responseMedicamentos = await fetch(urlMedicamentos);

            if(!(responseMedicamentos.ok)){
              if (responseMedicamentos.status === 404){
                throw new Error("Error Not-Found. Codigo Error: 404")
              }else{
                throw new Error(`HTTP error; status returned ${responseMedicamentos.status}`);
              }
            }

            const medicamentos = await responseMedicamentos.json();

            let filterValue = "";
            
            if (timeFilter === "last-month") {
            // Obtener los datos del último mes (calculado automáticamente)
              filterValue = "last-month";
            } else if (timeFilter === "last-n-days") {
              const lastDays = lastDaysInput.value;  // Obtener el número de días
                if (!lastDays) {
                  alert("Por favor, ingrese un número válido de días.");
                  return;
                }
              filterValue = `last-${lastDays}-days`;
            } else if (timeFilter === "date-range") {
              const startDate = startDateInput.value; // Obtener la fecha de inicio
              const endDate = endDateInput.value;     // Obtener la fecha de fin
              if (!startDate || !endDate) {
                alert("Por favor, ingrese un intervalo de fechas válido.");
                return;
              }
              filterValue = `date-range:${startDate}:${endDate}`;
            }
            
            if(medicamentos.length == 0){
              const li = document.createElement("li");
              li.textContent = "The patient has no medications";
              container.appendChild(li);
            }else{
              //si no es que hay medicamentos, hay que añadir uno a uno
              medicamentos.forEach(medicamento => { 
                buscarInfoMedicamento(patientID,medicamento.id, medicamento, filterValue);
              });
            }
            
          } catch(error){
              //distinguir entre hay conexion o no con la BD
              if(error instanceof TypeError){
                // Errores de red o problemas de conexión
                console.error("Error de red o conexión:", error.message);
                mostrarError("Error: No se pudo conectar al servidor. Por favor, revisa tu conexión a Internet.");
              }else{
                console.error("Error al buscar informacion intakes por fecha: ", error.message); //mostrar error en la consola de depuracion
                mostrarError(error.message); //pantalla de error
              }
            }
        }
}
