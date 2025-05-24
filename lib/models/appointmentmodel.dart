class Appointment {
  final String id;
  final String patientName;
  final DateTime dateTime;
  final String contactMethod; // e.g., "WhatsApp" or "SMS"

  Appointment({
    required this.id,
    required this.patientName,
    required this.dateTime,
    required this.contactMethod,
  });
}