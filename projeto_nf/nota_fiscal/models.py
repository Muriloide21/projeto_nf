from typing import Any
from django.db import models
from clientes.models import Cliente
from fornecedores.models import Fornecedor

class NotaFiscal(models.Model):
    # Modelo que representa uma nota fiscal. Cada nota fiscal possui um identificador único, um fornecedor e uma lista de clientes.

    identificador = models.CharField(max_length=50, unique=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    clientes = models.ManyToManyField(Cliente, related_name='notas_fiscais')

    def __str__(self) -> str:
        return f'Nota Fiscal {self.id} - {self.fornecedor}'

class Boleto(models.Model):
    # Modelo que representa um boleto. Cada boleto possui um valor, uma data de vencimento e uma nota fiscal.

    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Boleto {self.valor} - {self.data_vencimento}'
