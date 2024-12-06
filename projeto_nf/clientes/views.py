from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Cliente

app_name = "clientes"

@require_POST
def delete_cliente(request, id):
    try:
        cliente = Cliente.objects.get(id=id)
        # Deletar todas as notas fiscais relacionadas ao cliente
        notas = cliente.notas_fiscais.all()
        for nota in notas:
            nota.delete()
        cliente.delete()
    except Cliente.DoesNotExist:
        pass
    return redirect(reverse(f'{app_name}:list_clientes'))

def list_clientes(request):
    context = {
        'clientes': Cliente.objects.all()
    }
    
    return render(request, f'{app_name}/list_clientes.html', context)