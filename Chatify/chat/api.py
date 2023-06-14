from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, ChatMessageSerializer
from .models import User, Chat
from .utils import validate_contact_number, set_status
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import JsonResponse
from rest_framework.serializers import ValidationError
from .constants import LOGIN_VALIDATION_ERROR_MESSAGE
from .websocket_utils import send_chat_message, get_group_name
from django.contrib.sessions.models import Session
from .redis_utils import set_last_login, REDIS_CACHE
from django.utils import timezone
import datetime
from django.db.models import F
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from zipfile import ZipFile
from django.shortcuts import render


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
            serializer = UserSerializer(
                queryset,
                many=True,
            )
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
                send_chat_message(user.id, "login", "", "", "")
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
        user_id = request.data.get("id")
        get_status = request.data.get("status")
        set_status(user_id, get_status)
        send_chat_message(user_id, "login", "", "", "")
        return Response(status=status.HTTP_200_OK)


class OnlineUsersAPI(APIView):
    def get(self, request):
        data = (
            User.objects.filter(is_online=True, is_active=True)
            .order_by("-id")
            .exclude(id=request.user.id)
        )
        serializer = UserSerializer(data, many=True, context={"request": request})
        return JsonResponse({"UserData": serializer.data})


class LogoutView(APIView):
    def all_unexpired_sessions_for_user(self, user):
        user_sessions = []
        all_sessions = Session.objects.filter(expire_date__gte=datetime.datetime.now())
        for session in all_sessions:
            session_data = session.get_decoded()
            if user.pk == int(session_data.get("_auth_user_id")):
                user_sessions.append(session.pk)
        return Session.objects.filter(pk__in=user_sessions)

    def delete_all_unexpired_sessions_for_user(self, user, session_to_omit=None):
        session_list = self.all_unexpired_sessions_for_user(user)

        if session_to_omit is not None:
            session_list.exclude(session_key=session_to_omit.session_key)
            return redirect(reverse("chat:loginUI"))
        session_list.delete()

    def get(self, request):
        self.delete_all_unexpired_sessions_for_user(request.user)
        logout(request)
        return redirect(reverse("chat:loginUI"))


class SetUserActiveTime(APIView):
    def get(self, request):
        set_last_login(request.user.id)
        return Response(status=status.HTTP_200_OK)


class CheckUserActivity(APIView):
    def get(self, request):
        current_time = timezone.now()
        for key in REDIS_CACHE.keys("user:*:last_login"):
            redis_time = REDIS_CACHE.get(key)
            user_id = key.decode("utf-8").split(":")[1]
            redis_time = redis_time.decode("utf-8")
            last_active_time = datetime.datetime.fromisoformat(redis_time)
            time_diff = (current_time - last_active_time).total_seconds()
            if time_diff > 60:
                set_status(user_id, "offline")
                send_chat_message(user_id, "login", "", "", "")
        return Response(status=status.HTTP_200_OK)


class ChatMessages(APIView):
    def get(self, request, *args, **kwargs):
        get_id = kwargs.get("pk")
        group_name = Chat.objects.filter(
            group__name=get_group_name(request.user.id, get_id)
        ).order_by(F("id"))
        serializer = ChatMessageSerializer(group_name, many=True)
        return JsonResponse({"messageData": serializer.data}, status=status.HTTP_200_OK)


class BlockUserAPI(APIView):
    def post(self, request, *args, **kwargs):
        current_user_id = request.user.id
        block_user_id = request.data.get("blockUserId")
        current_user = User.objects.get(id=current_user_id)
        if int(block_user_id) in list(current_user.block_user.values_list(flat=True)):
            current_user.block_user.remove(block_user_id)
            send_chat_message(
                current_user_id, "login", block_user_id, current_user_id, "false"
            )
        else:
            current_user.block_user.add(block_user_id)
            send_chat_message(
                current_user_id, "login", block_user_id, current_user_id, "true"
            )
        return Response(status=status.HTTP_200_OK)


class HomePage(APIView):
    def get(self, request, *args, **kwargs):

        get_id = kwargs.get("pk")
        group_name = Chat.objects.filter(
            group__name=get_group_name(request.user.id, get_id)
        ).order_by(F("id"))
        serializer = ChatMessageSerializer(group_name, many=True)
        receiver_img = User.objects.get(id=get_id)
        return render(
            request,
            "chat/export_chat_design.html",
            {"messageData": serializer.data, "receiver_img": receiver_img},
        )


class PdfDownloadAPI(APIView):
    def get(self, request, *args, **kwargs):
        get_id = kwargs.get("pk")
        group_name = Chat.objects.filter(
            group__name=get_group_name(request.user.id, get_id)
        ).order_by(F("id"))
        serializer = ChatMessageSerializer(group_name, many=True)
        receiver_img = User.objects.get(id=get_id)

        # Convert HTML to PDF
        html_content = render_to_string(
            "chat/export_chat_design.html",
            {"messageData": serializer.data, "receiver_img": receiver_img},
        )
        pdf_file = HTML(string=html_content).write_pdf()

        # Create ZIP file
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w", allowZip64=True) as myzip:
            myzip.writestr("pdf_file.pdf", pdf_file)
        myzip.close()
        # Create HTTP response
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=chat.zip"

        return response
