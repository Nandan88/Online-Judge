from sys import stdout
# from time import timezone
from datetime import datetime
from typing import Container
from webbrowser import get
# import pytz
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import subprocess, filecmp
from django.conf import settings
from django.test import TestCase
import docker
import sys

client=docker.from_env()
img_py='python'
img_gcc='gcc'

from .models import Problem,Solution,Score

# If user info needed then just do request.user and current user ka instance mil jayega usse baaki info le skte like username email.

# Create your views here.
def index(request):
    return  render(request,'index.html')

@login_required
def dashboard(request):
    problems_list=Problem.objects.all()
    # solution=Solution.objects.all()
    solution=[]
    for p in problems_list:
        s=Solution.objects.filter(problem=p,username=request.user,verdict='Accepted')
        if s.count()>0:
            solution.append(p)
    context={'problems_list':problems_list,'solution':solution}
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

@login_required
def problemDetail(request,problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    return render(request,"details.html",{'problem':problem})

def submitProblem(request,problem_id):
    
    # problem = get_object_or_404(Problem,pk=problem_id)

    # # fin=open("E:\Django\OJ\ojapp\prob_in1.txt","w")
    # fout=open("E:\Django\OJ\ojapp\prob1_out.txt","w")
    # # fin.write(problem.input)
    # # fin.close()
    # # print(problem.input)
    # plang=request.POST.get("languages")

    code1=request.POST.get("code")
    problem = get_object_or_404(Problem,pk=problem_id)
    fout=open(str(settings.BASE_DIR)+"/"+"ojapp\prob1_out.txt","w")
    # infile='E:\Django\OJ\ojapp\\' + str(problem.code) +'.txt'
    #fin1=open(infile,"r")  #input file me already input rakh diya
    plang=request.POST.get("languages")
    data=problem.input
    res = bytes(data, 'utf-8')
    verdict='i'
    if plang=="Python":
        f=open("solution1.py","w")
        f.write(str(code1))
        f.close()
        try:
            subprocess.run(["python","solution1.py"],input=res,stdout=fout,shell=True) # i means interactive
        except:
            verdict='Time Limit Exceeded'
            fout.write(verdict)
        # subprocess.run(["python","solution1.py"],stdin=fin1,stdout=fout,shell=True)
    elif plang=="Cpp":
        f1=open(str(settings.BASE_DIR)+"/"+'ojapp/sol.cpp',"w")
        f1.write(str(code1))
        f1.close()

        try:
            subprocess.run(["g++",str(settings.BASE_DIR)+"/"+"ojapp\sol.cpp","-o","sol.exe"],shell=True)
            subprocess.run([".\sol.exe"],input=res,stdout=fout,shell=True)
            # subprocess.run(["g++","E:\Django\OJ\ojapp\sol.cpp","-o","sol.exe"],shell=True)
            # subprocess.run([".\sol.exe"],stdin=fin1,stdout=fout,shell=True)
        except:
            verdict='Time Limit Exceeded'
            fout.write(verdict)
    # fin1.close()
    # fout.close()
    # faout=open("E:\Django\OJ\ojapp\prob_actualout.txt","w")
    # faout.write(str(problem.output))
    # faout.close()
    # out1="E:\Django\OJ\ojapp\prob_actualout.txt"
    # out2="E:\Django\OJ\ojapp\prob1_out.txt"
    # if (filecmp.cmp(out1,out2)):
    #     verdict='Accepted'
    # else:
    #     verdict='Wrong Answer'
    s=Solution.objects.filter(username=request.user,problem=problem,verdict='Accepted')
    print(s.count())
    if s.count()==0:
        print(request.user)
        sc=Score.objects.get(user=request.user)
        print(sc)
        if sc==None:
            su=Score()
            su.user=request.user
            su.points=5
            su.save()
        else:
            sc.points+=5
            sc.save()
    #     # fin1.close()
    fout.close()
    faout=open(str(settings.BASE_DIR)+"/"+"ojapp/prob_actualout.txt","w")
    faout.write(str(problem.output))
    faout.close()
    
    outp=""
    with open(str(settings.BASE_DIR)+"/"+"ojapp/prob1_out.txt") as f:
        for line in f:
            if not line.isspace():
                outp+=line
    outp.strip()       
    while(outp.endswith('\n')):
        outp=outp[:-1]
    f1= open(str(settings.BASE_DIR)+"/"+"ojapp/prob1_out.txt","w")
    f1.write(str(outp))
    f1.close()
    outp2=""
    with open(str(settings.BASE_DIR)+"/"+"ojapp/prob_actualout.txt") as f:
        for line in f:
            if not line.isspace():
                outp2+=line
    outp2.strip()     

    while(outp2.endswith('\n')):
        outp2=outp2[:-1]
    # f= open(str(settings.BASE_DIR)+"/"+"ojapp/prob_actualout.txt","w")
    # # f.write(str(outp2))
    # f.close()

    # out1=str(settings.BASE_DIR)+"/"+"ojapp/prob_actualout.txt"
    # out2=str(settings.BASE_DIR)+"/"+"ojapp/prob1_out.txt"
    if verdict!='Time Limit Exceeded':
        # if (filecmp.cmp(out1,out2)):
        if (outp==outp2):
            verdict='Accepted'
        else:
            verdict='Wrong Answer'
    s=Solution.objects.filter(username=request.user,problem=problem,verdict='Accepted')
    # print(s.count())
    if s.count()==0:
        # print(request.user)
        sc=Score.objects.get(user=request.user)
        # print(sc)
        if sc==None:
            su=Score()
            su.user=request.user
            if verdict=='Accepted':
                su.points=5
            else:
                su.points=0
            su.save()
        else:
            if verdict=='Accepted':
                sc.points+=5
            sc.save()
    solution=Solution()
    solution.username=request.user
    solution.problem=problem
    solution.verdict=verdict
    # solution.submitted_at=timezone.
    # IST = pytz.timezone('Asia/Kolkata')
    solution.submitted_at=datetime.now()
    solution.submitted_code=str(code1)
    solution.save()

    # return HttpResponseRedirect(reverse('dashboard'))
    return render(request,'verdict.html',{'solution':solution})
    

# @login_required
# def submitProblem(request,problem_id):
#     code1=request.POST.get("code")
#     problem = get_object_or_404(Problem,pk=problem_id)
#     fout=open(str(settings.BASE_DIR)+"/"+"ojapp\prob1_out.txt","w")
#     plang=request.POST.get("languages")
#     data=problem.input
#     res = bytes(data, 'utf-8')
#     verdict='i'
#     if plang=="Python":
#         f=open(str(settings.BASE_DIR)+"/"+"ojapp/solution1.py","w")
#         f.write(str(code1))
#         f.close()
#         # docker rm py_cont    # This will remove previous container with this name
#         # docker run -it --name py_cont python
#         # container should be running ans its name should be py_cont ,use above command 
#             # docker run is equals create+start
#             # Now container will be created automatically if running or not created
#         try:
#             container:Container=client.containers.get('py_cont')
#             if container.status!='running':
#                 container.start()
#         except docker.errors.NotFound:
#             container=client.containers.run(img_py,detach=True,tty=True,name='py_cont')
#         try:
#             subprocess.run(["docker","cp",str(settings.BASE_DIR)+"/"+"ojapp/solution1.py","py_cont:/sol1.py"],shell=True) # copy file
#             subprocess.run(["docker","exec","-i","py_cont","python","sol1.py"],input=res,stdout=fout,shell=True,timeout=2) # i means interactive
#             subprocess.run(["docker","exec","py_cont","rm","-rf","sol1.py"]) # removing file 
#         except:
#             verdict='Time Limit Exceeded'
#             fout.write(verdict)
#     elif plang=="Cpp":
#         # settings.B
#         f1=open(str(settings.BASE_DIR)+"/"+'ojapp/sol.cpp',"w")
#         f1.write(str(code1))
#         f1.close()    
#         try:
#             container:Container=client.containers.get('cpp_cont')
#             if container.status!='running':
#                 container.start()
#         except docker.errors.NotFound:
#             container=client.containers.run(img_gcc,detach=True,tty=True,name='cpp_cont')
#         try:
#             subprocess.run(["docker","cp",str(settings.BASE_DIR)+"/"+"ojapp/sol.cpp","cpp_cont:/sol.cpp"])
#             subprocess.run(["docker","exec","-i","cpp_cont","g++","sol.cpp","-o","./sol" ],shell=True,timeout=2)
#             subprocess.run(["docker","exec","-i","cpp_cont","./sol" ],input=res,stdout=fout,shell=True,timeout=2)
#             subprocess.run(["docker","exec","cpp_cont","rm","-rf","sol.cpp"])
#             subprocess.run(["docker","exec","cpp_cont","rm","-rf","sol"])
#         except:
#             verdict='Time Limit Exceeded'
#             fout.write(verdict)

#     # fin1.close()
#     fout.close()
#     faout=open(str(settings.BASE_DIR)+"/"+"ojapp/prob_actualout.txt","w")
#     faout.write(str(problem.output))
#     faout.close()
    
#     outp=""
#     with open(str(settings.BASE_DIR)+"/"+"ojapp/prob1_out.txt") as f:
#         for line in f:
#             if not line.isspace():
#                 outp+=line
#     outp.strip()       
#     while(outp.endswith('\n')):
#         outp=outp[:-1]
#     f1= open(str(settings.BASE_DIR)+"/"+"ojapp/prob1_out.txt","w")
#     f1.write(str(outp))
#     f1.close()
#     outp2=""
#     with open(str(settings.BASE_DIR)+"/"+"ojapp/prob_actualout.txt") as f:
#         for line in f:
#             if not line.isspace():
#                 outp2+=line
#     outp2.strip()     

#     while(outp2.endswith('\n')):
#         outp2=outp2[:-1]
#     # f= open(str(settings.BASE_DIR)+"/"+"ojapp/prob_actualout.txt","w")
#     # # f.write(str(outp2))
#     # f.close()

#     # out1=str(settings.BASE_DIR)+"/"+"ojapp/prob_actualout.txt"
#     # out2=str(settings.BASE_DIR)+"/"+"ojapp/prob1_out.txt"
#     if verdict!='Time Limit Exceeded':
        
#         # if (filecmp.cmp(out1,out2)):
#         if (outp==outp2):
#             verdict='Accepted'
#         else:
#             verdict='Wrong Answer'
#     s=Solution.objects.filter(username=request.user,problem=problem,verdict='Accepted')
#     # print(s.count())
#     if s.count()==0:
#         # print(request.user)
#         sc=Score.objects.get(user=request.user)
#         # print(sc)
#         if sc==None:
#             su=Score()
#             su.user=request.user
#             if verdict=='Accepted':
#                 su.points=5
#             else:
#                 su.points=0
#             su.save()
#         else:
#             if verdict=='Accepted':
#                 sc.points+=5
#             sc.save()
#     solution=Solution()
#     solution.username=request.user
#     solution.problem=problem
#     solution.verdict=verdict
#     # solution.submitted_at=timezone.
#     # IST = pytz.timezone('Asia/Kolkata')
#     solution.submitted_at=datetime.now()
#     solution.submitted_code=str(code1)
#     solution.save()

#     # return HttpResponseRedirect(reverse('dashboard'))
#     return render(request,'verdict.html',{'solution':solution})


@login_required
def logout(request):
    # request.user
    return redirect('home')

@login_required
def submission(request):
    solution=Solution.objects.filter(username=request.user).order_by('submitted_at')
    context={'solution':solution}
    return render(request,'submission.html',context)

@login_required
def subcode(request,solution_id):
    solution=get_object_or_404(Solution,pk=solution_id)
    context={'solution':solution}
    return render(request,'subcode.html',context)

@login_required
def leaderboard(request):
    # score = Score.objects.all().order_by('-points').values()
    score = Score.objects.all().order_by('-points')
    
    context={'score':score}
    return render(request,'leaderboard.html',context)
