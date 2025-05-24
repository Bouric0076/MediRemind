import 'package:flutter/material.dart';
import '../views/appointmentscreen.dart';
import '../views/addappointmentscreen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Appointments")),
      body: AppointmentScreen(),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => AddAppointmentScreen()),
          );
        },
        child: Icon(Icons.add),
      ),
    );
  }
}
