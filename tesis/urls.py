"""tesis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView, \
PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    
    url(r'^admin/', admin.site.urls),
    url(r'^jugador/', include(('apps.jugador.urls', 'jugador'), namespace='jugador')),
    url(r'^usuario/', include(('apps.usuario.urls', 'usuario'), namespace='usuario')),
    url(r'^emparejamiento/', include(('apps.emparejamiento.urls', 'emparejamiento'), namespace='emparejamiento')),
    url(r'^login/', LoginView.as_view(template_name='index.html'), name='login'),
    url(r'^login/', LogoutView.as_view(template_name='index.html'), name='logout'),
    url(r'^reset/formulario', PasswordResetView.as_view(template_name='resetpassword/formulario_reset.html'), name='formulario_reset'),
    url(r'^reset/confirmacion', PasswordResetDoneView.as_view(template_name='resetpassword/reset_hecho.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', PasswordResetConfirmView.as_view(template_name='resetpassword/password_reset_confirmar.html'), name='password_reset_confirm'),
    url(r'^reset/completo', PasswordResetCompleteView.as_view(template_name='resetpassword/password_reset_completo.html'), name='password_reset_complete'),


]
