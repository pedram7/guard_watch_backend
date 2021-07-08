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
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import *


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    # def get(self, request):
    #     if request.user.is_authenticated:
    #         return Response(template_name='login.html')
    #     else:
    #         return Response(template_name='login.html')

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            login(request, user)
            from datetime import datetime

            return Response({'message': 'login successful', 'time': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')},
                            status=200)

        except ValidationError:
            return Response({'message': 'login failed'}, template_name='login.html',
                            status=401)


class CreateGuard(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    # def get(self, request):
    #     pass

    def post(self, request):
        serializer = GuardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Bad Credentials'}, status=400)
        guard = serializer.create(serializer.validated_data)
        return Response({'message': 'Registered Successfully'}, status=200)

        pass


class CreateBand(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    # def get(self, request):
    #     pass

    def post(self, request):
        serializer = BandSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Bad Credentials'}, status=400)
        band = serializer.create(serializer.validated_data)
        return Response({'message': 'Registered Successfully'}, status=200)

        pass


class UpdateGuard(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    # def get(self, request):
    #     pass

    def post(self, request):
        serializer = GuardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Bad Credentials'}, status=400)
        guard = serializer.update(serializer.validated_data)
        return Response({'message': 'Updated Successfully'}, status=200)

    def delete(self, request):
        try:
            guard = Guard.objects.get(staff_id=request.data.get('staff_id'))
        except Guard.DoesNotExist:
            return Response({'message': 'Wrong ID'}, status=400)
        guard.delete()
        return Response({'message': 'Deleted Successfully'}, status=200)


class UpdateBand(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    # def get(self, request):
    #     pass

    def post(self, request):
        serializer = BandSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Bad Credentials'}, status=400)
        band = serializer.update(serializer.validated_data)
        return Response({'message': 'Updated Successfully'}, status=200)

    def delete(self, request):
        try:
            band = Wristband.objects.get(band_id=request.data.get('band_id'))
        except Wristband.DoesNotExist:
            return Response({'message': 'Wrong ID'}, status=400)
        band.delete()
        return Response({'message': 'Deleted Successfully'}, status=200)


class EditBandGuard(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    # def get(self, request):
    #     pass

    def post(self, request):
        staff_id = request.data.get('staff_id')
        band_id = request.data.get('band_id')
        try:
            band = Wristband.objects.get(band_id=band_id)
            band.guard = Guard.objects.get(staff_id=staff_id)
            band.save()
            return Response({'message': 'edited'}, status=200)
        except:
            return Response({'message': 'bad request'}, status=400)


class BulkCreateLog(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = BulkLogSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Bad Credentials'}, status=400)

        try:
            band = Wristband.objects.get(band_id=serializer.validated_data['band_id'])
        except:
            return Response({'message': 'no such band'}, status=400)

        serializer.create(serializer.validated_data)

        return Response({'message': 'Registered Successfully'}, status=200)


@api_view(['GET'])
# @login_required(login_url='/api/login')
def get_guard_history(request, staff_id):
    try:
        logs = LogInstance.objects.filter(guard__staff_id=staff_id).order_by('time').values()
        return Response({'logs': logs}, status=200)
    except:
        return Response({'message': 'bad credentials'}, status=400)


@api_view(['GET'])
# @login_required(login_url='/api/login')
def get_band_history(request, band_id):
    try:
        from datetime import datetime
        qstart = request.query_params.get('qstart')
        # qstart = datetime.strptime(request.GET.get('qdate'), '%Y-%m-%d')
        # qend = datetime.strptime(request.GET.get('qdate'), '%Y-%m-%d')
        qend = request.query_params.get('qend')
        logs = LogInstance.objects.filter(wristband__band_id=band_id).order_by('time')
        if qstart:
            logs = logs.filter(time__gte=qstart)
        if qend:
            logs = logs.filter(time__lte=qend)

        return Response({'logs': logs.values()}, status=200)
    except:
        return Response({'message': 'bad request'}, status=400)


@api_view(['GET'])
# @login_required(login_url='/api/login')
def get_guard_list(request):
    bands = Wristband.objects.all().values('id', 'name', 'band__band_id', 'staff_id', 'date_joined', 'date_left')
    return Response({'bands': bands}, status=200)


@api_view(['GET'])
# @login_required(login_url='/api/login')
def get_band_list(request):
    bands = Wristband.objects.all().values('id', 'band_id', 'guard__staff_id', 'is_deleted')
    return Response({'bands': bands}, status=200)


@api_view(['GET'])
# @login_required(login_url='/api/login')
def get_guard_last_history(request, staff_id):
    try:
        last = LogInstance.objects.filter(guard__staff_id=staff_id).order_by('time').values()
        if len(last) > 0:
            last = last[len(last) - 1]
        return Response({'last': last}, status=200)
    except:
        return Response({'message': 'bad request'}, status=400)


@api_view(['GET'])
# @login_required(login_url='/api/login')
def get_band_last_history(request, band_id):
    try:
        last = LogInstance.objects.filter(wristband__band_id=band_id).order_by('time').values()
        if len(last) > 0:
            last = last[len(last) - 1]
        return Response({'last': last}, status=200)
    except:
        return Response({'message': 'edited'}, status=400)


@api_view(['GET'])
# @login_required(login_url='/api/login')
def get_day_history(request):
    try:
        from datetime import datetime
        qdate = datetime.strptime(request.GET.get('qdate'), '%Y-%m-%d')
        last = LogInstance.objects.filter(time__date=qdate).order_by('time').values()
        return Response({'logs': last}, status=200)
    except:
        return Response({'message': 'edited'}, status=400)


@api_view(['GET'])
# @login_required(login_url='/api/login')
def get_guard_profile(request, staff_id):
    try:
        guard = Guard.objects.get(staff_id=staff_id).values('id', 'name', 'band__band_id', 'staff_id', 'date_joined',
                                                            'date_left')
        return Response({'guard': guard}, status=200)

    except:
        return Response({'message': 'Bad req'}, status=400)


@api_view(['GET'])
# @login_required(login_url='/api/login')
def active_guards(request):
    try:
        guards = Guard.objects.filter(band__isnull=False).values(
            'id', 'name', 'band__band_id', 'staff_id', 'date_joined')

        return Response({'guards': guards}, status=200)
    except:
        return Response({'message': 'Bad req'}, status=400)
