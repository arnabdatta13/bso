# decorators.py
from django.shortcuts import redirect

def admin_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_user_id'):
            return redirect('login')  # Redirect to login if not logged in
        return view_func(request, *args, **kwargs)
    return wrapper
