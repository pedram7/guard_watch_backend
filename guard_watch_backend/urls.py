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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from core.views import *
from guard_watch_backend import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/login/', LoginView.as_view(), name='login'),
                  path('api/login', LoginView.as_view(), name='login_noslash'),
                  path('api/create_guard/', CreateGuard.as_view(), name='create_guard'),
                  path('api/create_wristband/', CreateBand.as_view(), name='create_band'),

                  path('api/guards_list/', get_guard_list, name='guard_list'),
                  path('api/guard_interval_history/<slug:staff_id>/', get_guard_history, name='guard_history'),
                  # qstart ,#qend
                  path('api/guard_last_history/<slug:staff_id>/', get_guard_last_history, name='guard_last'),
                  path('api/active_guards/', active_guards, name='guard_last'),

                  path('api/guard_profile/<slug:staff_id>/', get_guard_profile, name='guard_profile'),
                  path('api/edit_guard/<slug:staff_id>/', (UpdateGuard.as_view()),
                       name='edit_guard'),

                  path('api/bands_list/', get_band_list, name='band_list'),
                  path('api/band_interval_history/<slug:band_id>/', get_band_history, name='band_history'),
                  # qstart ,#qend
                  path('api/band_last_history/<slug:band_id>/', get_band_last_history, name='band_last'),

                  path('api/all_day_history/', get_day_history, name='day_history'),  # qdate
                  path('api/edit_wristband_guard/', EditBandGuard.as_view(), name='edit_band_guard'),

                  path('api/delete_band/', (UpdateBand.as_view()),
                       name='delete_band'),
                  path('api/delete_guard/', (UpdateGuard.as_view()),
                       name='delete_guard'),

                  path('api/bulk_create_log/', (BulkCreateLog.as_view()),
                       name='create_log'),

                  # path('api/edit_guard/', login_required(UpdateGuard.as_view(), login_url='/api/login'),
                  #      name='edit_guard'),
                  #
                  #
                  # path('api/delete_band/', login_required(UpdateBand.as_view(), login_url='/api/login'),
                  #      name='delete_band'),
                  # path('api/delete_guard/', login_required(UpdateGuard.as_view(), login_url='/api/login'),
                  #      name='delete_guard'),
                  #
                  # path('api/bulk_create_log/', login_required(BulkCreateLog.as_view(), login_url='/api/login'),
                  #      name='create_log'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
