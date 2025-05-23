from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from supabase_client import admin_client
from authapp.utils import get_authenticated_user

def verify_patient_auth(request):
    """Helper function to verify patient authentication and role"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, JsonResponse({"error": "Authorization header missing or invalid"}, status=401)
    
    token = auth_header.split(' ')[1]
    user = get_authenticated_user(token)

    if not user or not user.id:
        return None, JsonResponse({"error": "Invalid or expired token"}, status=401)

    try:
        if not user.profile or user.profile.get('role') != 'patient':
            return None, JsonResponse({"error": "Unauthorized. Only patients can access this endpoint"}, status=403)

        return user, None
    except Exception as e:
        print(f"Auth verification error: {str(e)}")
        return None, JsonResponse({"error": "Authentication verification failed"}, status=500)

@csrf_exempt
def patient_dashboard(request):
    """Patient dashboard endpoint - returns profile and any additional dashboard data"""
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user, error_response = verify_patient_auth(request)
    if error_response:
        return error_response

    try:
        # Get patient profile using admin_client
        result = admin_client.table("patients").select("*").eq("user_id", user.id).execute()
        
        if not result.data or len(result.data) == 0:
            return JsonResponse({"error": "Patient profile not found"}, status=404)

        dashboard_data = {
            "profile": result.data[0],
            "user_id": user.id,
            "role": "patient"
        }

        return JsonResponse({
            "message": "Dashboard data retrieved successfully",
            "data": dashboard_data
        }, status=200)

    except Exception as e:
        print(f"Patient dashboard error: {str(e)}")
        return JsonResponse({"error": "Failed to retrieve dashboard data"}, status=500)

@csrf_exempt
def patient_profile(request):
    """Patient profile management endpoint - handles profile retrieval"""
    user, error_response = verify_patient_auth(request)
    if error_response:
        return error_response

    try:
        if request.method == "GET":
            # Get patient profile using admin_client
            result = admin_client.table("patients").select("*").eq("user_id", user.id).execute()
            
            if not result.data or len(result.data) == 0:
                return JsonResponse({"error": "Profile not found"}, status=404)

            return JsonResponse({
                "message": "Profile retrieved successfully",
                "profile": result.data[0]
            }, status=200)
        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)

    except Exception as e:
        print(f"Patient profile error: {str(e)}")
        return JsonResponse({"error": "Failed to process profile request"}, status=500)

@csrf_exempt
def get_patient_profile(request):
    if request.method == "GET":
        user_id = request.headers.get("user_id")
        try:
            res = admin_client.table("patients").select("*").eq("user_id", user_id).single().execute()
            profile = res.data
            return JsonResponse({"profile": profile}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def update_patient_profile(request):
    """Dedicated endpoint for updating patient profile"""
    if request.method != "PUT":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user, error_response = verify_patient_auth(request)
    if error_response:
        return error_response

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON in request body",
            "details": "Please ensure the request body contains valid JSON data"
        }, status=400)

    if not data:
        return JsonResponse({
            "error": "Empty request body",
            "details": "Please provide data to update"
        }, status=400)

    # Define updateable fields and their validation rules
    updateable_fields = {
        "full_name": str,
        "phone": str,
        "email": str,
        "gender": str,
        "date_of_birth": str,
        "emergency_contact": str
    }

    # Filter and validate update data
    update_data = {}
    validation_errors = []

    for field, value in data.items():
        if field in updateable_fields:
            if value is None:
                continue
            try:
                # Validate field type
                expected_type = updateable_fields[field]
                if not isinstance(value, expected_type):
                    validation_errors.append(f"{field} must be of type {expected_type.__name__}")
                else:
                    update_data[field] = value
            except Exception as e:
                validation_errors.append(f"Error validating {field}: {str(e)}")

    if validation_errors:
        return JsonResponse({
            "error": "Validation failed",
            "details": validation_errors
        }, status=400)

    if not update_data:
        return JsonResponse({
            "error": "No valid fields to update",
            "details": f"Allowed fields are: {', '.join(updateable_fields.keys())}"
        }, status=400)

    try:
        # Update patient profile using admin_client
        profile_result = admin_client.table("patients").update(update_data).eq("user_id", user.id).execute()
        
        if not profile_result.data:
            return JsonResponse({"error": "Failed to update patient profile"}, status=500)

        # Update users table with relevant fields using admin_client
        user_update_data = {k: v for k, v in update_data.items() if k in ["full_name", "phone", "email"]}
        if user_update_data:
            admin_client.table("users").update(user_update_data).eq("id", user.id).execute()

        return JsonResponse({
            "message": "Profile updated successfully",
            "profile": profile_result.data[0]
        }, status=200)

    except Exception as e:
        print(f"Profile update error: {str(e)}")
        return JsonResponse({
            "error": "Failed to update profile",
            "details": str(e)
        }, status=500)