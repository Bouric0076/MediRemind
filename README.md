# MediRemind Backend

A robust Django-based backend system for managing medical appointments, notifications, and user management. This system integrates with Supabase for data storage and provides multiple notification channels including Web Push and WhatsApp.

## Tech Stack

- **Framework**: Django 4.2+
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth
- **Notification Services**:
  - Web Push Notifications (using pywebpush)
  - WhatsApp Messaging (via Twilio)
- **Language**: Python 3.8+
- **API Style**: RESTful

## Project Structure

```
mediremind_backend/
├── authapp/                 # Authentication and user management
├── appointments/           # Appointment scheduling and management
├── notifications/         # Push notifications and messaging
├── patients/             # Patient profile management
├── staff_profiles/       # Staff/Doctor profile management
├── mediremind_backend/   # Project settings and main configuration
├── supabase_client.py    # Supabase client configuration
├── manage.py             # Django management script
└── requirements.txt      # Project dependencies
```

## Features

### 1. Authentication System
- User registration with role-based profiles (Patient/Doctor/Admin)
- JWT-based authentication using Supabase Auth
- Secure password management
- Profile management for both patients and medical staff

### 2. Appointment Management
- Schedule/Reschedule appointments
- Appointment confirmation and cancellation
- Availability checking for both doctors and patients
- Appointment history and upcoming appointments
- Automated reminders and notifications

### 3. Notification System
- **Web Push Notifications**
  - Real-time appointment updates
  - Reminder notifications
  - Status changes
- **WhatsApp Notifications**
  - Appointment reminders (24h before)
  - Confirmation messages
  - Rescheduling notifications
  - Cancellation updates

### 4. Profile Management
- Patient profile management
- Staff profile management
- Medical history tracking
- Appointment preferences

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd mediremind_backend
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory with the following variables:
   ```env
   # Django settings
   DJANGO_SECRET_KEY=your_django_secret_key
   DJANGO_DEBUG=True

   # Supabase settings
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

   # Twilio settings (for WhatsApp)
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_WHATSAPP_FROM=your_twilio_whatsapp_number

   # Web Push settings
   VAPID_PUBLIC_KEY=your_vapid_public_key
   VAPID_PRIVATE_KEY=your_vapid_private_key
   VAPID_ADMIN_EMAIL=your_admin_email
   ```

5. **Generate VAPID Keys**
   ```bash
   python mediremind_backend/notifications/generate_vapid_keys.py
   ```

6. **Database Setup**
   - Create necessary tables in Supabase using the provided SQL migrations
   - Set up Row Level Security (RLS) policies

7. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication Endpoints
- `POST /auth/register/` - Register new user
- `POST /auth/login/` - User login
- `POST /auth/logout/` - User logout
- `POST /auth/forgot-password/` - Password reset request

### Patient Endpoints
- `GET /patients/dashboard/` - Patient dashboard data
- `GET /patients/profile/` - Get patient profile
- `PUT /patients/profile/update/` - Update patient profile
- `GET /patients/appointments/` - List patient appointments

### Staff Endpoints
- `GET /staff/dashboard/` - Staff dashboard data
- `GET /staff/profile/` - Get staff profile
- `PUT /staff/profile/update/` - Update staff profile
- `GET /staff/appointments/` - List staff appointments

### Appointment Endpoints
- `POST /appointments/schedule/` - Schedule new appointment
- `PUT /appointments/{id}/update/` - Update appointment
- `DELETE /appointments/{id}/cancel/` - Cancel appointment
- `POST /appointments/{id}/confirm/` - Confirm appointment
- `POST /appointments/{id}/reschedule/` - Request reschedule

### Notification Endpoints
- `POST /notifications/subscribe/` - Subscribe to push notifications
- `DELETE /notifications/unsubscribe/` - Unsubscribe from notifications
- `GET /notifications/vapid-public-key/` - Get VAPID public key

## Database Schema

### Users Table
```sql
create table users (
    id uuid references auth.users primary key,
    email text unique,
    full_name text,
    phone text,
    role text check (role in ('patient', 'doctor', 'admin')),
    created_at timestamp with time zone default timezone('utc'::text, now())
);
```

### Patients Table
```sql
create table patients (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references users(id),
    full_name text,
    phone text,
    email text,
    date_of_birth date,
    gender text,
    emergency_contact text,
    created_at timestamp with time zone default timezone('utc'::text, now())
);
```

### Staff Profiles Table
```sql
create table staff_profiles (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references users(id),
    full_name text,
    phone text,
    email text,
    position text,
    department text,
    staff_no text unique,
    created_at timestamp with time zone default timezone('utc'::text, now())
);
```

### Appointments Table
```sql
create table appointments (
    id uuid primary key default uuid_generate_v4(),
    patient_id uuid references users(id),
    doctor_id uuid references users(id),
    date date,
    time time,
    type text,
    status text,
    notes text,
    location_text text,
    created_at timestamp with time zone default timezone('utc'::text, now()),
    updated_at timestamp with time zone default timezone('utc'::text, now())
);
```

### Push Subscriptions Table
```sql
create table push_subscriptions (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references users(id),
    endpoint text not null,
    p256dh text not null,
    auth text not null,
    created_at timestamp with time zone default timezone('utc'::text, now()),
    updated_at timestamp with time zone default timezone('utc'::text, now())
);
```

## Security Considerations

1. **Authentication**
   - JWT-based authentication using Supabase Auth
   - Secure password hashing
   - Token expiration and refresh mechanisms

2. **Authorization**
   - Role-based access control
   - Row Level Security in Supabase
   - Endpoint permission checks

3. **Data Protection**
   - HTTPS for all API endpoints
   - Encrypted storage of sensitive data
   - Secure handling of VAPID keys

4. **API Security**
   - CORS configuration
   - Rate limiting
   - Input validation and sanitization

## Error Handling

The API uses standard HTTP status codes and returns error responses in the following format:
```json
{
    "error": "Error message",
    "details": "Detailed error description",
    "code": "ERROR_CODE"
}
```

## Automated Tasks

### Appointment Reminders
Configure a cron job to run the reminder script:
```bash
0 8 * * * /path/to/mediremind/scripts/send_reminders.sh >> /path/to/logs/reminders.log 2>&1
```

### Manual Testing
Test notifications manually:
```bash
python manage.py trigger_reminder <appointment_id>
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@mediremind.com or create an issue in the repository.

---

# MediRemind Frontend (Flutter)

## Overview

MediRemind's frontend is a cross-platform Flutter application that provides a seamless experience for both patients and staff (doctors/admins). It connects to the Django backend via REST APIs, supports role-based dashboards, and offers a modern, user-friendly interface.

## Features

- **Authentication:** Secure login/register with role-based navigation.
- **Role-based Dashboards:** Separate flows and screens for patients and staff.
- **Appointment Management:** Book, view, cancel, and manage appointments.
- **Profile Management:** View and edit user profiles.
- **Notifications:** Real-time reminders and updates (via backend).
- **Modern UI:** Consistent, beautiful design across all screens.

## App Structure

```
lib/
├── core/           # Theme, constants, and app-wide config
├── models/         # Data models (User, Appointment, Doctor, etc.)
├── services/       # API service for backend communication
├── widgets/        # Reusable UI components (buttons, cards, fields)
├── views/          # Screens (login, dashboard, appointment, profile, etc.)
├── routes/         # App routes and navigation
└── main.dart       # App entry point
```

## Main Workflows

### 1. Authentication Flow
- User opens the app and is greeted with a modern onboarding/welcome screen.
- User can **Sign In** or **Create Account**.
- On login/register, the app authenticates with the backend and retrieves the user's role.
- The user is redirected to the appropriate dashboard (patient or staff).

### 2. Patient Workflow
- **Dashboard:** Shows profile summary and upcoming appointments.
- **Book Appointment:** Patient can request a new appointment by selecting type, doctor, date, and time.
- **View Appointments:** List of all appointments with details and status.
- **Cancel Appointment:** Patient can cancel upcoming appointments.
- **Profile:** View and edit personal information.

### 3. Staff Workflow
- **Dashboard:** Shows staff profile, quick actions, and recent appointments.
- **Schedule Appointment:** Staff can schedule appointments for patients.
- **Manage Appointments:** View, complete, or cancel appointments.
- **Add Patient:** (Future) Add new patients to the system.
- **Profile:** View and edit staff information.

### 4. Navigation & Routing
- Uses named routes for all screens.
- Navigation is role-aware and context-sensitive.
- All screens use a consistent AppBar, background, and spacing.

## UI/UX Logic

- **Theme:** Uses a custom theme with a vivid blue primary color, soft backgrounds, rounded cards, and modern typography.
- **Widgets:** All forms use custom InputField and CustomButton widgets for consistency.
- **Cards:** Appointments, profiles, and quick actions are displayed in rounded, shadowed cards.
- **Responsiveness:** Layouts adapt to different screen sizes and platforms (mobile, web, desktop).
- **Error Handling:** All API errors are shown with friendly messages and retry options.

## How the Application Works (End-to-End)

1. **User Registration & Login**
   - User registers or logs in via the Flutter app.
   - Credentials are sent to the Django backend, which authenticates and returns a JWT token and user role.

2. **Role-Based Navigation**
   - The app stores the token securely and fetches the user's role.
   - Patients see the patient dashboard; staff see the staff dashboard.

3. **Appointments**
   - Patients can request appointments; staff can schedule/manage them.
   - All appointment actions (create, update, cancel) are sent to the backend via REST API.
   - Appointment status and details are always up-to-date.

4. **Profile Management**
   - Users can view and edit their profile.
   - Changes are sent to the backend and reflected in the app.

5. **Notifications**
   - The backend sends reminders and updates via push/WhatsApp.
   - The app displays real-time status and reminders.

6. **Logout**
   - User can log out, which clears the session and returns to the login screen.

## Running the Frontend

1. **Install Flutter** (https://flutter.dev/docs/get-started/install)
2. **Clone the repository** and navigate to the frontend directory.
3. **Install dependencies:**
   ```bash
   flutter pub get
   ```
4. **Run the app:**
   ```bash
   flutter run
   ```
   - For web: `flutter run -d chrome`
   - For desktop: `flutter run -d windows` (or macos/linux)

5. **Configure API endpoints** in `lib/core/constants.dart` if your backend is not running on localhost.

## Contribution

- All UI code follows best practices for readability and maintainability.
- New screens and features should use the existing theme and widgets for consistency. 