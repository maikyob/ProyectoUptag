from django.urls import include, path
from . import views

urlpatterns = [
    # Autenticación: llamadas a vistas propias
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    # Si quieres habilitar las URLs de autenticación de Django (login/logout/password),
    # registra el include en una ruta distinta (opcional):
    path('accounts/', include('django.contrib.auth.urls')),
    path("", views.index, name = "index"),
    #Urls Inventario
    path("productlist/", views.productlist, name = "productlist"),
    path("addproduct/", views.addproduct, name = "addproduct"),
    
    #Urls Ventas
    path("saleslist/", views.salelist, name = "saleslist"),
    path("pos/", views.pos, name = "pos"),
    path("newsale/", views.pos, name = "newsale"),
    path("salereturnlist/", views.salesreturnlist, name = "salesreturnlist"),
    path("createsalesreturn/", views.createsalesreturn, name = "createsalesreturn"),
    #Urls Compras
    path("purchaselist/", views.purchaselist, name = "purchaselist"),
    path("addpurchase/", views.addpurchase, name = "addpurchase"),
    path("importpurchase/", views.importpurchase, name = "importpurchase"),
    #Expensas
    path("expenselist/", views.expenselist, name = "expenselist"),
    path("addexpense/", views.addexpense, name = "addexpense"),
    path("expensecategory/", views.expensecategory, name = "expensecategory"),

    #Urls Perfil
    path("profile/", views.profile, name = "profile"),
]