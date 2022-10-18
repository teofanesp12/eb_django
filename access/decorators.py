from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
# from militares.models import Militares

def login_access_required(function):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            one = request
            try:
                is_authenticated = request.user.is_authenticated
            except:
                kwargs['pk'] = request.get_object().pk
                request = args[0]
                is_authenticated = request.user.is_authenticated
                # args = ()
            if not is_authenticated:
                if request.COOKIES.get('chave'):
                    chave = request.COOKIES.get('chave')
                    # m = Militares.objects.get(kwargs.get('pk'))
                    if str(chave) == str(kwargs.get('pk')):
                        return view_func(one, *args, **kwargs)
                    # verificamos se esta igual ao Militar
                    messages.add_message(request, messages.WARNING, 'Seu login não é autorizado para acessar esse cadastro!')
                    return redirect('access:access-login-view')
                else:
                    messages.add_message(request, messages.WARNING, 'Não realizou o login!')
                    return redirect('access:access-login-view')
            else:
                return view_func(one, *args, **kwargs)
        return _wrapped_view
    if function:
        return decorator(function)
    return decorator