"""guard_watch_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/create_guard/', CreateGuard.as_view(), name='create_guard'),
    path('api/create_wristband/', CreateBand.as_view(), name='create_guard'),

    path('api/guards_list/', get_guard_list, name='guard_list'),
    path('api/guard_interval_history/<slug:staff_id>', get_guard_history, name='guard_data'),  # qstart ,#qend
    path('api/guard_last_history/<slug:staff_id>', get_guard_last_history, name='guard_data'),  # qstart ,#qend
    path('api/guard_profile/', get_guard_profile.as_view(), name='guard_page'),

    path('api/bands_list/', get_band_list, name='guard_list'),
    path('api/band_interval_history/<slug:band_id>', get_band_history, name='guard_list'),  # qstart ,#qend
    path('api/band_last_history/<slug:band_id>', get_band_last_history, name='guard_list'),  # qstart ,#qend

    path('api/all_day_history/', get_day_history, name='guard_list'),  # qby:band/guard?,qdate
    path('api/edit_wristband_guard/', EditBandGuard.as_view(), name='guard_list'),
    path('api/edit_guard/', UpdateGuard.as_view(), name='guard_list'),
    path('api/delete_band/', UpdateBand.as_view(), name='guard_list'),
    path('api/delete_guard/', UpdateGuard.as_view(), name='guard_list'),

    path('api/bulk_create_log/', BulkCreateLog.as_view(), name='create_guard'),
]
