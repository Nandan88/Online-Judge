from sys import stdout
# from time import timezone
from datetime import datetime
from webbrowser import get
# import pytz
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import subprocess, filecmp

from django.test import TestCase

from .models import Problem,Solution,Score

# If user info needed then just do request.user and current user ka instance mil jayega usse baaki info le skte like username email.

# Create your views here.
def index(request):
    return  render(request,'index.html')

# @login_required
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
        f=open("E:\Django\OJ\ojapp\solution1.py","w")
        f.write(str(code1))
        f.close()
        # docker run -it --name py_cont python
        subprocess.run(["docker","cp","E:\Django\OJ\ojapp\solution1.py","py_cont:/sol1.py"],stdin=fin1,stdout=fout,shell=True)
        subprocess.run(["docker","exec","-i","py_cont","python","sol1.py"],stdin=fin1,stdout=fout,shell=True)
    elif plang=="Cpp":
        f1=open("E:\Django\OJ\ojapp\sol.cpp","w")
        f1.write(str(code1))
        f1.close()    # docker rm container id     this to remove container (docker stop k baad ya sirf ye karna padega)
        # subprocess.run(["docker","--rm","-it","--name","comp_cpp","gcc"])
        # subprocess.run(["docker","exec","-d",ubuntu_bash touch /tmp/execWorks])
        # subprocess.run(["docker","cp","E:\Django\OJ\sol.cpp","cpp_cont",":","/sol.cpp"])
        # subprocess.run(["docker","cp","E:\Django\OJ\sol.cpp","cpp_cont:/sol.cpp"])
        # subprocess.run(["docker","cp","E:\Django\OJ\sol.cpp","cpp_cont:./sol.exe"])
        # ps=subprocess.run(["docker","attach","cpp_cont"])
        # subprocess.run(["docker","exec","g++","/sol.cpp","-o","sol.exe" ],shell=True)
        # subprocess.run(["docker","exec","-i","cpp_cont","./sol" ],stdin=fin1,stdout=fout,shell=True)
        subprocess.run(["docker","cp","E:\Django\OJ\ojapp\sol.cpp","cpp_cont:/sol.cpp"])
        subprocess.run(["docker","exec","-i","cpp_cont","g++","sol.cpp","-o","./sol" ],shell=True)
        subprocess.run(["docker","exec","-i","cpp_cont","./sol" ],stdin=fin1,stdout=fout,shell=True)
        # data=fin1.read()
        # res = bytes(data, 'utf-8')
        # ps=subprocess.run(["docker","exec","-i","cpp_cont","./sol" ],input=res,capture_output=True,shell=True)
        # subprocess.run([""])
        # ps=subprocess.run(["docker","exec","-i","cpp_cont","./sol.exe" ],input=data,capture_output=True,shell=True,universal_newlines=True)
        # ps=ps.stdout
        # print(ps)
        # subprocess.run(["g++","sol.cpp","-o","sol.exe"],shell=True)
        # subprocess.run([".\sol.exe"],stdin=fin1,stdout=fout,shell=True)
        # subprocess.run(["docker","detach","cpp_cont"])
        
        # fout=ps
        # subprocess.run(["g++","E:\Django\OJ\ojapp\sol.cpp","-o","sol.exe"],shell=True)
        # subprocess.run([".\sol.exe"],stdin=fin1,stdout=fout,shell=True)
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

# def verdict(request,solution_id):
#     solution=get_object_or_404(Solution,pk=solution_id)


# def submitProblem(request,problem_id):
#     code1=request.POST.get("code")
#     problem = get_object_or_404(Problem,pk=problem_id)
#     infile='E:\Django\OJ\ojapp\\' + str(problem.code) +'.txt'

#     # fin=open("E:\Django\OJ\ojapp\prob_in1.txt","w")
#     fout=open("E:\Django\OJ\ojapp\prob1_out.txt","w")
#     # fin.write(problem.input)
#     # fin.close()
#     fin1=open(infile,"r")  #input file me already input rakh diya
#     # print(problem.input)
#     plang=request.POST.get("languages")
#     if plang=="Python":
#         f=open("solution1.py","w")
#         f.write(str(code1))
#         f.close()
#         subprocess.run(["python","solution1.py"],stdin=fin1,stdout=fout,shell=True)
#     elif plang=="Cpp":
#         f1=open("E:\Django\OJ\ojapp\sol.cpp","w")
#         f1.write(str(code1))
#         f1.close()
#         subprocess.run(["g++","E:\Django\OJ\ojapp\sol.cpp","-o","sol.exe"],shell=True)
#         subprocess.run([".\sol.exe"],stdin=fin1,stdout=fout,shell=True)
#     fin1.close()
#     fout.close()
#     faout=open("E:\Django\OJ\ojapp\prob_actualout.txt","w")
#     faout.write(str(problem.output))
#     faout.close()
#     out1="E:\Django\OJ\ojapp\prob_actualout.txt"
#     out2="E:\Django\OJ\ojapp\prob1_out.txt"
#     if (filecmp.cmp(out1,out2)):
#         verdict='Accepted'
#     else:
#         verdict='Wrong Answer'
#     s=Solution.objects.filter(username=request.user,problem=problem,verdict='Accepted')
#     print(s.count())
#     if s.count()==0:
#         print(request.user)
#         sc=Score.objects.get(user=request.user)
#         print(sc)
#         if sc==None:
#             su=Score()
#             su.user=request.user
#             su.points=5
#             su.save()
#         else:
#             sc.points+=5
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

# # def verdict(request,solution_id):
# #     solution=get_object_or_404(Solution,pk=solution_id)

def logout(request):
    # request.user
    return redirect('http://127.0.0.1:8000/')

def submission(request):
    solution=Solution.objects.filter(username=request.user).order_by('submitted_at')
    context={'solution':solution}
    return render(request,'submission.html',context)

def subcode(request,solution_id):
    solution=get_object_or_404(Solution,pk=solution_id)
    context={'solution':solution}
    return render(request,'subcode.html',context)

def leaderboard(request):
    # score = Score.objects.all().order_by('-points').values()
    score = Score.objects.all().order_by('-points')
    
    context={'score':score}
    return render(request,'leaderboard.html',context)

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