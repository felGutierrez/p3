from django.contrib import admin
from .models import Carrito_item,Carrito, User, Producto,Categoria,Registro,RegistroItem


# VISTA PARA PROBAR EN EL ADMIN DJANGO
class AdmcarritoI(admin.ModelAdmin):
    list_display= ['producto','carrito','cantidad']
    list_filter=['cantidad']


# PARA PROBAR EN EL ADMIN DJANGO
admin.site.register(Producto)
admin.site.register(Registro)
admin.site.register(RegistroItem)
admin.site.register(Carrito)
admin.site.register(Carrito_item,AdmcarritoI)
admin.site.register(Categoria)
admin.site.register(User)


