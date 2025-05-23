from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from supabase_client import supabase  # assumes create_client is set up

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            email = data.get("email")
            password = data.get("password")
            full_name = data.get("full_name")
            phone = data.get("phone")
            role = data.get("role")  # 'patient', 'doctor', etc.

            if not all([email, password, full_name, phone, role]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            # 1. Register with Supabase Auth
            result = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if not result.user:
                return JsonResponse({"error": "Sign-up failed"}, status=400)

            user_id = result.user.id

            # 2. First create the base user record
            base_user = {
                "id": user_id,
                "email": email,
                "full_name": full_name,
                "phone": phone,
                "role": role
            }
            supabase.table("users").insert(base_user).execute()

            # 3. Insert into profile table
            profile_data = {
                "user_id": user_id,
                "full_name": full_name,
                "phone": phone,
                "email": email
            }

            if role == "patient":
                supabase.table("patients").insert(profile_data).execute()
            else:
                profile_data["position"] = role  # e.g., 'doctor', 'admin'
                supabase.table("staff_profiles").insert(profile_data).execute()

            return JsonResponse({"message": "Registration successful"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not all([email, password]):
                return JsonResponse({"error": "Email and password required"}, status=400)

            result = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            session = result.session
            user = result.user

            if not session:
                return JsonResponse({"error": "Login failed"}, status=401)

            return JsonResponse({
                "message": "Login successful",
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "user": {
                    "id": user.id,
                    "email": user.email
                }
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def forgot_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            supabase.auth.reset_password_email(email)
            return JsonResponse({"message": "Password reset email sent"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)
