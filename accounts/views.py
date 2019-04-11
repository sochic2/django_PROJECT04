from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model 
from .forms import UserCustomChangeForm, UserCustomCreationForm



# Create your views here.

# model을 안만들어도 됨.. 유저 관련된거는 이미 만들어져 있어서?
# signup은 create랑 비슷  POST방식, GET방식으로 나눠서 
def signup(request):
    if request.user.is_authenticated:   # 로그인 상태인지 확인
        return redirect('boards:index')
    
    if request.method == 'POST':
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save()                          # 1 변수로 들어가고
            auth_login(request, user)                   # signup이 되고 로그인된채로 index로 이동
            return redirect('boards:index')
    else:
        form = UserCustomCreationForm()
    context = {
        'form' : form,
        
    }
    return render(request, 'accounts/auth_form.html', context)

def login(request): 
    if request.user.is_authenticated:   #로그인한사람이 다시 로그인페이지로 오면 안되니까
        return redirect('boards:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.POST.get('next') or 'boards:index')
    else:
        form = AuthenticationForm()
    context = {
            'form':form,
            'next' : request.GET.get('next', '')
    }
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
    return render(request, 'accounts/auth_form.html', context)    
    
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
    return render(request, 'accounts/auth_form.html', context)
    
    
"""
index에 게시글 작성자명 누르면 해당 프로필 페이지로 이동!
내가 쓴 모든 글 출력
내가 쓴 댓글 출력
"""
def profile(request, user_pk):
    puser = get_object_or_404(get_user_model(), pk=user_pk)
    context = {'puser':puser, }
    return render(request, 'accounts/profile.html', context)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    