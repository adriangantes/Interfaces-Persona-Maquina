import 'dart:async';
import 'dart:developer';
import 'dart:io';
import 'dart:convert';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'; //para las notificaciones de las proximas tomas ( posologias )
import 'package:timezone/data/latest.dart'
    as tz; //paquete para las zonas horarias
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

class PatientModelService {
  Future<List<Patient>> getPatients(int startIndex, int count) async {
    var uri = Uri.http("$serverUrl:$serverPort", "patients",
        {'start_index': "$startIndex", 'count': "$count"});

    var response = await http.get(uri);
    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      return List<Patient>.from(data.map((item) => Patient.fromJson(item)));
    } else {
      throw Exception("Invalid data");
    }
  }

  Future<Patient> getPatient(int id) async {
    var uri = Uri.http("$serverUrl:$serverPort", "patients/$id");

    var response = await http.get(uri);
    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      return Patient.fromJson(data);
    } else {
      throw Exception(response.body);
    }
  }

  Future<Patient> getPatientWithCode(String code) async {
    var uri = Uri.http("$serverUrl:$serverPort", "patients", {"code": code});

    var response = await http.get(uri);
    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      return Patient.fromJson(data);
    } else {
      throw Exception("Invalid data");
    }
  }
}

class MockPatientModelService extends PatientModelService {
  Patient patient = Patient(1, '314-42-2001', 'Tester', 'McTesting');

  @override
  Future<List<Patient>> getPatients(int startIndex, int count) {
    return Future(() => List.from([patient]));
  }

  @override
  Future<Patient> getPatient(int id) {
    if (id == patient.id) {
      return Future(() => patient);
    } else {
      throw Exception("Invalid data");
    }
  }

  @override
  Future<Patient> getPatientWithCode(String code) {
    if (code == patient.code) {
      return Future(() => patient);
    } else {
      throw Exception("Invalid data");
    }
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

  late PatientModelService
      service; // late es para que no se queje de que no está inicializado

  PatientModel({service}) {
    // Si no se le pasa un service se le pone el PatientModelService
    this.service = service ?? PatientModelService();
  }

  void loadPatients() async {
    isLoading = true;
    errorMessage = null;
    notifyListeners();

    /* var uri = Uri.http("$serverUrl:$serverPort", "patients",
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
    } */
    try {
      List<Patient> list = await service.getPatients(startIndex, count);
      if (list.isEmpty) {
        hasMorePatients = false;
      } else {
        startIndex = startIndex + count;
      }
      patients.addAll(list);
    } on http.ClientException {
      errorMessage = "Service is not available. Try again later.";
    }

    isLoading = false;
    notifyListeners();
  }

  Future<int> getPatientIdWithCode(String text) async {
    /* var uri = Uri.http("$serverUrl:$serverPort", "patients", {"code": text});

    try {
      // Esperamos la respuesta de la solicitud HTTP
      var response = await http.get(uri);

      // Si la respuesta fue exitosa, procesamos los datos
      if (response.statusCode == 200) {
        var data = json.decode(response.body);
        return Patient.fromJson(data).id; // Retornamos el ID del paciente
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
    } */
    try {
      Patient patient = await service.getPatientWithCode(text);
      return patient.id;
    } on http.ClientException {
      throw http.ClientException("Service is not available. Try again later.");
    }
  }

  //void toggleStarred(Patient patient) {
  //  patient.starred = !patient.starred;
  //  notifyListeners();
  //}

  Future<Patient> getPatientData(int id) async {
    /* var uri = Uri.http("$serverUrl:$serverPort", "patients/$id");
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
    } */
    try {
      Patient patient = await service.getPatient(id);
      return patient;
    } on http.ClientException {
      throw http.ClientException("Service is not available. Try again later.");
    }
  }

  // Esta función es necesaria porque nos hace falta una función que devuelva un future que sea solo el nombre.
  Future<String> getPatientName(int id) async {
    /* var uri = Uri.http("$serverUrl:$serverPort", "patients/$id");
    try {
      return (await service.getPatient(id)).name;
    } on http.ClientException {
      throw http.ClientException("Service is not available. Try again later.");
    } */
    try {
      Patient patient = await service.getPatient(id);
      return patient.name;
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

class MedicationModelService {
  Future<List<Medicine>> getMedications(int patientId) async {
    var uri =
        Uri.http("$serverUrl:$serverPort", "patients/$patientId/medications");

    var response = await http.get(uri);
    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      return List<Medicine>.from(data.map((item) => Medicine.fromJson(item)));
    } else {
      throw Exception("Invalid data");
    }
  }

  Future<Medicine> getMedication(int patientId, int medicationId) async {
    var uri = Uri.http("$serverUrl:$serverPort",
        "patients/$patientId/medications/$medicationId");

    var response = await http.get(uri);
    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      return Medicine.fromJson(data);
    } else {
      throw Exception(response.body);
    }
  }
}

class MockMedicationModelService extends MedicationModelService {
  Medicine medication =
      Medicine(1, "TestingMedication", "1.0", "11-12-2001", "20", 1);

  @override
  Future<List<Medicine>> getMedications(int patientId) {
    return Future(() => List.from([medication]));
  }

  @override
  Future<Medicine> getMedication(int patientId, int medicationId) {
    return Future(() => medication);
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

  late MedicationModelService service;

  MedicineModel({service}) {
    this.service = service ?? MedicationModelService();
  }

  void loadMedicines(int patientId) async {
    //cargar los medicamentos
    isLoading = true;
    errorMessage = null;
    notifyListeners();
    medicines.clear(); // Limpiar la lista antes de agregar nuevos datos

    try {
      List<Medicine> list = await service.getMedications(patientId);
      hasNoMedicines = list.isEmpty;
      medicines.addAll(list);
    } on http.ClientException {
      errorMessage = "Service is not avaliable. Try again later";
    }
    isLoading = false;
    notifyListeners();
  }

  Future<Medicine> getMedicineData(int patientId, int medicationId) async {
    try {
      Medicine medication =
          await service.getMedication(patientId, medicationId);
      return medication;
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

class PosologieModelService {
  Future<List<Posologie>> getPosologies(int patientId, int medicationId) async {
    var uri = Uri.http("$serverUrl:$serverPort",
        "patients/$patientId/medications/$medicationId/posologies");

    var response = await http.get(uri);
    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      return List<Posologie>.from(data.map((item) => Posologie.fromJson(item)));
    } else {
      throw Exception("Invalid data");
    }
  }

  Future<Posologie> getPosologie(
      int patientId, int medicationId, int posologieId) async {
    var uri = Uri.http("$serverUrl:$serverPort",
        "patients/$patientId/medications/$medicationId/posologies/$posologieId");

    var response = await http.get(uri);
    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      return Posologie.fromJson(data);
    } else {
      throw Exception(response.body);
    }
  }
}

class MockPosologyModelService extends PosologieModelService {
  Posologie posology = Posologie(1, 12, 0, 1);

  @override
  Future<List<Posologie>> getPosologies(int patientId, int medicationId) {
    return Future(() => List.from([posology]));
  }

  @override
  Future<Posologie> getPosologie(
      int patientId, int medicationId, int posologieId) {
    return Future(() => posology);
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

  late PosologieModelService service;

  PosologieModel({service}) {
    this.service = service ?? PosologieModelService();
  }

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

    try {
      List<Posologie> list =
          await service.getPosologies(patientId, medicationId);
      hasNoPosologies = list.isEmpty;
      posologies.addAll(list);
      isLoading = false;
      notifyListeners();
      // Programa las notificaciones para las posologías cargadas
      await schedulePosologieNotifications();
    } on http.ClientException {
      errorMessage = "Service is not avaliable. Try again later";
    }
    isLoading = false;
    notifyListeners();
  }

  Future<Posologie> getPosologieData(
      int patientId, int medicationId, int posologieId) async {
    try {
      Posologie posologie =
          await service.getPosologie(patientId, medicationId, posologieId);
      return posologie;
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

class IntakeModelService {
  Future<List<Intake>> getIntakes(int patientId, int medicationId) async {
    var uri = Uri.http("$serverUrl:$serverPort",
        "patients/$patientId/medications/$medicationId/intakes");

    var response = await http.get(uri);
    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      return List<Intake>.from(data.map((item) => Intake.fromJson(item)));
    } else {
      throw Exception("Invalid data");
    }
  }

  Future<Intake> getIntake(
      int patientId, int medicationId, int intakeId) async {
    var uri = Uri.http("$serverUrl:$serverPort",
        "patients/$patientId/medications/$medicationId/intakes/$intakeId");

    var response = await http.get(uri);
    if (response.statusCode == 200) {
      var data = json.decode(response.body);
      return Intake.fromJson(data);
    } else {
      throw Exception(response.body);
    }
  }

  //addIntake
  Future<Intake> addIntake(
      int patientId, int medicationId, DateTime date) async {
    var uri = Uri.http("$serverUrl:$serverPort",
        "patients/$patientId/medications/$medicationId/intakes");
    final body =
        jsonEncode({"date": date.toIso8601String().split(':00.000')[0]});

    var response = await http.post(uri,
        headers: {
          "Content-Type": "application/json", // Indica que el cuerpo es JSON
        },
        body: body);
    if (response.statusCode == 201) {
      // Añadir intake exitoso, recargar lista
      var data = json.decode(response.body);
      return Intake.fromJson(data);
    } else {
      throw Exception(response.body);
    }
  }
}

class MockIntakeModelService extends IntakeModelService {
  Intake intake = Intake(1, "2024-10-17T06:07", 1);
  List<Intake> list = List.empty(growable: true);

  @override
  Future<List<Intake>> getIntakes(int patientId, int medicationId) {
    return Future(() => list);
  }

  @override
  Future<Intake> getIntake(int patientId, int medicationId, int intakeId) {
    return Future(() => intake);
  }

  @override
  Future<Intake> addIntake(int patientId, int medicationId, DateTime date) {
    list.add(intake);
    return Future(() => intake);
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

  late IntakeModelService service;

  IntakeModel({service}) {
    this.service = service ?? IntakeModelService();
  }

  void loadIntakes(int patientId, int medicationId) async {
    //cargar los intakes
    isLoading = true;
    errorMessage = null;
    notifyListeners();
    intakes.clear(); // Limpiar la lista antes de agregar nuevos datos

    try {
      List<Intake> list = await service.getIntakes(patientId, medicationId);
      hasNoIntakes = list.isEmpty;
      intakes.addAll(list);
    } on http.ClientException {
      errorMessage = "Service is not avaliable. Try again later";
    }
    isLoading = false;
    notifyListeners();
  }

  Future<Intake> getIntakeData(
      int patientId, int medicationId, int intakeId) async {
    try {
      Intake intake =
          await service.getIntake(patientId, medicationId, intakeId);
      return intake;
    } on http.ClientException {
      throw http.ClientException("Service is not avaliable. Try again later");
    }
  }

  Future<void> addIntake(int patientId, int medicationId, DateTime date) async {
    try {
      Intake intake = await service.addIntake(patientId, medicationId, date);
      intakes.add(intake);
      hasNoIntakes = intakes.isEmpty;
      notifyListeners();
    } on http.ClientException {
      throw http.ClientException("Service is not avaliable. Try again later");
    }
  }
}
