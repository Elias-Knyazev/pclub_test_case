"""compclub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from equipclub.views import EquipClubNotBusyAPIView, ECListAPIView, RentEquipAPIView, UserRentListCreateAPIView, \
    UserRentUpdateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/club-auth/', include('rest_framework.urls')), #стандартная авторизация
    path('api/v1/equipclublist/', ECListAPIView.as_view()), # просмотр всего списка оборудования с обновленным статусом
    path('api/v1/notbusy/', EquipClubNotBusyAPIView.as_view()), # просмотр свободного  оборудования
    path('api/v1/rentequip/<int:pk>', RentEquipAPIView.as_view()), # запрос на аренду оборудования
    path('api/v1/equipclub-delete/<int:pk>', ECListAPIView.as_view()), #удаление оборудования
    path('api/v1/auth/', include('djoser.urls')), # авторизация djoser
    re_path(r'^auth/', include('djoser.urls.authtoken')), # авторизация по токенам djoser
    path('api/v1/userrentlist/', UserRentListCreateAPIView.as_view()), #просмотр данных о скидках пользователей
    path('api/v1/discount/', UserRentUpdateAPIView.as_view()), #получить данные по скидке

]
