from django.urls import path
from .views import index,eliminar,cerrar_sesion,crearcuenta,carrito,catalogo,compra,modificar_usuario,olvido_contraseña,pagar,pagar_s,perfil,producto,confirma,ver_catalogo

from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [

    path('',index,name='index'),

    #USUARIO
    path('perfil/<id>',perfil, name='perfil'),
    path('crearcuenta/', crearcuenta, name='crearcuenta'),
    path('cerrar_sesion',cerrar_sesion, name='cerrar_sesion'),
    path('eliminar/<id>',eliminar, name='eliminar'),
    path('modificar_usuario/<id>',modificar_usuario, name='modificar_usuario'),
    path('olvido_contraseña/',olvido_contraseña, name='olvido_contraseña'),

    #CARRITO
    path('carrito/',carrito, name='carrito'),
    path('carrito/add/<product_id>',views.add_to_cart, name='add_to_cart'),
    path('carrito/remove/<product_id>',views.remove_from_cart, name='remove_from_cart'),
    path('carrito/aumentar/<int:item_id>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('carrito/disminuir/<int:item_id>/', views.disminuir_cantidad, name='disminuir_cantidad'),

    #REGISTRO
    path('detalle/<int:id>/', views.detalle_registro, name='detalle_registro'),
    path('detallecompras/', views.detallecompras, name='detallecompras'),

    #CATALOGO
    path('catalogo/<id>',catalogo, name='catalogo'),
    path('ver_catalogo/',ver_catalogo, name='ver_catalogo'),

    #PRODUCTO
    path('producto/<id>',producto, name='producto'),

    #COMPRA
    path('compra',compra, name='compra'),
    path('pagar_s/',pagar_s, name='pagar_s'),
    path('pagar/<id>',pagar, name='pagar'),
    path('pagar_s/add_to_cart_and_redirect_anoni//<int:product_id>/',views.add_to_cart_and_redirect_anoni, name='add_to_cart_and_redirect_anoni'),
    path('pagar/add-to-cart-and-redirect//<int:product_id>/<str:username>/',views.add_to_cart_and_redirect, name='add_to_cart_and_redirect'),
    path('pagar/confirma/<id>',views.confirma, name='confirma'),

 
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

