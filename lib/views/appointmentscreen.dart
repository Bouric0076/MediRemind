import 'package:flutter/material.dart';
import '../models/appointmentmodel.dart';
import '../widgets/appointmentcard.dart';

class AppointmentScreen extends StatelessWidget {
  final appointments = [
    Appointment(
      id: '1',
      patientName: 'Jane Doe',
      dateTime: DateTime.now().add(Duration(hours: 1)),
      contactMethod: 'SMS',
    ),
    Appointment(
      id: '2',
      patientName: 'John Smith',
      dateTime: DateTime.now().add(Duration(days: 1)),
      contactMethod: 'WhatsApp',
    ),
  ];

   AppointmentScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: appointments.length,
      itemBuilder: (context, index) => AppointmentCard(appointment: appointments[index]),
    );
  }
}
