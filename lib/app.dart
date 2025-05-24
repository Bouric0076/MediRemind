import 'package:flutter/material.dart';
import 'routes/approutes.dart';
import 'views/loginscreen.dart';
import 'views/homescreen.dart';

class ClinicReminderApp extends StatelessWidget {
  const ClinicReminderApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Clinic Reminder',
      theme: ThemeData(primarySwatch: Colors.teal),
      debugShowCheckedModeBanner: false,
      initialRoute: AppRoutes.login,
      routes: {
        AppRoutes.login: (context) => LoginScreen(),
        AppRoutes.home: (context) => HomeScreen(),
      },
    );
  }
}
