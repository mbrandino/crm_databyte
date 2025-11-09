from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    data_cadastro = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Contato(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contatos')
    data = models.DateTimeField(default=timezone.now)
    assunto = models.CharField(max_length=200)
    descricao = models.TextField()
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    def __str__(self):
        return f"{self.cliente.nome} - {self.assunto}"

class Oportunidade(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='oportunidades')
    titulo = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(default=timezone.now)
    
    ETAPA_CHOICES = [
        ('prospeccao', 'Prospecção'),
        ('proposta', 'Proposta'),
        ('negociacao', 'Negociação'),
        ('fechado_ganho', 'Fechado Ganho'),
        ('fechado_perdido', 'Fechado Perdido'),
    ]
    etapa = models.CharField(max_length=20, choices=ETAPA_CHOICES, default='prospeccao')
    
    def __str__(self):
        return f"{self.cliente.nome} - {self.titulo} ({self.valor})"

class Curso(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome

class AvaliacaoCurso(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.nome} - {self.curso.nome} - Nota: {self.nota}"

class UsuarioCredencial(models.Model):
    matricula = models.CharField(max_length=20, unique=True)
    senha = models.CharField(max_length=128)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.matricula}"

class Interesse(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='interessados')
    bolsista = models.BooleanField(default=False)
    profissao = models.CharField(max_length=100)
    
    HORARIO_CHOICES = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
        ('integral', 'Integral'),
        ('fins_semana', 'Fins de Semana'),
    ]
    horario = models.CharField(max_length=20, choices=HORARIO_CHOICES)
    
    CONTATO_CHOICES = [
        ('telefone', 'Telefone'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'E-mail'),
        ('presencial', 'Presencial'),
    ]
    contato = models.CharField(max_length=20, choices=CONTATO_CHOICES)
    data_cadastro = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.nome} - {self.curso.nome}"
