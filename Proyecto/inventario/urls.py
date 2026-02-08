from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name = "login"),
    path('salir/', views.salir, name='logout'),
    path("signup/", views.signup, name = "signup"),
    path('accounts/password_change/', views.CustomPasswordChangeView.as_view(), name= "password_change"),
    path('accounts/password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name= "password_change_done"),
    path('accounts/password_reset/', views.CustomPasswordResetView.as_view(), name= "password_reset"),
    path('accounts/password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name= "password_reset_done"),
    path('accounts/reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name= "password_reset_confirm"),
    path('accounts/reset/done/', views.CustomPasswordResetCompleteView.as_view(), name= "password_reset_complete"),
    path("", views.index, name = "index"),
    #Urls Inventario
    path("productlist/", views.productlist, name = "productlist"),
    path("addproduct/", views.addproduct, name = "addproduct"),
    path("editar_producto/<int:pk>/", views.editar_producto, name = "editar_producto"),
    path("eliminar_producto/<int:pk>/", views.eliminar_producto, name = "eliminar_producto"),
    
    #Urls Ventas
    path("saleslist/", views.salelist, name = "saleslist"),
    path("pos/", views.pos, name = "pos"),
    path("newsale/", views.pos, name = "newsale"),
    path("salereturnlist/", views.salesreturnlist, name = "salesreturnlist"),
    path("createsalesreturn/", views.createsalesreturn, name = "createsalesreturn"),
    # AJAX Ventas
    path("buscar_cliente/", views.buscar_cliente, name="buscar_cliente"),
    path("get_productos_servicio/<int:servicio_id>/", views.get_productos_servicio, name="get_productos_servicio"),
    path("registrar_venta/", views.registrar_venta, name="registrar_venta"),
    #Urls Servicios
    path("servicelist/", views.servicelist, name = "servicelist"),
    path("addservice/", views.addservice, name = "addservice"),
    path("edit_service/<int:pk>/", views.edit_service, name = "edit_service"),
    path("delete_service/<int:pk>/", views.delete_service, name = "delete_service"),
    #clientes
    path("clientlist/", views.clientlist, name = "clientlist"),
    path("addclient/", views.addclient, name = "addclient"),
    path("edit_client/<int:pk>/", views.edit_client, name = "edit_client"),
    path("delete_client/<int:pk>/", views.delete_client, name = "delete_client"),
    #Url Transacciones
    path("transactions/", views.transactions, name = "transactions"),
    #Urls Perfil
    path("profile/", views.profile, name = "profile"),
]