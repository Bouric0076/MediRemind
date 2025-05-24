
import '../models/appointmentmodel.dart';

class ApiService {
  static Future<void> createAppointment(Appointment appointment) async {
    await Future.delayed(Duration(seconds: 1));
    print("Saved appointment: ${appointment.patientName}");
  }
}
