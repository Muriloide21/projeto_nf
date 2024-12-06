from django.db import models

class Endereco(models.Model):
    # Modelo que representa um endereço. Cada endereço possui um logradouro, um número, um bairro, uma cidade, um estado, um CEP, um país e um telefone.

    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    pais = models.CharField(max_length=50)
    telefone = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.logradouro

class Cliente(models.Model):
    # Modelo que representa um cliente. Cada cliente possui um nome, um tipo de documento (CPF ou CNPJ), um documento (CPF ou CNPJ) e um endereço.

    TIPO_DOCUMENTO = (
        ('CPF', 'CPF'),
        ('CNPJ', 'CNPJ'),
    )

    nome = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=4, choices=TIPO_DOCUMENTO)
    documento = models.CharField(max_length=14, unique=True) # cpf ou cnpj
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome 
