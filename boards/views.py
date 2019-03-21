from django.shortcuts import render, redirect, get_object_or_404
from .models import Board
from .forms import BoardForm

# Create your views here.
def index(request):
    boards = Board.objects.order_by('-pk')
    context = {'boards':boards}
    return render(request, 'boards/index.html', context)

def create(request):
    # POST 요청이면 FORM 데이터를 처리한다
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save()    
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
    
    context = {'board':board}
    return render(request, 'boards/detail.html', context)
    
def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        board.delete()
        return redirect('boards:index')
    else:
        return redirect('boards:detail', board.pk)

def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)  #1
        if form.is_valid():
            board = form.save()                         #2
            return redirect('boards:detail', board.pk)
    #GET 요청이면 (수정하기 버튼을 눌렀을때)
    else:
        form = BoardForm(instance=board)                #3
    context = {'form':form, 'board':board}
    return render(request, 'boards/form.html',context)