from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, UpdateUserActiveTime
from .models import User
from .utils import validate_contact_number, set_status
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import JsonResponse
from rest_framework.serializers import ValidationError
from .constants import LOGIN_VALIDATION_ERROR_MESSAGE
from .websocket_utils import send_chat_message
from django.contrib.sessions.models import Session
from .redis import check_last_login


class RegistrationApi(APIView):
    def post(self, request):
        try:
            data = request.data.dict()
            data["mobile_number"] = validate_contact_number(data.get("mobile_number"))
            serializer = UserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as err:
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserListAPI(APIView):
    def get(self, request):
        try:
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            login_serializer = LoginSerializer(data=request.data)
            login_serializer.is_valid(raise_exception=True)
            user = authenticate(request=request, **login_serializer.validated_data)
            if user:
                login(request, user)
                user.is_online = True
                user.save()
                send_chat_message(user.id, "login")
                return Response(
                    {"login": login_serializer.data}, status=status.HTTP_200_OK
                )
            return Response(
                {"error": LOGIN_VALIDATION_ERROR_MESSAGE},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VisibilityStatusAPI(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        user.is_online = request.data.get("status").lower().strip() == "online"
        user.save()
        return Response(status=status.HTTP_200_OK)


class OnlineUsersAPI(APIView):
    def get(self, request):
        data = User.objects.filter(is_online=True, is_active=True).order_by("-id")
        return JsonResponse({"UserData": list(UserSerializer(data, many=True).data)})


class LogoutView(APIView):
    def get(self, request):
        user_session_key = request.session.session_key
        Session.objects.filter(session_key__startswith=user_session_key).delete()
        send_chat_message(set_status(request.user), "logout")
        logout(request)
        return redirect(reverse("chat:loginUI"))


class SetUserActiveTime(APIView):
    def get(self, request):
        user = User.objects.filter(username=request.user)
        check_last_login(request.user.id)
        return JsonResponse({"user": list(UpdateUserActiveTime(user, many=True).data)})
