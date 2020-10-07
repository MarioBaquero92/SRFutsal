
from django.conf.urls import url, include
from apps.usuario.views import RegistroUsuario

urlpatterns = [
	url(r'^registro$',RegistroUsuario.as_view(), name='registrar_usuario')
]