import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart';
import 'package:provider/provider.dart';
import 'model.dart';
import 'package:timezone/data/latest.dart'
    as tz; //paquete para las zonas horarias
import 'package:timezone/timezone.dart' as tz; //tambien para la hora

/*
Future<String> namePatient(int id) {
  return PatientModel().getPatientName(id);
}
*/
/*
Future<int> getIdPatientFromText(String patientIdText) async {
  // Llamamos al modelo para obtener el ID del paciente de la base de datos
  try {
    // Esperamos el resultado del modelo, que es asincrónico
    int patientId = await PatientModel().getIdPatient(patientIdText);

    // Aquí podemos manejar cualquier validación adicional si es necesario
    if (patientId == -1) {
      throw Exception("Patient not found.");
    }

    // Devolvemos el patientId recibido
    return patientId;
  } catch (e) {
    // Si ocurre algún error (por ejemplo, error en la conexión, paciente no encontrado)
    throw Exception("Error occurred while fetching the patient ID: $e");
  }
}
*/

void main() {
  // Inicializa las herramientas de zona horaria
  tz.initializeTimeZones();
  tz.setLocalLocation(
      tz.getLocation('Europe/Madrid')); // Ajusta a tu zona horaria

  runApp(
    MultiProvider(
      providers: [
        // no se escucha en ningun momento pero se usa
        ChangeNotifierProvider(create: (context) => PatientModel()),
        ChangeNotifierProvider(create: (context) => MedicineModel()),
        ChangeNotifierProvider(create: (context) => PosologieModel()),
        ChangeNotifierProvider(create: (context) => IntakeModel()),
      ],
      child: const MainApp(),
    ),
  );
}

class MainApp extends StatelessWidget {
  const MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: LoginPage(),
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color.fromARGB(255, 112, 145, 190),
          brightness: Brightness.light,
        ),
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
    );
  }
}

class LoginPage extends StatelessWidget {
  final TextEditingController idController = TextEditingController();
  // Configuramos el TextInputFormatter para crear nuestro propio teclado con los caracteres que queramos
  final TextInputFormatter _idFormatter =
      FilteringTextInputFormatter.allow(RegExp(r'[\d-]'));

  @override
  Widget build(BuildContext context) {
    double textSize;
    double screenWidth =
        MediaQuery.of(context).size.width; //sacar el ancho de pantalla
    double screenHeight =
        MediaQuery.of(context).size.height; //sacar la altura de la pantalla
    double buttonHeight; //para ajustar tamaños en el reloj
    double padding; //para ajustar tamaños reloj vs movil
    //si el ancho de pantalla es menor a 300 es que es un reloj; si no es un movil pondremos tamaño letra del movil a 20 y la del reloj a 12
    if (screenWidth < 300) {
      textSize = 9.0;
      buttonHeight = 20.0; //boton mas pequeño q en un movil
      padding = 8.0; //padding mas pequeño q en el movil
    } else {
      textSize = 20.0;
      buttonHeight = 50.0;
      padding = 16.0;
    }
    return Scaffold(
      appBar: AppBar(
        title: Text(
          "Login",
          style: TextStyle(fontSize: textSize),
          textAlign: TextAlign.center,
        ), //alinear el texto centrado en el widget
        centerTitle: true, //aseguramos el centrado en el AppBar
      ),
      body: Padding(
        padding: EdgeInsets.all(padding),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              key: const Key('patientCodeTextField'),
              controller: idController,
              decoration: InputDecoration(
                  labelText: "Enter your patient ID",
                  labelStyle: TextStyle(fontSize: textSize)),
              keyboardType: TextInputType
                  .text, //teclado con texto para permitir signos - (por defecto en el smartwatch no sale en el numerico
              style: TextStyle(fontSize: textSize), //ajuste dinamico del texto
              inputFormatters: [
                _idFormatter
              ], // Usamos el TextInputFormatter personalizado
            ),
            SizedBox(height: padding), //espaciado variable con el padding
            SizedBox(
              height: buttonHeight, //altura dinamica para el boton
              child: ElevatedButton(
                key: const Key('loginElevatedButton'),
                onPressed: () async {
                  if (idController.text.isNotEmpty) {
                    String patientCode = idController.text;
                    final idRegex =
                        RegExp(r'^\d{3}-\d{2}-\d{4}$'); // Formato "###-##-####"

                    if (idRegex.hasMatch(patientCode)) {
                      try {
                        // Llamamos a la función asincrónica para obtener el patientId
                        // Está prohibido usar context.read en el propio build pero si dentro de eventos
                        int patientId = await context
                            .read<PatientModel>()
                            .getPatientIdWithCode(patientCode);

                        // Si el ID es válido, navega a la página correspondiente
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => MedicineListPage(
                              patientId: patientId,
                              textSize: textSize,
                              padding: padding,
                            ),
                          ),
                        );
                      } catch (e) {
                        // Si ocurre un error, mostramos el mensaje de error
                        ScaffoldMessenger.of(context).removeCurrentSnackBar();
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            duration: const Duration(seconds: 3),
                            content: Text(
                              "Error: ${e.toString()}",
                              style: TextStyle(fontSize: textSize - 3),
                              textAlign: TextAlign.center,
                            ),
                          ),
                        );
                      }
                    } else {
                      // Si el ID no tiene el formato correcto
                      ScaffoldMessenger.of(context).removeCurrentSnackBar();
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          duration: const Duration(seconds: 3),
                          content: Text(
                            "ID invalid. Format ###-##-####.",
                            style: TextStyle(fontSize: textSize - 3),
                            textAlign: TextAlign.center,
                          ),
                        ),
                      );
                    }
                  } else {
                    // Si el campo está vacío
                    ScaffoldMessenger.of(context).removeCurrentSnackBar();
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        duration: const Duration(seconds: 3),
                        content: Text(
                          "Please, ID cannot be empty.",
                          style: TextStyle(fontSize: textSize - 3),
                          textAlign: TextAlign.center,
                        ),
                      ),
                    );
                  }
                },
                child: Text(
                  "Login",
                  style: TextStyle(fontSize: textSize),
                  textAlign: TextAlign.center,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class MedicineListPage extends StatefulWidget {
  final int patientId;
  final double textSize;
  final double padding;

  const MedicineListPage(
      {required this.patientId,
      required this.textSize,
      required this.padding,
      super.key});
  @override
  State<StatefulWidget> createState() => _MedicineListPageState();
}

class _MedicineListPageState extends State<MedicineListPage> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context
          .read<MedicineModel>()
          .loadMedicines(widget.patientId); //cargar las medicinas del paciente
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: FutureBuilder<String>(
          future: context.read<PatientModel>().getPatientName(
              widget.patientId), // Llama al Future que obtiene el nombre
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              // Mientras se carga el Future
              return Text(
                "Loading...",
                style: TextStyle(fontSize: widget.textSize),
              );
            } else if (snapshot.hasError) {
              // Si ocurre un error
              return Text(
                "Error: ${snapshot.error}",
                style: TextStyle(fontSize: widget.textSize),
              );
            } else {
              // Si el Future se resuelve correctamente
              return Text(
                "${snapshot.data} (${widget.patientId})'s Medicines",
                style: TextStyle(fontSize: widget.textSize),
              );
            }
          },
        ),
        backgroundColor: Theme.of(context).primaryColor,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            context.watch<MedicineModel>().errorMessage !=
                    null //por si hay algun mensaje de error mostrarlo
                ? Padding(
                    padding: EdgeInsets.all(widget.padding),
                    child: ErrorMessage(
                      message: context.watch<MedicineModel>().errorMessage!,
                      textSize: widget.textSize,
                      padding: widget.padding,
                    ),
                  )
                : ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: context.watch<MedicineModel>().medicines.length,
                    itemBuilder: (context, index) {
                      return Padding(
                          padding: EdgeInsets.all(widget.padding),
                          child: MedicineTitle(
                            medicine:
                                context.watch<MedicineModel>().medicines[index],
                            textSize: widget.textSize,
                            padding: widget.padding,
                          ));
                    },
                  ),
            if (context.watch<MedicineModel>().isLoading)
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: CircularProgressIndicator(),
              ),
            context.watch<MedicineModel>().hasNoMedicines
                ? Padding(
                    padding: EdgeInsets.all(widget.padding),
                    child: Center(
                      child: Text(
                        "No medications found",
                        style: TextStyle(fontSize: widget.textSize),
                      ),
                    ),
                  )
                : Container(),
          ],
        ),
      ),
    );
  }
}

class MedicineTitle extends StatelessWidget {
  const MedicineTitle({
    super.key,
    required this.medicine,
    required this.textSize,
    required this.padding,
  });

  final Medicine medicine;
  final double textSize;
  final double padding;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(padding - 3),
      child: Container(
        decoration: BoxDecoration(
          border: Border.all(
            color: Colors.grey, // Color del borde
            width: 1.0, // Ancho del borde
          ),
          borderRadius: BorderRadius.circular(10.0), // Bordes redondeados
          color: Colors.white, // Fondo (opcional)
        ),
        padding: EdgeInsets.all(padding - 8.0), // Espaciado interno
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Expanded(
              child: InkWell(
                key: const Key("toMedicationDetailInkWell"),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      medicine.name,
                      style: Theme.of(context)
                          .textTheme
                          .titleLarge
                          ?.copyWith(fontSize: textSize),
                      overflow:
                          TextOverflow.ellipsis, // Para evitar desbordamiento
                    ),
                    Text(
                      medicine.dosage,
                      style: Theme.of(context)
                          .textTheme
                          .titleMedium
                          ?.copyWith(fontSize: textSize),
                    ),
                    Text(
                      medicine.start_date,
                      style: Theme.of(context)
                          .textTheme
                          .bodyMedium
                          ?.copyWith(fontSize: textSize),
                    ),
                    Text(
                      medicine.treatment_duration,
                      style: Theme.of(context)
                          .textTheme
                          .bodyMedium
                          ?.copyWith(fontSize: textSize),
                    ),
                  ],
                ),
                onTap: () => Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) =>
                        MedicineDetailsPage(medicine, textSize, padding),
                  ),
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}

class MedicineDetailsPage extends StatefulWidget {
  final Medicine medicine;
  final double textSize;
  final double padding;
  const MedicineDetailsPage(this.medicine, this.textSize, this.padding,
      {super.key});

  @override
  State<StatefulWidget> createState() => _MedicineDetailsPage();
}

class _MedicineDetailsPage extends State<MedicineDetailsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          "Medication details",
          style: TextStyle(fontSize: widget.textSize),
        ),
        backgroundColor: Theme.of(context).primaryColor,
        foregroundColor: Colors.white,
      ),
      body: FutureBuilder(
          future: context
              .read<MedicineModel>()
              .getMedicineData(widget.medicine.patient_id, widget.medicine.id),
          builder: (context, snapshot) {
            if (snapshot.hasError) {
              return ErrorMessage(
                message: snapshot.error.toString(),
                textSize: widget.textSize,
                padding: widget.padding,
              );
            } else {
              if (!snapshot.hasData) {
                return Center(child: CircularProgressIndicator());
              } else {
                return Padding(
                  padding: EdgeInsets.all(widget.padding),
                  child: SingleChildScrollView(
                    child: Column(
                      children: [
                        MedicineDetailsTile(
                          title: "Name",
                          content: snapshot.data!.name,
                          textSize: widget.textSize,
                          padding: widget.padding,
                        ),
                        MedicineDetailsTile(
                          title: "Dosage",
                          content: snapshot.data!.dosage,
                          textSize: widget.textSize,
                          padding: widget.padding,
                        ),
                        MedicineDetailsTile(
                          title: "Start Date",
                          content: snapshot.data!.start_date,
                          textSize: widget.textSize,
                          padding: widget.padding,
                        ),
                        MedicineDetailsTile(
                          title: "Treatment Duration",
                          content: snapshot.data!.treatment_duration,
                          textSize: widget.textSize,
                          padding: widget.padding,
                        ),
                        Center(
                            child: Row(
                          mainAxisAlignment:
                              MainAxisAlignment.center, //centrar los botones
                          children: [
                            ElevatedButton(
                              key: const Key("toPosologiesListElevatedButton"),
                              onPressed: () {
                                //ir a la lista de posologias
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => PosologiesListPage(
                                      patientId: widget.medicine.patient_id,
                                      medicationId: widget.medicine.id,
                                      textSize: widget.textSize,
                                      padding: widget.padding,
                                    ),
                                  ),
                                );
                              },
                              child: Text(
                                "Posologies",
                                style: TextStyle(fontSize: widget.textSize - 2),
                              ),
                            ),
                            SizedBox(
                              width: 8,
                            ), //espacio entre os botones
                            ElevatedButton(
                              key: const Key("toIntakesListElevatedButton"),
                              onPressed: () {
                                //ir a la lista de intakes
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => IntakesListPage(
                                      patientId: widget.medicine.patient_id,
                                      medicationId: widget.medicine.id,
                                      padding: widget.padding,
                                      textSize: widget.textSize,
                                    ),
                                  ),
                                );
                              },
                              child: Text(
                                "Intakes",
                                style: TextStyle(fontSize: widget.textSize - 2),
                              ),
                            )
                          ],
                        ))
                      ],
                    ),
                  ),
                );
              }
            }
          }),
    );
  }
}

class MedicineDetailsTile extends StatelessWidget {
  const MedicineDetailsTile(
      {super.key,
      required this.title,
      required this.content,
      required this.textSize,
      required this.padding});

  final String title;
  final String content;
  final double textSize;
  final double padding;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.only(bottom: padding),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center, //alineado al centro
        children: [
          Text(
            title,
            style: TextStyle(fontSize: textSize),
            overflow: TextOverflow.ellipsis,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center, //alineado al centro
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Flexible(
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Text(
                    content,
                    style: Theme.of(context)
                        .textTheme
                        .headlineSmall
                        ?.copyWith(fontSize: textSize),
                    overflow: TextOverflow.ellipsis,
                  ),
                  //sin boton de editar
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class PosologiesListPage extends StatefulWidget {
  final int patientId;
  final int medicationId;
  final double textSize;
  final double padding;

  const PosologiesListPage(
      {required this.patientId,
      required this.medicationId,
      required this.textSize,
      required this.padding,
      super.key});

  @override
  State<StatefulWidget> createState() => _PosologiesListPageState();
}

class _PosologiesListPageState extends State<PosologiesListPage> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<PosologieModel>().loadPosologies(widget.patientId,
          widget.medicationId); //cargar las medicinas del paciente
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: FutureBuilder<String>(
          future: context
              .read<PatientModel>()
              .getPatientName(widget.patientId), // Llama al Future aquí
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              // Mientras se espera, muestra un texto de "Loading..."
              return Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  "Loading...",
                  style: TextStyle(fontSize: widget.textSize - 4),
                ),
              );
            } else if (snapshot.hasError) {
              // Si hay un error, muestra un mensaje de error
              return Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  "Error: ${snapshot.error}",
                  style: TextStyle(fontSize: widget.textSize - 4),
                ),
              );
            } else {
              // Una vez cargado el nombre, muestra el título completo
              return Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  "${snapshot.data} (${widget.patientId})'s Posologies for Medication ${widget.medicationId}",
                  style: TextStyle(fontSize: widget.textSize - 3),
                ),
              );
            }
          },
        ),
        backgroundColor: Theme.of(context).primaryColor,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            context.watch<PosologieModel>().errorMessage != null
                ? ErrorMessage(
                    message: context.watch<PosologieModel>().errorMessage!,
                    textSize: widget.textSize,
                    padding: widget.padding,
                  )
                : ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount:
                        context.watch<PosologieModel>().posologies.length,
                    itemBuilder: (context, index) {
                      return PosologieTitle(
                        posologie:
                            context.watch<PosologieModel>().posologies[index],
                        textSize: widget.textSize,
                        padding: widget.padding,
                      );
                    },
                  ),
            if (context.watch<PosologieModel>().isLoading)
              Padding(
                padding: EdgeInsets.all(widget.padding),
                child: CircularProgressIndicator(),
              ),
            context.watch<PosologieModel>().hasNoPosologies
                ? Center(
                    child: Text(
                    "No posologies found",
                    style: TextStyle(fontSize: widget.textSize),
                  ))
                : Container(),
          ],
        ),
      ),
    );
  }
}

class PosologieTitle extends StatelessWidget {
  const PosologieTitle({
    super.key,
    required this.posologie,
    required this.textSize,
    required this.padding,
  });

  final Posologie posologie;
  final double textSize;
  final double padding;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(padding),
      child: Center(
        //centrar el contenido
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center, //centrar
          children: [
            InkWell(
              child: Row(
                crossAxisAlignment: CrossAxisAlignment
                    .center, // Centra los textos verticalmente
                children: [
                  Row(
                    children: [
                      Text(
                        "Hour: ",
                        style: Theme.of(context).textTheme.bodyMedium!.copyWith(
                              fontWeight: FontWeight.bold,
                              fontSize: textSize,
                            ),
                      ),
                      Text(
                        posologie.hour.toString(),
                        style:
                            Theme.of(context).textTheme.titleMedium!.copyWith(
                                  fontStyle: FontStyle.italic,
                                  fontSize: textSize,
                                ),
                      ),
                    ],
                  ),
                  const SizedBox(width: 16), // Espacio entre "Hora" y "Minuto"
                  Row(
                    children: [
                      Text(
                        "Minute: ",
                        style: Theme.of(context).textTheme.bodyMedium!.copyWith(
                              fontWeight: FontWeight.bold,
                              fontSize: textSize,
                            ),
                      ),
                      Text(
                        posologie.minute.toString(),
                        style: Theme.of(context).textTheme.bodyMedium!.copyWith(
                              fontStyle: FontStyle.italic,
                              fontSize: textSize,
                            ),
                      ),
                    ],
                  ),
                ],
              ),
              /*onTap: () => Navigator.push(
                  // ir a página de detalles de medicamento
                  context,
                  MaterialPageRoute(
                    builder: (context) => irATomas,
                  ),
                ),*/
            ),
          ],
        ),
      ),
    );
  }
}

class IntakesListPage extends StatefulWidget {
  final int patientId;
  final int medicationId;
  final double padding;
  final double textSize;

  const IntakesListPage(
      {required this.patientId,
      required this.medicationId,
      required this.padding,
      required this.textSize,
      super.key});

  @override
  State<StatefulWidget> createState() => _IntakesListPageState();
}

class _IntakesListPageState extends State<IntakesListPage> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<IntakeModel>().loadIntakes(
          widget.patientId, widget.medicationId); //cargar los intakes
    });
  }

  @override
  Widget build(BuildContext context) {
    final screenSize = MediaQuery.of(context).size; //sacar dimensiones pantalla
    final isSmallScreen =
        screenSize.width < 300; //si el ancho de la pantalla es menor a 300
    final buttonSize = isSmallScreen
        ? 26.0
        : 58.0; //tamaño del boton si es o no pantalla pequeña
    return Scaffold(
      appBar: AppBar(
        title: FutureBuilder<String>(
          future: context
              .read<PatientModel>()
              .getPatientName(widget.patientId), // Llama al Future aquí
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return Text(
                "Loading...",
                style: TextStyle(fontSize: widget.textSize - 3),
              );
            } else if (snapshot.hasError) {
              return Text(
                "Error: ${snapshot.error}",
                style: TextStyle(fontSize: widget.textSize - 3),
              );
            } else {
              return Text(
                "${snapshot.data} (${widget.patientId})'s Intakes for Medication ${widget.medicationId}",
                style: TextStyle(fontSize: widget.textSize - 2),
              );
            }
          },
        ),
        backgroundColor: Theme.of(context).primaryColor,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            context.watch<IntakeModel>().errorMessage != null
                ? ErrorMessage(
                    message: context.watch<IntakeModel>().errorMessage!,
                    textSize: widget.textSize,
                    padding: widget.padding,
                  )
                : ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: context.watch<IntakeModel>().intakes.length,
                    itemBuilder: (context, index) {
                      return IntakeTitle(
                        intake: context.watch<IntakeModel>().intakes[index],
                        textSize: widget.textSize,
                        padding: widget.padding,
                      );
                    },
                  ),
            if (context.watch<IntakeModel>().isLoading)
              Padding(
                padding: EdgeInsets.all(widget.padding),
                child: CircularProgressIndicator(),
              ),
            context.watch<IntakeModel>().hasNoIntakes
                ? Center(
                    child: Text(
                    "No intakes found",
                    style: TextStyle(fontSize: widget.textSize),
                  ))
                : Container(),
          ],
        ),
      ),
      floatingActionButtonLocation:
          FloatingActionButtonLocation.centerFloat, //centrar el boton flotante
      floatingActionButton: SizedBox(
        width: buttonSize, //ancho del boton
        height: buttonSize, //alto del boton
        child: FloatingActionButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => IntakeAddPage(
                  patientId: widget.patientId,
                  medicationId: widget.medicationId,
                  textSize: widget.textSize,
                  padding: widget.padding,
                ),
              ),
            );
          },
          tooltip: 'Add Intake',
          child: const Icon(Icons.add),
          //ajustar tamaño boton segun la pantalla (movil o reloj)
          backgroundColor: Theme.of(context)
              .primaryColor, //color del fondo que lo obtenga color prinicpal de la app
        ),
      ),
    );
  }
}

class IntakeTitle extends StatelessWidget {
  const IntakeTitle({
    super.key,
    required this.intake,
    required this.textSize,
    required this.padding,
  });

  final Intake intake;
  final double textSize;
  final double padding;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(padding),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          InkWell(
            child: Row(
              crossAxisAlignment:
                  CrossAxisAlignment.center, // Centra los textos verticalmente
              children: [
                Row(
                  children: [
                    /*Text(
                      "Date: ",
                      style: Theme.of(context).textTheme.bodyMedium!.copyWith(
                            fontWeight: FontWeight.bold,
                            fontSize: 18, // Tamaño más grande para "Hora"
                          ),
                    ),*/
                    Text(
                      intake.date,
                      style: Theme.of(context).textTheme.titleMedium!.copyWith(
                            fontSize: textSize,
                          ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class IntakeAddPage extends StatefulWidget {
  final int patientId;
  final int medicationId;
  final double textSize;
  final double padding;
  DateTime selectedDate =
      DateTime.now().copyWith(second: 0, millisecond: 0, microsecond: 0);

  // no puede ser const porque no siempre que se crea es igual
  IntakeAddPage(
      {required this.patientId,
      required this.medicationId,
      required this.textSize,
      required this.padding,
      super.key});

  @override
  State<StatefulWidget> createState() => _IntakeAddPage();
}

class _IntakeAddPage extends State<IntakeAddPage> {
  @override
  void initState() {
    super.initState();
    /*WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<IntakeModel>().loadIntakes(
          widget.patientId, widget.medicationId); //cargar los intakes
    });*/
  }

  void _selectDate() async {
    final DateTime? picked = await showDatePicker(
        context: context,
        initialDate: widget.selectedDate,
        firstDate: DateTime(DateTime.now().year - 1),
        lastDate: widget.selectedDate);
    if (picked != null && picked != widget.selectedDate) {
      // Como es un estado local de esta pantalla, considero que usar setState() es lo apropiado
      setState(() {
        widget.selectedDate = widget.selectedDate
            .copyWith(year: picked.year, month: picked.month, day: picked.day);
      });
    }
  }

  void _selectTime() async {
    final TimeOfDay? picked = await showTimePicker(
        context: context,
        initialTime: TimeOfDay(
            hour: widget.selectedDate.hour,
            minute: widget.selectedDate.minute));
    if (picked != null &&
        picked !=
            TimeOfDay(
                hour: widget.selectedDate.hour,
                minute: widget.selectedDate.minute)) {
      setState(() {
        widget.selectedDate = widget.selectedDate
            .copyWith(hour: picked.hour, minute: picked.minute);
      });
    }
  }

  // Selector de fecha para smartwatch (Dialog de pantalla completa)
  void _selectDateSmartwatch() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return Dialog(
          child: ListView.builder(
            itemCount: 31,
            itemBuilder: (context, index) {
              final date = DateTime.now().add(Duration(days: index));
              return ListTile(
                title: Text("${date.toLocal()}".split(' ')[0]),
                onTap: () {
                  setState(() {
                    widget.selectedDate = widget.selectedDate.copyWith(
                      year: date.year,
                      month: date.month,
                      day: date.day,
                    );
                  });
                  Navigator.pop(context);
                },
              );
            },
          ),
        );
      },
    );
  }

  // Selector de hora con minutos para smartwatch (Dialog de pantalla completa)
  void _selectTimeSmartwatch() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return Dialog(
          child: Column(
            children: [
              Expanded(
                child: ListView.builder(
                  itemCount: 24,
                  itemBuilder: (context, hour) {
                    return ListTile(
                      title: Text("$hour:00"),
                      onTap: () {
                        showDialog(
                          context: context,
                          builder: (BuildContext context) {
                            return Dialog(
                              child: ListView.builder(
                                itemCount: 60,
                                itemBuilder: (context, minute) {
                                  return ListTile(
                                    title: Text(
                                        "$hour:${minute.toString().padLeft(2, '0')}"),
                                    onTap: () {
                                      setState(() {
                                        widget.selectedDate =
                                            widget.selectedDate.copyWith(
                                          hour: hour,
                                          minute: minute,
                                        );
                                      });
                                      Navigator.pop(
                                          context); // Cierra el selector de minutos
                                      Navigator.pop(
                                          context); // Cierra el selector de horas
                                    },
                                  );
                                },
                              ),
                            );
                          },
                        );
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    // Detectar si estamos en un smartwatch o un móvil
    final isSmartwatch = MediaQuery.of(context).size.shortestSide < 300;
    return Scaffold(
      appBar: AppBar(
        title: FutureBuilder<String>(
          future: context
              .read<PatientModel>()
              .getPatientName(widget.patientId), // Llama al Future aquí
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              // Muestra un texto de carga mientras el Future está pendiente
              return Text("Loading...");
            } else if (snapshot.hasError) {
              // Maneja errores en caso de que fallen las llamadas HTTP
              return Text("Error: ${snapshot.error}");
            } else {
              // Muestra el nombre del paciente una vez cargado
              return Text(
                "New Intake ${snapshot.data}",
                style: TextStyle(fontSize: widget.textSize + 2),
              );
            }
          },
        ),
        backgroundColor: Theme.of(context).primaryColor,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(widget.padding),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // Fecha
            Text(
              "Date",
              style: TextStyle(fontSize: widget.textSize),
            ),
            Row(
              children: [
                Expanded(
                  child: InkWell(
                    child: Text(
                      "${widget.selectedDate.toLocal()}".split(' ')[0],
                      style: Theme.of(context)
                          .textTheme
                          .headlineSmall
                          ?.copyWith(fontSize: widget.textSize),
                      textAlign: TextAlign.center, //centrar el valor del campo
                    ),
                    onTap: () =>
                        isSmartwatch ? _selectDateSmartwatch() : _selectDate(),
                  ),
                ),
              ],
            ),
            const SizedBox(
              height: 8,
            ),

            // Hora
            Text(
              "Time",
              style: TextStyle(fontSize: widget.textSize),
            ),
            Row(
              children: [
                Expanded(
                  child: InkWell(
                    child: Text(
                      "${widget.selectedDate.toLocal()}"
                          .split(' ')[1]
                          .split(':00.000')[0],
                      style: Theme.of(context)
                          .textTheme
                          .headlineSmall
                          ?.copyWith(fontSize: widget.textSize),
                      textAlign: TextAlign.center, //centrar el texto del valor
                    ),
                    onTap: () =>
                        isSmartwatch ? _selectTimeSmartwatch() : _selectTime(),
                  ),
                )
              ],
            ),
            const SizedBox(
              height: 8,
            ),
            const SizedBox(
              height: 16,
            ),

            // Boton para guardar
            Padding(
              padding: EdgeInsets.symmetric(
                  vertical: widget.padding), //centrar el boton
              child: ElevatedButton(
                key: const Key('AddIntakeElevatedButton'),
                onPressed: () async {
                  try {
                    await context.read<IntakeModel>().addIntake(
                        widget.patientId,
                        widget.medicationId,
                        widget.selectedDate);
                    Navigator.pop(context, true);
                  } catch (error) {
                    // Mostrar el error al usuario
                    ScaffoldMessenger.of(context).removeCurrentSnackBar();
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        duration: const Duration(seconds: 3),
                        behavior: SnackBarBehavior
                            .floating, //para que no este pegado abajo el mensaje de error y permita flotar
                        content: Text(
                          'Error: ${error.toString()}',
                          style: TextStyle(fontSize: widget.textSize - 3),
                          textAlign: TextAlign.center,
                        ),
                        backgroundColor: Colors.red,
                      ),
                    );
                  }
                },
                child: Text(
                  "Save",
                  style: TextStyle(fontSize: widget.textSize),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/*
class PatientListPage extends StatefulWidget {
  const PatientListPage({super.key});

  @override
  State<StatefulWidget> createState() => _PatientListPage();
}

class _PatientListPage extends State<PatientListPage> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<PatientModel>().loadPatients();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("My patients"),
        backgroundColor: Theme.of(context).primaryColor,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            context.watch<PatientModel>().errorMessage != null
                ? ErrorMessage(
                    message: context.watch<PatientModel>().errorMessage!)
                : ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: context.watch<PatientModel>().patients.length,
                    itemBuilder: (context, index) {
                      return PatientTile(
                          patient:
                              context.watch<PatientModel>().patients[index]);
                    },
                  ),
            if (context.watch<PatientModel>().isLoading)
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: CircularProgressIndicator(),
              ),
            context.watch<PatientModel>().hasMorePatients
                ? Center(
                    child: ElevatedButton(
                      onPressed: () =>
                          context.read<PatientModel>().loadPatients(),
                      child: Text("Load more patients"),
                    ),
                  )
                : Text("End of list"),
          ],
        ),
      ),
    );
  }
}

class PatientTile extends StatelessWidget {
  const PatientTile({
    super.key,
    required this.patient,
  });

  final Patient patient;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          InkWell(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "${patient.name} ${patient.surname} ",
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                Text(
                  patient.code,
                  style: Theme.of(context).textTheme.titleMedium,
                ),
              ],
            ),
            onTap: () => Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => PatientDetailsPage(patient),
              ),
            ),
          ),
          IconButton(
            icon: Icon(patient.starred ? Icons.star : Icons.star_border),
            onPressed: () =>
                context.read<PatientModel>().toggleStarred(patient),
          ),
        ],
      ),
    );
  }
}
*/

class ErrorMessage extends StatelessWidget {
  const ErrorMessage({
    required this.message,
    required this.textSize,
    required this.padding,
    super.key,
  });

  final String message;
  final double textSize; //puede aceptar textSize
  final double padding; //y valor de padding
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(padding),
      child: Text(
        message,
        textAlign: TextAlign.center,
        style: Theme.of(context).textTheme.bodyMedium!.copyWith(
              color: Color.fromARGB(255, 173, 68, 68),
              fontSize:
                  textSize, //tamaño del texto por si es un reloj, movil etc
            ),
      ),
    );
  }
}

/*
class PatientDetailsPage extends StatefulWidget {
  final Patient patient;
  const PatientDetailsPage(this.patient, {super.key});

  @override
  State<StatefulWidget> createState() => _PatientDetailsPage();
}

class _PatientDetailsPage extends State<PatientDetailsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Patient details"),
        backgroundColor: Theme.of(context).primaryColor,
        foregroundColor: Colors.white,
      ),
      body: FutureBuilder(
          future:
              context.read<PatientModel>().getPatientData(widget.patient.id),
          builder: (context, snapshot) {
            if (snapshot.hasError) {
              return ErrorMessage(message: snapshot.error.toString());
            } else {
              if (!snapshot.hasData) {
                return Center(child: CircularProgressIndicator());
              } else {
                return Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    children: [
                      PatientDetailsTile(
                        title: "Name",
                        content: snapshot.data!.name,
                      ),
                      PatientDetailsTile(
                        title: "Surname",
                        content: snapshot.data!.surname,
                      ),
                      PatientDetailsTile(
                        title: "Code",
                        content: snapshot.data!.code,
                      ),
                      Center(
                          child: ElevatedButton(
                        onPressed: () {},
                        child: const Text("Do something!"),
                      ))
                    ],
                  ),
                );
              }
            }
          }),
    );
  }
}

class PatientDetailsTile extends StatelessWidget {
  const PatientDetailsTile(
      {super.key, required this.title, required this.content});

  final String title;
  final String content;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.only(bottom: 16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                content,
                style: Theme.of(context).textTheme.headlineSmall,
              ),
              IconButton(onPressed: () {}, icon: Icon(Icons.edit)),
            ],
          ),
        ],
      ),
    );
  }
}
*/