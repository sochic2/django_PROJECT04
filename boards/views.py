from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required 
from .models import Board, Comment
from django.views.decorators.http import require_POST
from .forms import BoardForm, CommentForm

# Create your views here.
def index(request):
    boards = get_list_or_404(Board.objects.order_by('-pk'))
    context = {
        'boards':boards,
    }
    return render(request, 'boards/index.html', context)

@login_required
def create(request):
    # POST 요청이면 FORM 데이터를 처리한다
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            # board를 바로 저장하지 않고, 현재 user를 넣고 저장
            # 실제 DB에 반영 전까지의 단계를 진행하고, 그 중간에 user 정보를
            # request.user에서 가져와서 그 후에 저장한다.
            board = form.save(commit=False)        
            board.user = request.user
            board.save()
            return redirect('boards:detail', board.pk)
    # get 요청(혹은 다른 메서드)이면 기본 폼을 생성한다.
    else:
        form = BoardForm()
    context = {'form' : form}
    return render(request, 'boards/form.html', context)
    
def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    # 있으면 주석처리한 부분하고 똑같이 작동하고 없으면 404에러를 보여줌
    board = get_object_or_404(Board, pk=board_pk)
    comments = board.comment_set.all()
    form = CommentForm()
    context = {
        'board':board,
        'comments':comments,
        'form': form
    }
    
    return render(request, 'boards/detail.html', context)
    
    
def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
        if request.method == 'POST':
            board.delete()
            return redirect('boards:index')
        else:
            return redirect('boards:detail', board.pk)
    else:
        return redirect('boards:index')
@login_required
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
        if request.method == 'POST':
            form = BoardForm(request.POST, instance=board)  #1
            if form.is_valid():
                board = form.save()                         #2
                return redirect('boards:detail', board.pk)
        #GET 요청이면 (수정하기 버튼을 눌렀을때)
        else:
            form = BoardForm(instance=board)                #3
    else:
        return redirect('boards:index')
    context = {
        'form':form, 
        'board':board
    }
    return render(request, 'boards/form.html',context)
   
    
@require_POST
@login_required
def comment_create(request, board_pk):
    # board = get_object_or_404(Board, pk=board_pk)   쿼리문이 하나 더 늘어나니까 이걸 없애고 comment.board 방식으로.
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user         #board 넣었던 것 처럼 번호만 들어감
        comment.board_id = board_pk
        comment.save()
    return redirect('boards:detail', board_pk)

@require_POST
@login_required
def comment_delete(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('boards:detail', board_pk)
    

    
          
    
