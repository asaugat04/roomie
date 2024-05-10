from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return HttpResponse("home")
    # return render(request,"app/signup.html")



def signup(request):
    return render(request,"app/signup.html")


def login(request):
    return render(request,"app/login.html")