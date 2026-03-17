from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Tarefa

# Create your views here.
@login_required
def home(request):
    return redirect('lista')

@login_required
def lista(request):
    tarefas = Tarefa.objects.filter(usuario=request.user)
    return render(request, 'lista.html', {'tarefas': tarefas})

@login_required
def gerencia_tarefa(request):
    if request.method == 'POST':
        acao = request.POST.get('acao')
        
        if acao == 'criar':
            nome = request.POST.get('nome')
            descricao = request.POST.get('descricao')
            Tarefa.objects.create(nome=nome, descricao=descricao, usuario=request.user)
            
        elif acao == 'editar':
            tarefa_id = request.POST.get('tarefa_id')
            tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
            tarefa.nome = request.POST.get('nome')
            tarefa.descricao = request.POST.get('descricao')
            tarefa.save()
            
        elif acao == 'excluir':
            tarefa_id = request.POST.get('tarefa_id')
            tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
            tarefa.delete()
            
        elif acao == 'concluir':
            tarefa_id = request.POST.get('tarefa_id')
            tarefa = get_object_or_404(Tarefa, id=tarefa_id, usuario=request.user)
            tarefa.concluida = not tarefa.concluida
            tarefa.save()
            
        return redirect('gerencia_tarefa')

    tarefas = Tarefa.objects.filter(usuario=request.user)
    tarefa_edit = None
    
    edit_id = request.GET.get('edit_id')
    if edit_id:
        tarefa_edit = get_object_or_404(Tarefa, id=edit_id, usuario=request.user)
        
    contexto = {
        'tarefas': tarefas,
        'tarefa_edit': tarefa_edit
    }
    return render(request, 'gerencia_tarefa.html', contexto)

def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')
    return render(request, 'cadastro.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('gerencia_tarefa')
        
    return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')