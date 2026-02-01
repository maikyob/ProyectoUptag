from django.urls import include, path
from . import views

urlpatterns = [
    # Autenticación: llamadas a vistas propias
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path("signout/", views.signout, name="signout"),
    # Si quieres habilitar las URLs de autenticación de Django (login/logout/password),
    # registra el include en una ruta distinta (opcional):
    path('accounts/', include('django.contrib.auth.urls')),
    path("", views.index, name = "index"),
    #Urls Inventario
    path("productlist/", views.productlist, name = "productlist"),
    path("addproduct/", views.addproduct, name = "addproduct"),
    
    #Urls Ventas
    path("saleslist/", views.salelist, name = "saleslist"),
    path("productos_por_servicio/", views.productos_por_servicio, name="productos_por_servicio"),
    path("pos/", views.pos, name = "pos"),
    path("newsale/", views.pos, name = "newsale"),
    path("salereturnlist/", views.salesreturnlist, name = "salesreturnlist"),
    path("createsalesreturn/", views.createsalesreturn, name = "createsalesreturn"),
    #Urls Servicios
    path("servicelist/", views.servicelist, name = "servicelist"),
    path("addservice/", views.addservice, name = "addservice"),
    #clientes
    path("clientlist/", views.clientlist, name = "clientlist"),
    path("addclient/", views.addclient, name = "addclient"),
    path("registrar_venta/", views.registrar_venta, name="registrar_venta"),
    #Urls Perfil
    path("profile/", views.profile, name = "profile"),

    #Url Transacciones
    path("transactions/", views.transactions, name = "transactiones"),
]