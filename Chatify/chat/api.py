from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User


class RegistrationApi(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"errors": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserListAPI(APIView):
    def get(self, request):
        try:
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"errors": str(e.detail)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserOnlineAPIView(APIView):
    def put(self, request, *args, **kwargs):
        user = request.user.id
        user.save(is_online=True if request.data.get("online") else False)
        return Response(status=status.HTTP_200_OK)
#         if request.data.get("online") == "true":
#             user.save(online=True)
#         else:
#             user.save(online=False)