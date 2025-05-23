from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from supabase_client import supabase, admin_client
from authapp.utils import get_authenticated_user

@csrf_exempt
def staff_dashboard(request):
    if request.method == "GET":
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({"error": "Authorization header missing or invalid"}, status=401)
        
        token = auth_header.split(' ')[1]
        user = get_authenticated_user(token)

        if not user:
            return JsonResponse({"error": "Invalid or expired token"}, status=401)

        try:
            # First get the user's role
            user_result = admin_client.table("users").select("role").eq("id", user.id).execute()
            if not user_result.data:
                return JsonResponse({"error": "User not found"}, status=404)
            
            if user_result.data[0]['role'] != 'doctor' and user_result.data[0]['role'] != 'admin':
                return JsonResponse({"error": "Unauthorized. Only staff members can access this endpoint"}, status=403)

            # Then get the staff profile
            result = admin_client.table("staff_profiles").select("*").eq("user_id", user.id).execute()
            
            if result.data and len(result.data) > 0:
                return JsonResponse({
                    "message": "Staff dashboard data retrieved successfully",
                    "profile": result.data[0]
                }, status=200)
            else:
                return JsonResponse({"error": "Staff profile not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)
