from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, GetUserDataSerializer
from .models import User
from .utils import set_contact_number
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import JsonResponse
from django.http import HttpResponseRedirect


class RegistrationApi(APIView):
    def post(self, request):

        try:

            serializer = UserSerializer(data=set_contact_number(request.data))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )


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
            else:
                return Response(
                    {"error": "enter a valid username and password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserOnlineAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        data = request.data
        user = request.user
        user.is_online = (
            True
            if data.get("status") == "online"
            else False
            if data.get("status") == "offline"
            else user.is_online
        )
        user.save()
        return Response(status=status.HTTP_200_OK)


class UserDataSerializer(APIView):
    def get(self, request):
        data = User.objects.all()
        return JsonResponse(
            {"UserData": list(GetUserDataSerializer(data, many=True).data)}
        )
