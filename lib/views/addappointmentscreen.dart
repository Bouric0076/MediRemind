import 'package:flutter/material.dart';
import '../widgets/inputfield.dart';
import '../widgets/custombutton.dart';

// ignore: use_key_in_widget_constructors
class AddAppointmentScreen extends StatefulWidget {
  @override
  // ignore: library_private_types_in_public_api
  _AddAppointmentScreenState createState() => _AddAppointmentScreenState();
}

class _AddAppointmentScreenState extends State<AddAppointmentScreen> {
  final nameController = TextEditingController();
  DateTime? selectedDate;
  String contactMethod = 'SMS';

  Future<void> pickDateTime() async {
    final date = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime(2100),
    );

    if (date != null) {
      final time = await showTimePicker(context: context, initialTime: TimeOfDay.now());
      if (time != null) {
        setState(() {
          selectedDate = DateTime(date.year, date.month, date.day, time.hour, time.minute);
        });
      }
    }
  }

  void submit() {
    if (nameController.text.isEmpty || selectedDate == null) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Complete all fields")));
      return;
    }
    print("New appointment created for ${nameController.text}");
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Add Appointment")),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            InputField(controller: nameController, label: "Patient Name"),
            SizedBox(height: 16),
            Row(
              children: [
                Text(selectedDate == null ? "Select Date & Time" : selectedDate.toString()),
                Spacer(),
                IconButton(icon: Icon(Icons.calendar_today), onPressed: pickDateTime),
              ],
            ),
            SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: contactMethod,
              onChanged: (val) => setState(() => contactMethod = val!),
              items: ['SMS', 'WhatsApp'].map((method) => DropdownMenuItem(value: method, child: Text(method))).toList(),
            ),
            Spacer(),
            CustomButton(label: "Save", onPressed: submit),
          ],
        ),
      ),
    );
  }
}
