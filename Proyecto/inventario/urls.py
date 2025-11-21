from django.urls import path
from . import views

urlpatterns = [
    path("signin/", views.signin, name = "signin"),
    path("signup/", views.signup, name = "signup"),
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

    path("buscar_cliente/", views.buscar_cliente, name="buscar_cliente"),
    #Urls Perfil
    path("profile/", views.profile, name = "profile"),
]