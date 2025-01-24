import 'dart:async';
import 'dart:io';
import 'dart:convert';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'; //para las notificaciones de las proximas tomas ( posologias )
import 'package:timezone/data/latest.dart' as tz; //paquete para las zonas horarias
import 'package:timezone/timezone.dart' as tz; //tambien para la hora

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

var serverUrl = Platform.isAndroid ? "10.0.2.2" : "127.0.0.1";
//var serverUrl = "127.0.0.1"; //si haces adb reverse tcp:8000 tcp:8000 rediriges trafico de movil a pc
var serverPort = "8000";

class Patient {
  Patient(this.id, this.code, this.name, this.surname);
  final int id;
  final String code;
  final String name;
  final String surname;
  bool starred = false;

  Patient.fromJson(Map json)
      : id = json["id"],
        name = json["name"],
        surname = json["surname"],
        code = json["code"],
        starred = false;

  @override
  String toString() {
    return "$id | $code | $name $surname";
  }
}

class PatientModel with ChangeNotifier {
  List<Patient> patients = [];
  int patientCount = 0;
  int startIndex = 0;
  int count = 10;
  String? errorMessage;
  bool isLoading = false;
  bool hasMorePatients = true;
  Patient? selectedPatient;

  void loadPatients() async {
    isLoading = true;
    errorMessage = null;
    notifyListeners();

    var uri = Uri.http("$serverUrl:$serverPort", "patients",
        {'start_index': "$startIndex", 'count': "$count"});
    try {
      var response = await http.get(uri);
      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        if (data.isEmpty) {
          hasMorePatients = false;
        } else {
          startIndex = startIndex + count;
        }
        patients.addAll(
            List<Patient>.from(data.map((item) => Patient.fromJson(item))));
      } else {
        errorMessage = "Invalid data";
      }
    } on http.ClientException {
      errorMessage = "Service is not available. Try again later.";
    }
    isLoading = false;
    notifyListeners();
  }

  Future<int> getIdPatient(String text) async {
    var uri = Uri.http("$serverUrl:$serverPort", "patients", {"code": text});

    try {
      // Esperamos la respuesta de la solicitud HTTP
      var response = await http.get(uri);

      // Si la respuesta fue exitosa, procesamos los datos
      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        return Patient.fromJson(data).id;  // Retornamos el ID del paciente
      } else {
        // Si la respuesta del servidor no es exitosa
        throw Exception("Error: ${response.statusCode} - ${response.body}");
      }
    } on http.ClientException {
      // Si hay problemas con la conexión al servidor (por ejemplo, no hay internet)
      throw http.ClientException("Service is not available. Try again later.");
    } catch (e) {
      // Capturamos otros posibles errores
      throw Exception("An unexpected error occurred: $e");
    }
  }


  void toggleStarred(Patient patient) {
    patient.starred = !patient.starred;
    notifyListeners();
  }

  Future<Patient> getPatientData(int id) async {
    var uri = Uri.http("$serverUrl:$serverPort", "patients/$id");
    try {
      ///print("aqui $uri");
      var response = await http.get(uri);
      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        return Patient.fromJson(data);
      } else {
        throw Exception(response.body);
      }
    } on http.ClientException {
      throw http.ClientException("Service is not available. Try again later.");
    }
  }

  Future<String> getPatientName(int id) async {
    var uri = Uri.http("$serverUrl:$serverPort", "patients/$id");
    try {
      //print("aqui $uri");
      var response = await http.get(uri);
      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        return Patient.fromJson(data).name;
      } else {
        throw Exception(response.body);
      }
    } on http.ClientException {
      throw http.ClientException("Service is not available. Try again later.");
    }
  }

}

class Medicine {
  Medicine(this.id, this.name, this.dosage, this.start_date,
      this.treatment_duration, this.patient_id);
  final int id;
  final String name;
  final String dosage;
  final String start_date;
  final String treatment_duration;
  final int patient_id;

  Medicine.fromJson(Map json)
      : id = json["id"],
        name = json["name"],
        dosage = json["dosage"].toString(),
        start_date = json["start_date"].toString(),
        treatment_duration = json["treatment_duration"].toString(),
        patient_id = json["patient_id"];

  @override
  String toString() {
    return "$id | $name | $dosage | $start_date | $treatment_duration | $patient_id";
  }
}

class MedicineModel with ChangeNotifier {
  List<Medicine> medicines = [];
  //int startIndex = 0; //startIndex ni count los acepta la BD en medicamentos
  //int count = 10;
  String? errorMessage;
  bool isLoading = false;
  bool hasNoMedicines = false;
  Medicine? selectedMedicine;

  void loadMedicines(int patientId) async {
    //cargar los medicamentos
    isLoading = true;
    errorMessage = null;
    notifyListeners();
    medicines.clear(); // Limpiar la lista antes de agregar nuevos datos

    var uri =
        Uri.http("$serverUrl:$serverPort", "patients/$patientId/medications");

    try {
      var response = await http.get(uri);
      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        if (data.isEmpty) {
          hasNoMedicines = true;
        } else {
          //pues nada
          hasNoMedicines = false;
        }
        medicines.addAll(
            List<Medicine>.from(data.map((item) => Medicine.fromJson(item))));
      } else {
        errorMessage = "Invalid Data Medicines";
      }
    } on http.ClientException {
      errorMessage = "Service is not avaliable. Try again later";
    }
    isLoading = false;
    notifyListeners();
  }

  Future<Medicine> getMedicineData(int idPatient, int idMedicine) async {
    var uri = Uri.http("$serverUrl:$serverPort",
        "patients/$idPatient/medications/$idMedicine");
    try {
      var response = await http.get(uri);
      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        return Medicine.fromJson(data);
      } else {
        throw Exception(response.body);
      }
    } on http.ClientException {
      throw http.ClientException("Service is not avaliable. Try again later");
    }
  }
}

class Posologie {
  Posologie(this.id, this.hour, this.minute, this.medication_id);
  final int id;
  final int hour;
  final int minute;
  final int medication_id;
  Posologie.fromJson(Map json)
      : id = json["id"],
        hour = json["hour"],
        minute = json["minute"],
        medication_id = json["medication_id"];

  @override
  String toString() {
    return "$id | $hour | $minute | $medication_id";
  }
}

class PosologieModel with ChangeNotifier {
  List<Posologie> posologies = [];
  //int startIndex = 0; //startIndex ni count los acepta la BD en medicamentos
  //int count = 10;
  String? errorMessage;
  bool isLoading = false;
  bool hasNoPosologies = false;
  Posologie? selectedPosologie;



  //notificaciones
  // Instancia de FlutterLocalNotificationsPlugin
  final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin =
  FlutterLocalNotificationsPlugin();

  // Inicializar las notificaciones
  Future<void> initializeNotifications() async {
    const AndroidInitializationSettings initializationSettingsAndroid =
    AndroidInitializationSettings('@mipmap/ic_launcher');

    const InitializationSettings initializationSettings =
    InitializationSettings(android: initializationSettingsAndroid);

    await flutterLocalNotificationsPlugin.initialize(initializationSettings);
  }


  // Programar notificaciones para las posologías
  Future<void> schedulePosologieNotifications() async {
    for (var posologie in posologies) {
      // Calcula la hora de la notificación (5 minutos antes)
      final now = DateTime.now();
      final notificationTime = DateTime(
        now.year,
        now.month,
        now.day,
        posologie.hour,
        posologie.minute,
      ).subtract(const Duration(minutes: 5));

      // Si el tiempo de la notificación ya pasó hoy, no la programamos
      if (notificationTime.isBefore(now)) continue;

      // Convierte DateTime a TZDateTime
      final tzNotificationTime = tz.TZDateTime.from(notificationTime, tz.local);

      // Configurar notificación
      await flutterLocalNotificationsPlugin.zonedSchedule(
        posologie.id, // ID único para cada notificación
        'Reminder', // Título
        'It’s time to take your medication (ID: ${posologie.medication_id})',
        tzNotificationTime, // Hora de la notificación
        const NotificationDetails(
          android: AndroidNotificationDetails(
            'medication_channel', // ID del canal
            'Medication Reminders', // Nombre del canal
            channelDescription: 'Reminders to take your medications',
            importance: Importance.high,
            priority: Priority.high,
          ),
        ),
        uiLocalNotificationDateInterpretation:
        UILocalNotificationDateInterpretation.absoluteTime,
        androidScheduleMode: AndroidScheduleMode.exact, // Especificar el modo
      );
    }
  }


  // Método para cancelar todas las notificaciones (si es necesario)
  Future<void> cancelAllNotifications() async {
    await flutterLocalNotificationsPlugin.cancelAll();
  }



  void loadPosologies(int patientId, int medicationId) async {
    //cargar las posologias
    isLoading = true;
    errorMessage = null;
    notifyListeners();
    posologies.clear(); // Limpiar la lista antes de agregar nuevos datos

    var uri = Uri.http("$serverUrl:$serverPort",
        "patients/$patientId/medications/$medicationId/posologies");

    try {
      var response = await http.get(uri);
      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        if (data.isEmpty) {
          hasNoPosologies = true;
        } else {
          //pues nada
          hasNoPosologies = false;
        }
        posologies.addAll(
            List<Posologie>.from(data.map((item) => Posologie.fromJson(item))));
        isLoading = false;
        notifyListeners();
        // Programa las notificaciones para las posologías cargadas
        await schedulePosologieNotifications();
      } else {
        errorMessage = "Invalid Data Posologies";
      }
    } on http.ClientException {
      errorMessage = "Service is not avaliable. Try again later";
    }
    isLoading = false;
    notifyListeners();
  }

  Future<Posologie> getPosologieData(
      int idPatient, int idMedicine, int idPosologie) async {
    var uri = Uri.http("$serverUrl:$serverPort",
        "patients/$idPatient/medications/$idMedicine/posologies/$idPosologie");
    try {
      var response = await http.get(uri);
      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        return Posologie.fromJson(data);
      } else {
        throw Exception(response.body);
      }
    } on http.ClientException {
      throw http.ClientException("Service is not avaliable. Try again later");
    }
  }
}

// Intakes
class Intake {
  Intake(this.id, this.date, this.medicationId);
  final int id;
  final String date;
  final int medicationId;
  Intake.fromJson(Map json)
      : id = json["id"],
        date = json["date"],
        medicationId = json["medication_id"];

  @override
  String toString() {
    return "$id | $date | $medicationId";
  }
}

class IntakeModel with ChangeNotifier {
  List<Intake> intakes = [];
  //int startIndex = 0; //startIndex ni count los acepta la BD en medicamentos
  //int count = 10;
  String? errorMessage;
  bool isLoading = false;
  bool hasNoIntakes = false;
  //Intake? selectedIntake;

  void loadIntakes(int patientId, int medicationId) async {
    //cargar los intakes
    isLoading = true;
    errorMessage = null;
    notifyListeners();
    intakes.clear(); // Limpiar la lista antes de agregar nuevos datos

    var uri = Uri.http("$serverUrl:$serverPort",
        "patients/$patientId/medications/$medicationId/intakes");

    try {
      var response = await http.get(uri);
      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        if (data.isEmpty) {
          hasNoIntakes = true;
        } else {
          hasNoIntakes = false;
        }
        intakes.addAll(
            List<Intake>.from(data.map((item) => Intake.fromJson(item))));
      } else {
        errorMessage = "Invalid Data Intakes";
      }
    } on http.ClientException {
      errorMessage = "Service is not avaliable. Try again later";
    }
    isLoading = false;
    notifyListeners();
  }

  Future<Intake> getIntakeData(
      int patientId, int medicationId, int intakeId) async {
    var uri = Uri.http("$serverUrl:$serverPort",
        "patients/$patientId/medications/$medicationId/intakes/$intakeId");
    try {
      var response = await http.get(uri);
      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        return Intake.fromJson(data);
      } else {
        throw Exception(response.body);
      }
    } on http.ClientException {
      throw http.ClientException("Service is not avaliable. Try again later");
    }
  }

  Future<void> addIntake(int patientId, int medicationId, DateTime date) async {
    var uri = Uri.http("$serverUrl:$serverPort",
        "patients/$patientId/medications/$medicationId/intakes");
    final body =
        jsonEncode({"date": date.toIso8601String().split(':00.000')[0]});
    try {
      var response = await http.post(uri,
          headers: {
            "Content-Type": "application/json", // Indica que el cuerpo es JSON
          },
          body: body);
      if (response.statusCode == 201) {
        // Añadir intake exitoso, recargar lista
        var data = json.decode(response.body);
        intakes.add(Intake.fromJson(data));
        notifyListeners();
      } else {
        throw Exception(response.body);
      }
    } on http.ClientException {
      throw http.ClientException("Service not available");
    }
  }
}
