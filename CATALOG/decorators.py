from django.shortcuts import redirect

from .models import USER_TYPE_CHOICES


def allowed_users(allowed_types=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            for type in USER_TYPE_CHOICES:
                if type[0] == request.user.type:
                    if type[1] in allowed_types:
                        return view_func(request, *args, **kwargs)
                    else:
                        return redirect('/CATALOG/not-permission/')
                    break
            
        return wrapper_func
    return decorator