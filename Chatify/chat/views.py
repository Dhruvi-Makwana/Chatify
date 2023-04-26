from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class RegisterView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'chat/register.html'

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)