from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Importa los módulos de vistas
from managecultivo import views


urlpatterns = [
    path('', views.home, name='home'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),    
    path("bienvenida/", views.bienvenida, name="bienvenida"),        

    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path("crear_zonaagricola/", views.crear_zonaagricola, name="crear_zonaagricola"),          
    path("crear_personal/", views.crear_personal, name="crear_personal"),    

    path("parametrizar_cultivo/", views.parametrizar_cultivo, name="parametrizar_cultivo"),
    path("crear_cultivo/", views.crear_cultivo, name="crear_cultivo"),
    path("crear_actividadcultivo/", views.crear_actividadcultivo, name="crear_actividadcultivo"),
    path("crear_actividad/", views.crear_actividad, name="crear_actividad"),
    path("crear_insumo/", views.crear_insumo, name="crear_insumo"),
    path("crear_actividadcultivo/", views.crear_actividadcultivo, name="crear_actividadcultivo"),
    path("borrar_actividadcultivo/<int:pk>/", views.borrar_actividadcultivo, name="borrar_actividadcultivo"),
    path("planear_ciclo/", views.planear_ciclo, name="planear_ciclo"),
    path("compra_insumos/", views.gestionar_insumos, name="compra_insumos"),
    path("Consulta/clima/", views.clima, name="clima")
]
