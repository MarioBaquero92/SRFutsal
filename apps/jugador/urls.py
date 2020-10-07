
from django.conf.urls import url, include
from apps.jugador.views import index_jugador,  \
	ListaJugador, CrearJugador, EditarJugador, EliminarJugador

urlpatterns = [
    
    url(r'^$', index_jugador, name='index_jugador'),
    url(r'^formulario$', CrearJugador.as_view(), name='crear_jugador'),
    url(r'^lista$', ListaJugador.as_view(), name='listar_jugadores'),
    url(r'^editar/(?P<pk>\d+)/$', EditarJugador.as_view(), name='editar_jugadores'),
    url(r'^eliminar/(?P<pk>\d+)/$', EliminarJugador.as_view(), name='eliminar_jugadores'),

   
]
