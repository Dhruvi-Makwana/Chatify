from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import render


def register(request):
    return render(request, "chat/register.html")


def login(request):
    return render(request, "chat/login.html")

def chat(request):
    return render(request,"chat/chat.html")