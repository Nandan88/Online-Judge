from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import subprocess

# Create your views here.
def index(request):
    return  render(request,'index.html')

# @login_required
def dashboard(request):
    return render(request,'dashboard.html')

def register(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
        form=UserCreationForm()
        # return render(request,'registration.html',{'form':form})
    return render(request,'registration/register.html',{'form':form})


def problem1(request):
    # return HttpResponse("This is problem1")
    code1=request.POST.get("code")
    
    print(code1)
    return render(request,'problem1.html')