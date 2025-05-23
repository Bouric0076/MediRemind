from supabase_client import supabase

def get_authenticated_user(access_token):
    try:
        response = supabase.auth.get_user(access_token)
        return response.user
    except Exception as e:
        return None
    
def get_user_by_id(user_id):
    try:
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        return None
    
def get_user_by_email(email):
    try:
        response = supabase.table("users").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        return None

    

