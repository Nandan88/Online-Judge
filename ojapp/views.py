from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return  render(request,'index.html')

def problem1(request):
    # return HttpResponse("This is problem1")
    return render(request,'problem1.html')