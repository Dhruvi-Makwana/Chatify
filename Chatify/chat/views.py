from django.shortcuts import render


def register(request):
    return render(request, "chat/register.html")


def login(request):
    return render(request, "chat/login.html")


def chat(request):
    return render(request, "chat/chat.html")


# def websocket(request):
#     return render(request, 'chat/websocket_connection.html')
