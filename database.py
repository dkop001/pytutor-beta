import os
from supabase import create_client, Client

# The default template whenever a new user starts using your app
DEFAULT_USER_TEMPLATE = {
    "streak": 0,
    "xp": 0,
    "hearts": 5,
    "current_lesson_id": 0,
    "completed_lessons": []
}

def init_db(app):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    print("SUPABASE_URL exists:", bool(url))
    print("SUPABASE_KEY exists:", bool(key))

    if url and key:
        try:
            app.supabase = create_client(url, key)
            print("Supabase connected successfully")
        except Exception as e:
            print("Supabase connection failed:", e)
            app.supabase = None
    else:
        print("WARNING: Supabase URL or Key missing!")
        app.supabase = None

def get_user(user_id):
    """
    Fetch the user from the Supabase database.
    """
    from flask import current_app as app
    
    if not app.supabase:
        print("WARNING: Supabase is not initialized.")
        return DEFAULT_USER_TEMPLATE
    
    # Fetch user row
    response = app.supabase.table('users').select("*").eq("id", user_id).execute()
    
    if len(response.data) > 0:
        return response.data[0]
    else:
        # Create a new record simulating a signup flow in our Supabase table
        new_user = DEFAULT_USER_TEMPLATE.copy()
        new_user["id"] = user_id
        
        insert_response = app.supabase.table('users').insert(new_user).execute()
        
        if len(insert_response.data) > 0:
            return insert_response.data[0]
        return new_user

def update_user(user_id, updated_data):
    """
    Updates the user's progress in the database securely.
    """
    from flask import current_app as app
    
    if not app.supabase:
        return False
        
    try:
        app.supabase.table('users').update(updated_data).eq("id", user_id).execute()
        return True
    except Exception as e:
        print(f"Error updating user in Supabase: {e}")
        return False
