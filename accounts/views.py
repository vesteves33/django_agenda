from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContact

# Create your views here.
def login(request):
    if request.method != 'POST':
      return render(request, 'accounts/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    
    login = auth.authenticate(request, username=username, password=password)

    if not login:
      messages.error(request, "Usuário ou senha incorretos")
      return render(request, 'accounts/login.html')
    else:
      auth.login(request, login)
      messages.success(request, "Login realizado com sucesso!")
      return redirect('dashboard')


def logout(request):
    auth.logout(request)
    
    return redirect('login')


def register(request):
    if request.method != 'POST':
      return render(request, 'accounts/register.html')

    # Validate the form
    name = request.POST.get('name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')

    if not name or not last_name or not email or not username or not password or not password2:
      messages.error(request, "Por favor preencha os campos")

    try:
      validate_email(email)
    except:
      messages.error(request, "Email inválido!")
      return render(request, 'accounts/register.html')


    if password != password2:
      messages.error(request, "Senhas são diferentes, por favor digite novamente")
      return render(request, 'accounts/register.html')

    if len(password) < 6:
      messages.error(request, "A senha precisa ter 6 ou mais caracteres")
      return render(request, 'accounts/register.html')

    if len(username) < 6:
      messages.error(request, "O usuário precisa ter 6 ou mais caracteres")
      return render(request, 'accounts/register.html')

    if User.objects.filter(username=username).exists():
      messages.error(request, "O usuário já está cadastrados")
      return render(request, 'accounts/register.html')
    
    if User.objects.filter(email=email).exists():
      messages.error(request, "O email já está cadastrados")
      return render(request, 'accounts/register.html')

    messages.success(request, "Cadastro realizado com sucesso!")
    new_user = User.objects.create_user(username=username, email=email, password=password, first_name=name, last_name=last_name)
    
    new_user.save()

    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
  if request.method != 'POST':
    form = FormContact()    
    return render(request, 'accounts/dashboard.html', {'form': form})

  form = FormContact(request.POST, request.FILES)

  if not form.is_valid():
    messages.error(request, "Por favor preencha os campos corretamente")
    form = FormContact(request.POST)
    return render(request, 'accounts/dashboard.html', {'form': form})

  form.save()
  messages.success(request, f"Contato { request.POST.get('name') } cadastrado com sucesso!")
  return redirect("dashboard")