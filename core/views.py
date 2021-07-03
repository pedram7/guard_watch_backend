import _pickle as cPickle
import os
import pathlib
import random

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.http import FileResponse
from django.shortcuts import redirect
# Create your views here.

from rest_framework import permissions, authentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import LoginSerializer


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(template_name='login.html')
        else:
            return Response(template_name='login.html')

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)

            return redirect('choose_file')

        except ValidationError:
            return Response({'message': 'login failed', 'form': serializer}, template_name='login.html',
                            status=403)


class CreateGuard(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass


class BulkCreateLog(APIView):

    def post(self, request):
        pass


@api_view(['GET'])
def guard_list(request):
    pass


@api_view(['GET'])
def get_guard_report_page(request):
    pass


@api_view(['GET'])
def get_guard_report_data(request):
    pass
