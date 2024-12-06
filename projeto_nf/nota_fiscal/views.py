from django.shortcuts import get_object_or_404, render, redirect
import xml.etree.ElementTree as ET
from .models import Boleto, NotaFiscal
from fornecedores.models import Fornecedor
from clientes.models import Cliente, Endereco
from django.urls import reverse
from django.views.decorators.http import require_POST

app_name = "nota_fiscal"

def parse_xml(xml_file):
    xml = ET.parse(xml_file)
    root = xml.getroot()
    nsNFe = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
    nf_id = root.find('.//ns:infNFe', nsNFe).attrib['Id']

    # Extraindo informações do fornecedor da nota fiscal
    xNome = root.find('ns:NFe/ns:infNFe/ns:emit/ns:xNome', nsNFe).text
    cnpj = root.find('ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFe).text
    fornecedor = {'nome': xNome, 'cnpj': cnpj}
   
    # Extraindo informações dos clientes da nota fiscal
    clientes = []
    for dest in root.findall('ns:NFe/ns:infNFe/ns:dest', nsNFe):
        xNome = dest.find('ns:xNome', nsNFe).text
        cpf = dest.find('ns:CPF', nsNFe)
        cnpj = dest.find('ns:CNPJ', nsNFe)

        # Extraindo informações do endereço do cliente
        endereco = dest.find('ns:enderDest', nsNFe)
        logradouro = endereco.find('ns:xLgr', nsNFe).text
        numero = endereco.find('ns:nro', nsNFe).text
        bairro = endereco.find('ns:xBairro', nsNFe).text
        cidade = endereco.find('ns:xMun', nsNFe).text
        estado = endereco.find('ns:UF', nsNFe).text
        cep = endereco.find('ns:CEP', nsNFe).text
        pais = endereco.find('ns:xPais', nsNFe).text
        telefone = endereco.find('ns:fone', nsNFe).text
        
        documento = cpf.text if cpf is not None else cnpj.text
        tipo_documento = 'CPF' if cpf is not None else 'CNPJ'

        endereco_json = {
            'logradouro': logradouro, 'numero': numero, 'bairro': bairro,
            'cidade': cidade, 'estado': estado, 'cep': cep, 'pais': pais, 'telefone': telefone
        }

        clientes.append({'nome': xNome, 'documento': documento, 'tipo_documento': tipo_documento, 'endereco': endereco_json})

    # Extraindo informações dos boletos da nota fiscal
    boletos = []
    for duplicata in root.findall('ns:NFe/ns:infNFe/ns:cobr/ns:dup', nsNFe):
        valor = duplicata.find('ns:vDup', nsNFe).text
        data_vencimento = duplicata.find('ns:dVenc', nsNFe).text
        boletos.append({'valor': valor, 'data_vencimento': data_vencimento}) # Adicionando informações do boleto à lista de boletos 

    return {'nf_id': nf_id, 'fornecedor': fornecedor, 'clientes': clientes, 'boletos': boletos}



def index(request):
    context = {}
    if request.method == 'POST':
        # Verificando se o usuário deseja ler um arquivo XML
        if 'read_xml' in request.POST:
            xml_data = parse_xml(request.FILES['xml_file'])
            request.session['xml_data'] = xml_data
            context['xml_data'] = xml_data

        # Verificando se o usuário deseja salvar a nota fiscal lida
        elif 'save_nf' in request.POST:
            xml_data = request.session.pop('xml_data', {})
            fornecedor, _ = Fornecedor.objects.get_or_create(nome=xml_data['fornecedor']['nome'], cnpj=xml_data['fornecedor']['cnpj'])
            nf, created = NotaFiscal.objects.get_or_create(identificador=xml_data['nf_id'], fornecedor=fornecedor)
            
            # Verificando se a nota fiscal já foi cadastrada
            if not created:
                context['error'] = 'Nota Fiscal já cadastrada'
                context['xml_data'] = xml_data
                return render(request, 'index.html', context)

            # Adicionando clientes à nota fiscal
            for cliente_data in xml_data['clientes']:
                documento = cliente_data['documento']
                try:
                    cliente_obj = Cliente.objects.get(documento=documento)
                except Cliente.DoesNotExist:
                    endereco_obj = Endereco.objects.create(**cliente_data['endereco'])
                    cliente_obj = Cliente.objects.create(documento=documento, nome=cliente_data['nome'], tipo_documento=cliente_data['tipo_documento'], endereco=endereco_obj)
                
                nf.clientes.add(cliente_obj)

            # Adicionando boletos à nota fiscal
            for boleto_data in xml_data['boletos']:
                Boleto.objects.create(valor=boleto_data['valor'], data_vencimento=boleto_data['data_vencimento'], nota_fiscal=nf)

            context['success'] = 'Nota Fiscal cadastrada com sucesso'

    return render(request, f'{app_name}/index.html', context)

@require_POST
def delete_nf(request, id):
    try:
        nf = NotaFiscal.objects.get(id=id)
        nf.delete()
    except NotaFiscal.DoesNotExist:
        pass
    return redirect(reverse(f'{app_name}:list_nfs'))


def list_nfs(request):
    context = {
        'nfs': NotaFiscal.objects.all()
    }
    return render(request, f'{app_name}/list_nfs.html', context)


def detail_nf(request, id):
    # Simplificando código:
    
    # nf =  NotaFiscal.objects.get(id=id)
    # clientes = nf.clientes.all()
    # fornecedor = nf.fornecedor
    # boletos = Boleto.objects.filter(nota_fiscal=nf)

    # context = {
    #     'nf': nf,
    #     'clientes': clientes,
    #     'boletos': boletos,
    #     'fornecedor': fornecedor
    # }

    nf = get_object_or_404(NotaFiscal, pk=id)

    context = { 'nf': nf }
    
    return render(request, f'{app_name}/detail_nf.html', context)
