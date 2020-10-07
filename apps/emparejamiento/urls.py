from django.conf.urls import url, include

from apps.emparejamiento.views import CrearPartido, FormacionPartido, ListaPartido, EliminarPartido, \
CrearEquipo, ListaEquipo, EditarEquipo, EliminarEquipo, GenerarJugador,  JugadoresEquipo, CrearConfirmacion

urlpatterns = [
url(r'^partido$', CrearPartido.as_view(), name='crear_partido'),
url(r'^lista_partido$', ListaPartido.as_view(), name='listar_partidos'),
url(r'^partido/(?P<pk>\d+)/$', FormacionPartido.as_view(), name='formacion_partido'),
url(r'^eliminar_partido/(?P<pk>\d+)/$', EliminarPartido.as_view(), name='eliminar_partidos'),

url(r'^formulario_equipo$', CrearEquipo.as_view(), name='crear_equipo'),
url(r'^lista_equipo$', ListaEquipo.as_view(), name='listar_equipos'),
url(r'^editar_equipo/(?P<pk>\d+)/$', EditarEquipo.as_view(), name='editar_equipos'),
url(r'^eliminar_equipo/(?P<pk>\d+)/$', EliminarEquipo.as_view(), name='eliminar_equipos'),
url(r'^generar_jugador$', GenerarJugador, name='generar_jugador'),
#url(r'^generar_recomendacion$', GenerarRecomendacion, name='generar_recomendacion'),
url(r'^lista_jugadorequipo$', JugadoresEquipo.as_view(), name='listar_jugadorequipo'),
url(r'^confimar_disponibilidad/(?P<pk>\d+)/$', CrearConfirmacion.as_view(), name='confimar_disponibilidad'),
]