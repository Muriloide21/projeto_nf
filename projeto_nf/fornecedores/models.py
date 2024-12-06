from django.db import models

class Fornecedor(models.Model):
    # Modelo que representa um fornecedor de produtos. Cada fornecedor possui um nome e um CNPJ.
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)

    def __str__(self) -> str:
        return self.nome