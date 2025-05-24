import 'package:flutter/material.dart';
import '../widgets/inputfield.dart';
import '../widgets/custombutton.dart';
import '../routes/approutes.dart';
class LoginScreen extends StatelessWidget {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: EdgeInsets.all(20),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text("Clinic Reminder", style: TextStyle(fontSize: 28)),
              SizedBox(height: 20),
              InputField(controller: emailController, label: "Email"),
              SizedBox(height: 10),
              InputField(controller: passwordController, label: "Password", obscureText: true),
              SizedBox(height: 20),
              CustomButton(
                label: "Login",
                onPressed: () => Navigator.pushReplacementNamed(context, AppRoutes.home),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
