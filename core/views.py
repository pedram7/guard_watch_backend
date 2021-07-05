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

from core.serializers import *


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
        serializer = GuardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Bad Credentials'}, status=400)
        guard = serializer.create(serializer.validated_data)
        return Response({'message': 'Registered Successfully'}, status=200)

        pass


class CreateBand(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass


class UpdateGuard(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass

    def delete(self, request):
        pass


class UpdateBand(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass

    def delete(self, request):
        pass


class EditBandGuard(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass


class BulkCreateLog(APIView):

    def post(self, request):
        import json
        data = json.loads(request.data)
        return Response('hi')


@api_view(['GET'])
def guard_list(request):
    pass


@api_view(['GET'])
def get_guard_history(request, staff_id):
    pass


@api_view(['GET'])
def get_band_history(request, staff_id):
    pass


@api_view(['GET'])
def get_guard_list(request):
    pass


@api_view(['GET'])
def get_band_list(request):
    pass


@api_view(['GET'])
def get_guard_last_history(request):
    pass


@api_view(['GET'])
def get_band_last_history(request):
    pass


@api_view(['GET'])
def get_day_history(request):
    pass


@api_view(['GET'])
def get_guard_profile(request):
    pass
