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