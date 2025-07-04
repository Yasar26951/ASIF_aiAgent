from django.shortcuts import render
from django.http  import   HttpResponse
from .forms import inputform

# Create your views here.
def hello_world(request):
    text={}
    text['context']=inputform()
    return render(request,"index.html",text)
