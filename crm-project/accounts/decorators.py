from django.shortcuts import redirect


def unauthenticated_user(my_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return my_func(request, *args, **kwargs)
    return wrapper


def admin_required(my_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return my_func(request, *args, **kwargs)
        return redirect('profile')
    return wrapper
# def admin_only(my_func):
#     def wrapper(request, *args, **kwargs):
#         group = None
#         if request.user.groups.exists():
#             group = request.user.groups.all()[0].name
#         if group == 'customer':
#             return redirect('profile')
#         if group == 'admin':
#             return my_func(request, *args, **kwargs)
#     return wrapper