from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from supabase_client import supabase, admin_client
from authapp.utils import get_authenticated_user

def verify_staff_auth(request):
    """Helper function to verify staff authentication and role"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        print("No Authorization header found")
        return None, JsonResponse({"error": "Authorization header missing"}, status=401)
        
    if not auth_header.startswith('Bearer '):
        print("Invalid Authorization header format")
        return None, JsonResponse({"error": "Invalid Authorization header format. Must start with 'Bearer '"}, status=401)
    
    token = auth_header.split(' ')[1]
    print(f"Verifying token: {token[:10]}...")  # Log first 10 chars of token
    
    user = get_authenticated_user(token)
    if not user:
        print("Failed to authenticate user with token")
        return None, JsonResponse({"error": "Invalid or expired token"}, status=401)

    if not user.id:
        print(f"No user ID found in authenticated user")
        return None, JsonResponse({"error": "Invalid user data"}, status=401)

    try:
        if not user.profile:
            print(f"No profile found for user {user.id}")
            return None, JsonResponse({"error": "User profile not found"}, status=404)
            
        role = user.profile.get('role')
        if role not in ['doctor', 'admin']:
            print(f"Invalid role for user {user.id}: {role}")
            return None, JsonResponse({
                "error": "Unauthorized. Only staff members can access this endpoint",
                "details": f"User role '{role}' is not authorized. Must be 'doctor' or 'admin'"
            }, status=403)

        print(f"Successfully verified staff member: {user.id} with role: {role}")
        return user, None
    except Exception as e:
        print(f"Auth verification error: {str(e)}")
        return None, JsonResponse({"error": "Authentication verification failed"}, status=500)

@csrf_exempt
def staff_dashboard(request):
    """Staff dashboard endpoint - returns profile and any additional dashboard data"""
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user, error_response = verify_staff_auth(request)
    if error_response:
        return error_response

    try:
        # Get staff profile using admin_client
        print(f"Fetching staff profile for user {user.id}")
        result = admin_client.table("staff_profiles").select("*").eq("user_id", user.id).execute()
        
        if not result.data or len(result.data) == 0:
            print(f"No staff profile found for user {user.id}")
            return JsonResponse({"error": "Staff profile not found"}, status=404)

        dashboard_data = {
            "profile": result.data[0],
            "user_id": user.id,
            "role": user.profile.get('role')
        }

        return JsonResponse({
            "message": "Dashboard data retrieved successfully",
            "data": dashboard_data
        }, status=200)

    except Exception as e:
        print(f"Staff dashboard error: {str(e)}")
        return JsonResponse({
            "error": "Failed to retrieve dashboard data",
            "details": str(e)
        }, status=500)

@csrf_exempt
def staff_profile(request):
    """Staff profile management endpoint - handles profile retrieval"""
    user, error_response = verify_staff_auth(request)
    if error_response:
        return error_response

    try:
        if request.method == "GET":
            # Get staff profile using admin_client
            print(f"Fetching staff profile for user {user.id}")
            result = admin_client.table("staff_profiles").select("*").eq("user_id", user.id).execute()
            
            if not result.data or len(result.data) == 0:
                print(f"No staff profile found for user {user.id}")
                return JsonResponse({"error": "Profile not found"}, status=404)

            return JsonResponse({
                "message": "Profile retrieved successfully",
                "profile": result.data[0]
            }, status=200)
        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)

    except Exception as e:
        print(f"Staff profile error: {str(e)}")
        return JsonResponse({
            "error": "Failed to process profile request",
            "details": str(e)
        }, status=500)

@csrf_exempt
def update_staff_profile(request):
    """Dedicated endpoint for updating staff profile"""
    if request.method != "PUT":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user, error_response = verify_staff_auth(request)
    if error_response:
        return error_response

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in request body: {str(e)}")
        return JsonResponse({
            "error": "Invalid JSON in request body",
            "details": str(e)
        }, status=400)

    if not data:
        print("Empty request body received")
        return JsonResponse({
            "error": "Empty request body",
            "details": "Please provide data to update"
        }, status=400)

    # Define updateable fields and their validation rules
    updateable_fields = {
        "full_name": str,
        "phone": str,
        "email": str,
        "department": str,
        "position": str,
        "staff_no": str,
        "branch": str
    }

    # Filter and validate update data
    update_data = {}
    validation_errors = []

    for field, value in data.items():
        if field in updateable_fields:
            if value is None or value == "":  # Handle both None and empty string
                continue
            try:
                # Validate field type
                expected_type = updateable_fields[field]
                if not isinstance(value, expected_type):
                    error_msg = f"{field} must be of type {expected_type.__name__}"
                    print(f"Validation error: {error_msg}")
                    validation_errors.append(error_msg)
                else:
                    # Trim whitespace from string values
                    if isinstance(value, str):
                        value = value.strip()
                    update_data[field] = value
            except Exception as e:
                error_msg = f"Error validating {field}: {str(e)}"
                print(error_msg)
                validation_errors.append(error_msg)

    if validation_errors:
        return JsonResponse({
            "error": "Validation failed",
            "details": validation_errors
        }, status=400)

    if not update_data:
        print("No valid fields to update")
        return JsonResponse({
            "error": "No valid fields to update",
            "details": f"Allowed fields are: {', '.join(updateable_fields.keys())}"
        }, status=400)

    try:
        # Update staff profile using admin_client
        print(f"Updating staff profile for user {user.id} with data: {update_data}")
        profile_result = admin_client.table("staff_profiles").update(update_data).eq("user_id", user.id).execute()
        
        if not profile_result.data:
            print(f"Failed to update staff profile for user {user.id}")
            return JsonResponse({"error": "Failed to update staff profile"}, status=500)

        # Update users table with relevant fields using admin_client
        user_update_data = {k: v for k, v in update_data.items() if k in ["full_name", "phone", "email"]}
        if user_update_data:
            print(f"Updating user record for user {user.id} with data: {user_update_data}")
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