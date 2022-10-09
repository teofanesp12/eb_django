from django.shortcuts import render, redirect

from militares.models import Militar

# Create your views here.
def access_login(request):
    context = {}
    # next = request.GET.get('next', '/')

    if request.POST:
        tipo = request.POST.get('type')
        username = request.POST.get('username')
        password = request.POST.get('password')
        militar = None
        try:
            if tipo == 'cpf':
                militar = Militar.objects.get(cpf=username)
            elif tipo == 'rg':
                militar = Militar.objects.get(rg=username)
            elif tipo == 'numero':
                militar = Militar.objects.get(numero=username)
        except Exception:
            militar = None

        if not militar:
            return redirect('militar:militar-create_militar-view')

        response = redirect(militar)
        response.set_cookie('chave', militar.pk)

        return response

    return render(request, 'access/login.html', context)

def access_logout(request):
    context = {}
    return render(request, 'access/logout.html', context)