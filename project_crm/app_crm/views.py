from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cliente, Contato, Oportunidade, Curso, AvaliacaoCurso, UsuarioCredencial, Interesse
from django.db.models import Sum, Avg

def home(request):
    total_clientes = Cliente.objects.filter(ativo=True).count()
    total_oportunidades = Oportunidade.objects.count()
    valor_total = Oportunidade.objects.filter(etapa='fechado_ganho').aggregate(Sum('valor'))['valor__sum'] or 0
    
    context = {
        'total_clientes': total_clientes,
        'total_oportunidades': total_oportunidades,
        'valor_total': valor_total,
    }
    return render(request, 'usuarios/home.html', context)

def lista_clientes(request):
    clientes = Cliente.objects.filter(ativo=True)
    return render(request, 'usuarios/clientes.html', {'clientes': clientes})

def detalhe_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    contatos = cliente.contatos.all().order_by('-data')
    oportunidades = cliente.oportunidades.all().order_by('-data_criacao')
    
    context = {
        'cliente': cliente,
        'contatos': contatos,
        'oportunidades': oportunidades,
    }
    return render(request, 'usuarios/detalhe_cliente.html', context)

def adicionar_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        empresa = request.POST.get('empresa')
        
        cliente = Cliente(nome=nome, email=email, telefone=telefone, empresa=empresa)
        cliente.save()
        
        messages.success(request, 'Cliente adicionado com sucesso!')
        return redirect('lista_clientes')
    
    return render(request, 'usuarios/adicionar_cliente.html')

def pesquisa(request):
    # Não precisamos mais buscar cursos do banco de dados pois estão fixos no template
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        curso_id = request.POST.get('curso')
        nota = request.POST.get('nota')
        comentario = request.POST.get('comentario')
        
        # Buscar o curso pelo ID ou criar se não existir
        curso, created = Curso.objects.get_or_create(
            id=curso_id,
            defaults={
                'nome': obter_nome_curso(curso_id),
                'descricao': f'Curso de {obter_nome_curso(curso_id)}',
                'ativo': True
            }
        )
        
        avaliacao = AvaliacaoCurso(
            nome=nome,
            email=email,
            curso=curso,
            nota=nota,
            comentario=comentario
        )
        avaliacao.save()
        
        messages.success(request, 'Avaliação enviada com sucesso! Obrigado pela sua participação.')
        return redirect('pesquisa')
    
    return render(request, 'usuarios/pesquisa.html')

def obter_nome_curso(curso_id):
    cursos = {
        '1': 'Excel Avançado',
        '2': 'Informática',
        '3': 'Hardware e Redes',
        '4': 'Designer Gráfico',
        '5': 'Administração',
        '6': 'Inglês'
    }
    return cursos.get(curso_id, 'Curso Desconhecido')

def autenticacao(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        senha = request.POST.get('senha')

        if not matricula or not senha:
            messages.error(request, 'Matrícula e senha são obrigatórias.')
            return render(request, 'usuarios/autenticacao.html')

def interesse(request):
    cursos = Curso.objects.filter(ativo=True)
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        curso_id = request.POST.get('curso')
        bolsista = request.POST.get('bolsista') == 'true'
        profissao = request.POST.get('profissao')
        horario = request.POST.get('horario')
        contato = request.POST.get('contato')
        
        # Buscar o curso
        curso = get_object_or_404(Curso, id=curso_id)
        
        # Criar registro de interesse
        interesse_obj = Interesse(
            nome=nome,
            telefone=telefone,
            email=email,
            curso=curso,
            bolsista=bolsista,
            profissao=profissao,
            horario=horario,
            contato=contato
        )
        interesse_obj.save()
        
        messages.success(request, 'Interesse registrado com sucesso! Veja o relatório de contatos.')
        return redirect('controle_contatos')
    
    context = {'cursos': cursos}
    return render(request, 'usuarios/interesse.html', context)

def controle_contatos(request):
    interesses = Interesse.objects.all().order_by('-data_cadastro')
    
    context = {'interesses': interesses}
    return render(request, 'usuarios/controle_contatos.html', context)

def autenticacao(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        senha = request.POST.get('senha')

        # Validar credenciais no banco de dados
        valido = UsuarioCredencial.objects.filter(
            matricula=matricula,
            senha=senha,
            ativo=True
        ).exists()

        if not valido:
            messages.error(request, 'Credenciais inválidas. Verifique matrícula e senha.')
            return render(request, 'usuarios/autenticacao.html')

        # Autenticação bem-sucedida: registra a matrícula na sessão e redireciona
        request.session['matricula'] = matricula
        messages.success(request, 'Autenticação realizada com sucesso!')
        return redirect('pesquisa')

    return render(request, 'usuarios/autenticacao.html')