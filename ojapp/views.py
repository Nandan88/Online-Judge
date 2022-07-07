from sys import stdout
# from time import timezone
from datetime import datetime
# import pytz
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import subprocess, filecmp

from django.test import TestCase

from .models import Problem,Solution

# Create your views here.
def index(request):
    return  render(request,'index.html')

# @login_required
def dashboard(request):
    problems_list=Problem.objects.all()
    context={'problems_list':problems_list}
    return render(request,'dashboard.html',context)

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

# def problems(request):

def problemDetail(request,problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request,"details.html",{'problem':problem})

def submitProblem(request,problem_id):
    code1=request.POST.get("code")
    problem = get_object_or_404(Problem,pk=problem_id)
    infile='E:\Django\OJ\ojapp\\' + str(problem.code) +'.txt'

    # fin=open("E:\Django\OJ\ojapp\prob_in1.txt","w")
    fout=open("E:\Django\OJ\ojapp\prob1_out.txt","w")
    # fin.write(problem.input)
    # fin.close()
    fin1=open(infile,"r")  #input file me already input rakh diya
    # print(problem.input)
    plang=request.POST.get("languages")
    if plang=="Python":
        f=open("solution1.py","w")
        f.write(str(code1))
        f.close()
        subprocess.run(["python","solution1.py"],stdin=fin1,stdout=fout,shell=True)
    elif plang=="Cpp":
        f1=open("E:\Django\OJ\ojapp\sol.cpp","w")
        f1.write(str(code1))
        f1.close()
        subprocess.run(["g++","E:\Django\OJ\ojapp\sol.cpp","-o","sol.exe"],shell=True)
        subprocess.run([".\sol.exe"],stdin=fin1,stdout=fout,shell=True)
    fin1.close()
    fout.close()
    faout=open("E:\Django\OJ\ojapp\prob_actualout.txt","w")
    faout.write(str(problem.output))
    faout.close()
    out1="E:\Django\OJ\ojapp\prob_actualout.txt"
    out2="E:\Django\OJ\ojapp\prob1_out.txt"
    if (filecmp.cmp(out1,out2)):
        verdict='Accepted'
    else:
        verdict='Wrong Answer'
    solution=Solution()
    solution.problem=problem
    solution.verdict=verdict
    # solution.submitted_at=timezone.
    # IST = pytz.timezone('Asia/Kolkata')
    solution.submitted_at=datetime.now()
    solution.submitted_code=str(code1)
    solution.save()

    # return HttpResponseRedirect(reverse('dashboard'))
    return render(request,'verdict.html',{'solution':solution})

# def verdict(request,solution_id):
#     solution=get_object_or_404(Solution,pk=solution_id)

def leaderboard(request):
    return render(request,'leaderboard.html')

def problem1(request):
    # return HttpResponse("This is problem1")
    code1=request.POST.get("code")
    # print(code1)
    # if code1!="":
    fin=open("E:\Django\OJ\ojapp\prob_in1.txt","r")
    fout=open("E:\Django\OJ\ojapp\prob1_out.txt","w")
    plang=request.POST.get("languages")
    if plang=="Python":
        f=open("solution1.py","w")
        f.write(str(code1))
        f.close()
        subprocess.run(["python","solution1.py"],stdin=fin,stdout=fout,shell=True)
    elif plang=="Cpp":
        f1=open("E:\Django\OJ\ojapp\sol.cpp","w")
        f1.write(str(code1))
        f1.close()
        subprocess.run(["g++","E:\Django\OJ\ojapp\sol.cpp","-o","sol.exe"],shell=True)
        subprocess.run([".\sol.exe"],stdin=fin,stdout=fout,shell=True)

    fin.close()
    fout.close()
    return render(request,'problem1.html')