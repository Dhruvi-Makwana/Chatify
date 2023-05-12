from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, GetUserDataSerializer
from .models import User
from .utils import validate_contact_number
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import JsonResponse
from rest_framework.serializers import ValidationError


class RegistrationApi(APIView):
    def post(self, request):
        try:
            data = request.data.dict()
            data["mobile_number"] = validate_contact_number(data.get("mobile_number"))

            serializer = UserSerializer(data=data)  # add block except validation as e
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as err:
            print(f"hiiiiiiii {str(err)}")
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
            login_serializer.is_valid()
            user = authenticate(request=request, **login_serializer.validated_data)

            if user:
                login(request, user)
                return Response(
                    {"login": login_serializer.data}, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "enter a valid username or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VisibilityStatusAPI(APIView):
    def post(self, request, *args, **kwargs):

        data = request.data
        user = request.user
        data.get("status").lower().strip() == "online"
        user.is_online = data.get("status").lower().strip() == "online"
        user.save()
        return Response(status=status.HTTP_200_OK)


class OnlineUserAPI(APIView):
    def get(self, request):
        data = User.objects.filter(is_online=True).order_by("-id")
        return JsonResponse(
            {"UserData": list(GetUserDataSerializer(data, many=True).data)}
        )


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect(reverse("chat:loginUI"))
