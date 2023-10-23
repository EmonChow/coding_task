from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import (
    authenticate,
    login as loginuser,
    logout as logoutuser,
    get_user_model,
)
from tasks.forms import todoForm, imageupload
from tasks.models import todo, image
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="login")
def home(request):
    if request.user.is_authenticated:
        user = request.user
        Todo = todo.objects.filter(user=user)
        Context = {"todo": Todo, "user": user}
        return render(request, "index.html", context=Context)


@login_required(login_url="login")
def search(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            searchtext = request.POST.get("search")
        user = request.user
        form = todoForm()
        Todo = todo.objects.filter(user=user, title__contains=searchtext)
        Context = {"form": form, "todo": Todo, "user": user}
        return render(request, "index.html", context=Context)


@login_required(login_url="login")
def filter(request, condition):
    user = request.user
    form = todoForm()
    if condition == "priority":
        Todo = todo.objects.filter(user=user).order_by("priority")
    elif condition == "creation":
        Todo = todo.objects.filter(user=user).order_by("-date")
    elif condition == "pending":
        Todo = todo.objects.filter(user=user, status="P")
    elif condition == "completed":
        Todo = todo.objects.filter(user=user, status="C")
    Context = {"form": form, "todo": Todo, "user": user}
    return render(request, "index.html", context=Context)


def login(request):
    if request.method == "GET":
        form = AuthenticationForm()
        Context = {"form": form}
        return render(request, "login.html", context=Context)
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        Context = {"form": form}
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                loginuser(request, user)
                return redirect("home")
        else:
            return render(request, "login.html", context=Context)


def signup(request):
    if request.method == "GET":
        form = UserCreationForm()
        Context = {"form": form}
        return render(request, "signup.html", context=Context)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        Context = {"form": form}
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect("login")
        else:
            return render(request, "signup.html", context=Context)


@login_required(login_url="login")
def addtodo(request):
    if request.user.is_authenticated:
        user = request.user
        form = todoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            if request.method == "POST":
                images = request.FILES.getlist("images")
                for e in images:
                    image.objects.create(todo=todo, images=e)
            # save multiple images
            return redirect("home")
        else:
            return render(
                request,
                "addtask.html",
                context={
                    "form": form,
                },
            )


def logout(request):
    logoutuser(request)
    return redirect("login")


def deletetask(request, id):
    todo.objects.get(pk=id).delete()
    return redirect("home")


def changetask(request, id, status):
    Todo = todo.objects.get(pk=id)
    Todo.status = status
    Todo.save()
    return redirect("home")


def description(request, id):
    Todo = todo.objects.get(pk=id)
    images = image.objects.filter(todo=Todo)
    print("here it should be printing!")
    print(images)
    Context = {"todo": Todo, "images": images}
    return render(request, "description.html", context=Context)


def adminpanel(request):
    Users = get_user_model()
    users = Users.objects.all()
    Context = {"users": users}
    return render(request, "adminpanel.html", context=Context)


def adminwatch(request, id):
    Users = get_user_model()
    watchperson = Users.objects.get(pk=id)
    Todo = todo.objects.filter(user=watchperson)
    Context = {"todo": Todo}
    return render(request, "adminwatch.html", context=Context)


def admindescription(request, id):
    Todo = todo.objects.get(pk=id)
    images = image.objects.filter(todo=Todo)
    print("here it should be printing!")
    print(images)
    Context = {"todo": Todo, "images": images}
    return render(request, "admindescription.html", context=Context)


def adminedit(request, condition, id, user):
    if condition == "i":
        image.objects.get(pk=id).delete()
    elif condition == "p":
        Todo = todo.objects.get(pk=user)
        if id == 3:
            Todo.priority = "1"
        elif id == 2:
            Todo.priority = "3"
        else:
            Todo.priority = "2"
        Todo.save()
    return redirect("admindescription", user)
