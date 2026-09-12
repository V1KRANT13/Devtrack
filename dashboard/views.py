from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Problem, Task


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')

        return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)
        return redirect('/')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard(request):
    problems = Problem.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)

    total = problems.count()
    solved = problems.filter(solved=True).count()
    pending = tasks.filter(completed=False).count()

    context = {
        'total': total,
        'solved': solved,
        'pending': pending,
        'problems': problems.order_by('-created_at')[:5],
        'tasks': tasks.order_by('-created_at')[:5],
    }

    return render(request, 'dashboard.html', context)


@login_required
def problems(request):
    search = request.GET.get('search', '')

    data = Problem.objects.filter(user=request.user)

    if search:
        data = data.filter(title__icontains=search)

    return render(request, 'problems.html', {'problems': data})


@login_required
def add_problem(request):
    if request.method == 'POST':
        Problem.objects.create(
            user=request.user,
            title=request.POST['title'],
            platform=request.POST['platform'],
            difficulty=request.POST['difficulty'],
            topic=request.POST['topic'],
            solved='solved' in request.POST
        )

        return redirect('/problems/')

    return render(request, 'add_problem.html')


@login_required
def delete_problem(request, id):
    problem = get_object_or_404(Problem, id=id, user=request.user)
    problem.delete()
    return redirect('/problems/')


@login_required
def tasks(request):
    data = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html', {'tasks': data})


@login_required
def add_task(request):
    if request.method == 'POST':
        Task.objects.create(
            user=request.user,
            title=request.POST['title']
        )
        return redirect('/tasks/')

    return render(request, 'add_task.html')


@login_required
def complete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('/tasks/')


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()
    return redirect('/tasks/')