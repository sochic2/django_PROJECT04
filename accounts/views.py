from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from .forms import UserCustomChangeForm


# Create your views here.

# model을 안만들어도 됨.. 유저 관련된거는 이미 만들어져 있어서?
# signup은 create랑 비슷  POST방식, GET방식으로 나눠서 
def signup(request):
    if request.user.is_authenticated:   # 로그인 상태인지 확인
        return redirect('boards:index')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()                          # 1 변수로 들어가고
            auth_login(request, user)                   # signup이 되고 로그인된채로 index로 이동
            return redirect('boards:index')
    else:
        form = UserCreationForm()
    context = {'form' : form}
    return render(request, 'accounts/signup.html', context)

def login(request): 
    if request.user.is_authenticated:   #로그인한사람이 다시 로그인페이지로 오면 안되니까
        return redirect('boards:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('boards:index')
    else:
        form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'accounts/login.html', context)
    
def logout(request):
    auth_logout(request)
    return redirect('boards:index')
    
def delete(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
    return redirect('boards:index')
    
def edit(request):
    if request.method == 'POST':
        # 수정 로직 진행
        form = UserCustomChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('boards:index')
    else:
        form = UserCustomChangeForm(instance=request.user)
    context = {'form':form, }
    return render(request, 'accounts/edit.html', context)    
    
def change_password(request):
    if request.method=='POST':
        form = PasswordChangeForm(request.user, request.POST)   # 인자 순서 유의
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('boards:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form, }
    return render(request, 'accounts/change_password.html', context)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    