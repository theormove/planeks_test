"""planeks_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from csv_generator import views as generator_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', generator_views.data_schemas, name = 'data-schemas' ),
    path('data_schema/<int:pk>/', generator_views.data_schema, name = 'data-schema'),
    path('data_schema/new/', generator_views.new_data_schema, name = 'new-data-schema'),
    path('data_sets/<int:pk>/', generator_views.data_sets, name = 'data-sets'),
    path('login/', auth_views.LoginView.as_view(template_name = "csv_generator/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = "csv_generator/logout.html"), name='logout'),
    path('task_status/<slug:slug>', generator_views.progress, name = 'progress'),
    path('forbidden/', generator_views.forbidden, name='forbidden')
]
from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
