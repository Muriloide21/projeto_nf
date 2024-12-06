from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Fornecedor

app_name = "fornecedores"

@require_POST
def delete_fornecedor(request, id):
    try:
        fornecedor = Fornecedor.objects.get(id=id)
        fornecedor.delete()
    except Fornecedor.DoesNotExist:
        pass
    return redirect(reverse(f'{app_name}:list_fornecedores'))

def list_fornecedores(request):
    context = {
        'fornecedores': Fornecedor.objects.all()
    }
    return render(request, f'{app_name}/list_fornecedores.html', context)