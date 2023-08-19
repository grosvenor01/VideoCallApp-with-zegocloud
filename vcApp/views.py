from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required

from .models import *
# Create your views here.
def index(request):
    return render(request,"index.html")
def register(request):
    if request.method=="POST":
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        email=request.POST["email"]
        if request.POST["password1"]==request.POST["password2"]:
            if User.objects.filter(email=email).exists():
                return render(request, 'register.html', {'error': 'User with this email already exists.'})
            else:
                user=User.objects.create(username=email,first_name=first_name,last_name=last_name,email=email,password=request.POST["password1"])
                user.set_password(request.POST["password1"])
                user.save()
                return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})
    return render(request,'register.html')
def login_view(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            return render(request, 'login.html', {'error': "Invalid credentials. Please try again."})
    return render(request, 'login.html')
def logoute(request):
    logout(request)
    return redirect('login_view')
@login_required(login_url='/login/')
def dashboard(request):
    return render(request,'dashboard.html',{'name':request.user.first_name})
@login_required(login_url='/login/')
def videocall(request):
    return render(request, "videocalling.html",{"name":request.user.last_name+" "+request.user.first_name})
@login_required(login_url='/login/')
def join_meeting(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID="+roomID)
    return render(request,'join.html')