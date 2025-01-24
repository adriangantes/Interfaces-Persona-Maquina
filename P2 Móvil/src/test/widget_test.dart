// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

import 'package:src/main.dart';
import 'package:src/model.dart';

/*
Posibles casos de prueba:
  - Muestra paciente al insertar texto y meter botón
  - Muestra posología al darle al botón de posología
  - Muestra intakes al darle al botón de intakes
  - Va a la ventana de crear intake al darle al botón correspondiente
  - Agrega el intake al darle a añadir

De error:
  - El servidor está caído (no se puede testear al usar mockService)
  - En el login pongan un usuario inválido
  - En el login se ponga un formato de código incorrecto
  - El login se deja vacío
  - Más?
*/

void main() {
  testWidgets('Test app', (WidgetTester tester) async {
    // Modelos que usan el servicio falso
    final patientModel = PatientModel(service: MockPatientModelService());
    final medicationModel =
        MedicineModel(service: MockMedicationModelService());
    final posologyModel = PosologieModel(service: MockPosologyModelService());
    final intakeModel = IntakeModel(service: MockIntakeModelService());

    // Construimos la app
    await tester.pumpWidget(MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => patientModel),
        ChangeNotifierProvider(create: (context) => medicationModel),
        ChangeNotifierProvider(create: (context) => posologyModel),
        ChangeNotifierProvider(create: (context) => intakeModel),
      ],
      child: const MainApp(),
    ));

    // Testear que muestra medicamentos al meter el texto

    // Mirar que está el campo de texto y el botón
    expect(find.byKey(const Key('patientCodeTextField')), findsOneWidget);
    expect(find.byKey(const Key('loginElevatedButton')), findsOneWidget);

    // Intentamos acceder dejando el campo vacío
    await tester.tap(find.byKey(const Key('loginElevatedButton')));
    await tester.pumpAndSettle();
    expect(find.byType(LoginPage), findsOneWidget);
    expect(find.textContaining("Please, ID cannot be empty."), findsOneWidget);

    // Metemos un código que no existe para ver si salta el error
    await tester.enterText(find.byKey(const Key('patientCodeTextField')),
        MockPatientModelService().patient.code.replaceAll('3', '1'));
    await tester.tap(find.byKey(const Key('loginElevatedButton')));
    await tester.pumpAndSettle();
    expect(find.byType(LoginPage), findsOneWidget);
    expect(find.textContaining("Error"), findsOneWidget);

    // Metemos un código con formato erroneo
    await tester.enterText(
        find.byKey(const Key('patientCodeTextField')), '123-12-12345');
    await tester.tap(find.byKey(const Key('loginElevatedButton')));
    // esperamos un rato para que desaparezca el anterior
    await tester.pumpAndSettle();
    expect(find.byType(LoginPage), findsOneWidget);
    expect(find.textContaining("ID invalid"), findsOneWidget);

    // Metemos el código y pulsamos el botón
    await tester.enterText(find.byKey(const Key('patientCodeTextField')),
        MockPatientModelService().patient.code);
    await tester.tap(find.byKey(const Key('loginElevatedButton')));
    await tester.pumpAndSettle();

    // Miramos que se generara la nueva pantalla
    expect(find.byType(MedicineListPage), findsOneWidget);

    // Mirar que ha aparecido un medicamento y toda su información
    expect(find.byType(MedicineTitle), findsOneWidget);
    expect(find.text(MockMedicationModelService().medication.name),
        findsOneWidget);
    expect(find.text(MockMedicationModelService().medication.dosage),
        findsOneWidget);
    expect(find.text(MockMedicationModelService().medication.start_date),
        findsOneWidget);
    expect(
        find.text(MockMedicationModelService().medication.treatment_duration),
        findsOneWidget);

    // Clickamos en el medicamento (solo debería haber 1)
    await tester.tap(find.byKey(const Key('toMedicationDetailInkWell')));
    await tester.pumpAndSettle();

    // Vemos si está la nueva pantalla
    expect(find.byType(MedicineDetailsPage), findsOneWidget);

    // Verificamos que se muestra lo que se debe mostrar
    expect(find.text(MockMedicationModelService().medication.name),
        findsOneWidget);
    expect(find.text(MockMedicationModelService().medication.dosage),
        findsOneWidget);
    expect(find.text(MockMedicationModelService().medication.start_date),
        findsOneWidget);
    expect(
        find.text(MockMedicationModelService().medication.treatment_duration),
        findsOneWidget);
    expect(find.byKey(const Key('toPosologiesListElevatedButton')),
        findsOneWidget);
    expect(
        find.byKey(const Key('toIntakesListElevatedButton')), findsOneWidget);

    // Vamos a la lista de posologías
    await tester.tap(find.byKey(const Key('toPosologiesListElevatedButton')));
    await tester.pumpAndSettle();

    // Vemos si está la nueva pantalla
    expect(find.byType(PosologiesListPage), findsOneWidget);

    // Vemos si está la posología
    expect(find.byType(PosologieTitle), findsOneWidget);
    expect(find.textContaining("Hour"), findsOne);
    expect(find.textContaining("Minute"), findsOne);

    // Vamos hacia atras con el botón de retroceso en la AppBar
    await tester.tap(find.byType(BackButton));
    await tester.pumpAndSettle();

    // Verificar que estamos de vuelta en la pantalla anterior
    expect(find.byType(MedicineDetailsPage), findsOneWidget);

    // Vamos a la lista de intakes
    await tester.tap(find.byKey(const Key('toIntakesListElevatedButton')));
    await tester.pumpAndSettle();

    // Vemos si está la nueva pantalla
    expect(find.byType(IntakesListPage), findsOneWidget);

    // Vemos si está vacía (debería)
    expect(find.byType(IntakeTitle), findsNothing);
    expect(find.textContaining("No intakes"), findsOne);

    // Buscamos el botón de añadir intakes
    expect(find.byType(FloatingActionButton), findsOne);

    // Clickamos en añadir intakes
    await tester.tap(find.byType(FloatingActionButton));
    await tester.pumpAndSettle();

    // Vemos si estamos en la nueva pantalla
    expect(find.byType(IntakeAddPage), findsOneWidget);

    // Miramos si están los campos
    expect(find.text('Date'), findsOneWidget);
    expect(find.text('Time'), findsOneWidget);
    expect(find.byKey(const Key('AddIntakeElevatedButton')), findsOne);

    // Pulsamos para añadir
    await tester.tap(find.byKey(const Key('AddIntakeElevatedButton')));
    await tester.pumpAndSettle();

    // Revisar si volvimos a la lista
    expect(find.byType(IntakesListPage), findsOneWidget);

    // Ver si tiene un elemento
    expect(find.byType(IntakeTitle), findsOneWidget);
    expect(find.textContaining("No intakes"), findsNothing);
  });
}
