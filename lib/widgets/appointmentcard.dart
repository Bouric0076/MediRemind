import 'package:flutter/material.dart';
import '../models/appointmentmodel.dart';
import 'package:intl/intl.dart';

class AppointmentCard extends StatelessWidget {
  final Appointment appointment;

  const AppointmentCard({super.key, required this.appointment});

  @override
  Widget build(BuildContext context) {
    final formatted = DateFormat('MMM d, hh:mm a').format(appointment.dateTime);
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      child: ListTile(
        title: Text(appointment.patientName),
        subtitle: Text(formatted),
        trailing: Icon(
          appointment.contactMethod == "WhatsApp" ? Icons.chat : Icons.sms,
        ),
      ),
    );
  }
}