from django.shortcuts import render
from datetime import date
from .models import Producto,User,Carrito,Carrito_item,Categoria,Registro,RegistroItem
from django.shortcuts import get_object_or_404, redirect
from .forms import UpdateUserForm, FiltroProductoForm,UsernameEmailForm
from os import remove, path
from django.conf import settings
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F, Sum
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash


#######################CREA CUENTA DE USUARIO##################################
def crearcuenta(request):
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        nombre_usuario = request.POST.get('nombre_usuario')
        rut = request.POST.get('rut')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('lastName')
        email = request.POST.get('email')
        celular = request.POST.get('idcelular')
        direccion = request.POST.get('address')
        codigo_postal = request.POST.get('zip')
        contraseña1 = request.POST.get('contraseña1')
        contraseña2 = request.POST.get('contraseña2')

        # Validar que las contraseñas coincidan
        if contraseña1 != contraseña2:
            return render(request, 'registration/crearcuenta.html', {'error_message': 'Las contraseñas no coinciden.'})

        # Creamos un nuevo objeto Usuario con los datos del formulario
        nuevo_usuario = User(
            username=nombre_usuario,
            rut=rut,
            first_name=nombre,
            last_name=apellido,
            email=email,
            celular=celular,
            direccion=direccion,
            postal=codigo_postal,
        )

        nuevo_usuario.set_password(contraseña1)

        # Guardamos el objeto en la base de datos
        nuevo_usuario.save()

        # Redirigimos a una página de éxito o cualquier otra acción que desees realizar después de guardar
        return redirect(to='index')

    else:
        # Si no es una solicitud POST, simplemente renderizamos el formulario vacío
        return render(request, 'registration/crearcuenta.html')  
###############################################################################

#######################CIERRA LA SESION########################################
def cerrar_sesion(request):
    logout(request)
    return redirect(to='index')
###############################################################################

#######################INDEX###################################################
def index(request):
    fecha=date.isoformat(date.today())
    texto="Para traer los datos desde la vista se debe enviar a través del contexto de datos"
    lista=['Alfajor', 'Poleron', 'Paraguas','Gorro','Cruz con Micrófono']
    elementos=len(lista)
    categorias = Categoria.objects.all()
    datos={
        "fecha":fecha,
        "msg":texto,
        "lista":lista,
        "items":elementos,
        'categorias': categorias
    }
    return render(request,'crud/index.html', datos)
###############################################################################

#######################BORRA CUENTA DE USUARIO#################################
def eliminar(request,id):
    persona=get_object_or_404(User, username=id)
    
    if request.method=="POST":
        
        #from os import remove, path
        #from django.conf import settings
        #remove(path.join(str(settings.MEDIA_ROOT).replace('/media',''))+persona.foto.url)
        persona.delete()
        return redirect(to="index")
        
    datos={
        "persona":persona
    }
    
    return render(request,'crud/eliminar.html', datos)
###############################################################################

#######################OBTIENE RANGO DE PRECIO#################################
def obtener_rango(precio):
    """Convierte el precio en un rango definido"""
    if precio <= 50:
        return '0-50'
    elif 51 <= precio <= 100:
        return '51-100'
    elif 101 <= precio <= 200:
        return '101-200'
    else:
        return '201'
###############################################################################

#######################MUESTRA CATALOGO CON FILTRO#############################
def catalogo(request,id):
    categoria=get_object_or_404(Categoria,id=id)
    catalogo = Producto.objects.filter(categoria=categoria)
    form = FiltroProductoForm(request.GET)
    
    if form.is_valid():
        rangos_seleccionados = form.cleaned_data['rangos_precios']
        if rangos_seleccionados:
            precios_filtrados = []
            for rango in rangos_seleccionados:
                if rango == '201':
                    # Incluir todos los productos con precio mayor o igual a 201
                    precios_filtrados.extend([p for p in catalogo if p.precio >= 201])
                else:
                    # Convertir el rango seleccionado en valores numéricos
                    rango_split = rango.split('-')
                    min_precio = int(rango_split[0])
                    max_precio = int(rango_split[1])
                    # Filtrar productos dentro del rango especificado
                    precios_filtrados.extend([p for p in catalogo if min_precio <= p.precio <= max_precio])
    
            # Eliminar duplicados y mantener el orden
            catalogo = list(set(precios_filtrados))
    
    catalogo_con_stock = [producto for producto in catalogo if producto.cantidad_disponible > 0]
    paginator = Paginator(catalogo_con_stock, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    datos = {
        "pagina": page_obj,
        "form": form,
    }
    return render(request, 'crud/catalogo.html', datos)
###############################################################################

#######################MUESTRA EL CATALOGO SIN FILTRO##########################
def ver_catalogo(request):
    catalogo = Producto.objects.all()
    form = FiltroProductoForm(request.GET)
    
    if form.is_valid():
        rangos_seleccionados = form.cleaned_data['rangos_precios']
        if rangos_seleccionados:
            precios_filtrados = []
            for rango in rangos_seleccionados:
                if rango == '201':
                    # Incluir todos los productos con precio mayor o igual a 201
                    precios_filtrados.extend([p for p in catalogo if p.precio >= 201])
                else:
                    # Convertir el rango seleccionado en valores numéricos
                    rango_split = rango.split('-')
                    min_precio = int(rango_split[0])
                    max_precio = int(rango_split[1])
                    # Filtrar productos dentro del rango especificado
                    precios_filtrados.extend([p for p in catalogo if min_precio <= p.precio <= max_precio])
    
            # Eliminar duplicados y mantener el orden
            catalogo = list(set(precios_filtrados))
    
    catalogo_con_stock = [producto for producto in catalogo if producto.cantidad_disponible > 0]
    paginator = Paginator(catalogo_con_stock, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    datos = {
        "pagina": page_obj,
        "form": form,
    }
    return render(request, 'crud/catalogo.html', datos)
###############################################################################

#######################MUESTRA EL PRODUCTO#####################################
def producto(request,id):
    item=get_object_or_404(Producto,id=id)
    stock=Producto.objects.all() #queryset

    datos={
        "item":item,
        "catalogo":stock  
    }
    return render(request,'crud/producto.html',datos)
###############################################################################

#######################MUESTRA EL CARRITO######################################
def carrito(request):   
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    else:
        # Obtener el ID del carrito desde la sesión para usuarios anónimos
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = get_object_or_404(Carrito, id=carrito_id)
        else:
            carrito = Carrito.objects.create()
            # Guardar el ID del carrito en la sesión del usuario anónimo
            request.session['carrito_id'] = carrito.id

    items = carrito.items.all()
    carrito.total = carrito.items.aggregate(total=Sum(F('cantidad') * F('producto__precio')))['total'] or 0
    datos={
        "carrito":carrito,
        "items":items  
    }
    return render(request,'crud/carrito.html' , datos)
###############################################################################

#######################AÑADE PRODUCTO AL CARRITO###############################
def add_to_cart(request, product_id):
    producto = get_object_or_404(Producto, id=product_id)

    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
            # Limpiar el ID del carrito en la sesión si existe
        if 'carrito_id' in request.session:
            del request.session['carrito_id']
    
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = get_object_or_404(Carrito, id=carrito_id)
        else:
            carrito = Carrito.objects.create()
            request.session['carrito_id'] = carrito.id
     
    cart_item, created = Carrito_item.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        aux = int(request.POST.get('contador', 1))
        cart_item.cantidad = F('cantidad') + aux
        cart_item.save()
    else:
        cart_item.cantidad = int(request.POST.get('contador', 1))  # Si es un nuevo item, setea la cantidad a 'contador'
        cart_item.save()
    # Actualizar el total del carrito
    carrito.total = carrito.items.aggregate(total=Sum(F('cantidad') * F('producto__precio')))['total'] or 0
    carrito.save()
    
    return redirect(request.META.get('HTTP_REFERER'))
###############################################################################

#######################QUITA PRODUCTO AL CARRITO###############################
def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        carrito = get_object_or_404(Carrito, usuario=request.user)
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = get_object_or_404(Carrito, id=carrito_id)
        else:
            return redirect('view_cart')  # Redirigir si no hay carrito encontrado
       
    cart_item = get_object_or_404(Carrito_item, carrito=carrito, id=product_id)
    cart_item.delete()

    # Actualizar el total del carrito
    carrito.total = carrito.items.aggregate(total=Sum(F('cantidad') * F('producto__precio')))['total'] or 0
    carrito.save()
    
    return redirect('carrito')
###############################################################################

#######################AUMENTA PRODUCTO AL CARRITO#############################
def aumentar_cantidad(request, item_id):
    item = get_object_or_404(Carrito_item, id=item_id)
    item.cantidad += 1
    item.save()
    return redirect(request.META.get('HTTP_REFERER'))
###############################################################################

#######################DISMINUYE PRODUCTO AL CARRITO###########################
def disminuir_cantidad(request, item_id):
    item = get_object_or_404(Carrito_item, id=item_id)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    return redirect(request.META.get('HTTP_REFERER'))
###############################################################################

#######################MUESTRA EL PERFIL#######################################
def perfil(request,id):

    persona=get_object_or_404(User,username=id)  
    datos={
        "perfil":persona
    }
    return render(request,'crud/perfil.html',datos)
###############################################################################

#######################MODIFICA DATOS DEL USUARIO##############################
def modificar_usuario(request,id):
    persona=get_object_or_404(User,username=id)
    form=UpdateUserForm(instance=persona)
    
    if request.method=="POST":
        form=UpdateUserForm(data=request.POST,files=request.FILES,instance=persona)
        if form.is_valid():
            usuario_modificado = form.save(commit=False)
            # Si se ha proporcionado una nueva contraseña, actualiza la contraseña del usuario
            nueva_contraseña = form.cleaned_data.get('password')
            if nueva_contraseña:
                usuario_modificado.set_password(nueva_contraseña)
                 # Actualiza la sesión del usuario para mantenerlo conectado(por la contraseña Django
                 # cierra automaticamente cuando se actualiza contraseña)
                update_session_auth_hash(request, usuario_modificado) 
            usuario_modificado.save()

            return redirect(reverse('perfil', args=[id]))
    
    datos={
        "form":form,
        "persona":persona
    }
    return render(request,'crud/modificar_usuario.html',datos)
###############################################################################

#######################CONFIRMA COMPRA Y GUARDA REGISTRO#######################
def confirma(request, id):
    carrito = get_object_or_404(Carrito, id=id)
    items = carrito.items.all()
    
    # Verificar si hay suficiente stock
    for item in items:
        if item.producto.cantidad_disponible < item.cantidad:
            messages.error(request, f"No hay suficiente stock para el producto {item.producto.nombre}.")
            return redirect('carrito')
    
    # Crear el Registro de compra
    usuario = request.user if request.user.is_authenticated else None
    compra = Registro.objects.create(
        usuario=usuario,
        rut=request.POST.get('rut'),
        nombre=request.POST.get('nombre'),
        apellido=request.POST.get('lastName'),
        direccion=request.POST.get('address'),
        celular=request.POST.get('idcelular'),
        email=request.POST.get('email'),
        total=0
    )
    total = 0
    for item in items:
        producto = item.producto
        cantidad = item.cantidad
        precio_producto = producto.precio
        subtotal = cantidad * precio_producto
        
        # Crear un RegistroItem para la compra y asociarlo correctamente
        registro_item = RegistroItem.objects.create(
            compra=compra,  # Asociar este RegistroItem con la compra creada
            producto=producto,
            cantidad=cantidad,
            precio_producto=precio_producto,
            subtotal=subtotal
        )
        
        total += subtotal
    
    # Actualizar el total en la compra final
    compra.total = total
    compra.save()
    
    # Actualizar el stock de los productos después de la compra
    for item in items:
        producto = item.producto
        producto.cantidad_disponible -= item.cantidad
        producto.save()
    
    # Vaciar el carrito después de la compra
    carrito.items.all().delete()
    
    return redirect('compra')
###############################################################################

#######################EVITA DUPLICAR REGISTRO#################################
def compra(request):
    return render(request,'crud/compra.html')
###############################################################################

#######################OLVIDA CONTRASEÑA USUARIO###############################
def olvido_contraseña(request):
    if request.method == 'POST':
        form = UsernameEmailForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            try:
                user = User.objects.get(username=username)
                if user.email == email:
                    user.password = make_password(new_password)
                    user.save()
                    messages.success(request, f"La contraseña para {username} ha sido cambiada exitosamente.")
                    return redirect('olvido_contraseña')
                else:
                    messages.error(request, f"El correo {email} no pertenece al usuario {username}.")
            except User.DoesNotExist:
                messages.error(request, f"El usuario {username} no existe.")
        else:
            messages.error(request, "Formulario inválido. Por favor, intente de nuevo.")
    else:
        form = UsernameEmailForm()
    
    return render(request, 'crud/olvido_contraseña.html', {'form': form})
###############################################################################

#######################MUESTRA LAS COMPRAS DEL USUARIO#########################
def detallecompras(request):
    registros = Registro.objects.filter(usuario=request.user).order_by('-fecha_compra')
    context = {
        'registros': registros
    }
    return render(request, 'crud/detallecompras.html', context)
###############################################################################

#######################MUESTRA EL DETALLE DE LAS COMPRAS#######################
def detalle_registro(request, id):
    registro = get_object_or_404(Registro, id=id, usuario=request.user)
    items = RegistroItem.objects.filter(compra=registro)
    context = {
        'registro': registro,
        'items': items
    }
    return render(request, 'crud/detalle_registro.html', context)
###############################################################################

#######################MUESTRA DATOS DEL USUARIO AL PAGAR######################
def pagar(request,id):
    persona=get_object_or_404(User,username=id)  
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    else:
        # Obtener el ID del carrito desde la sesión para usuarios anónimos
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = get_object_or_404(Carrito, id=carrito_id)
        else:
            carrito = Carrito.objects.create()
            # Guardar el ID del carrito en la sesión del usuario anónimo
            request.session['carrito_id'] = carrito.id
    items = carrito.items.all()
    carrito.total = carrito.items.aggregate(total=Sum(F('cantidad') * F('producto__precio')))['total'] or 0
    carrito.save()
    datos={
        "pagar":persona,
        "carrito":carrito,
        "items":items  
    }
    return render(request,'crud/pagar.html',datos)
###############################################################################

#######################MANDA A PAGAR EL PRODUCTO CON USUARIO###################
def add_to_cart_and_redirect(request, product_id, username):
    producto = get_object_or_404(Producto, id=product_id)

    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        # Limpiar el ID del carrito en la sesión si existe
        if 'carrito_id' in request.session:
            del request.session['carrito_id']
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = get_object_or_404(Carrito, id=carrito_id)
        else:
            carrito = Carrito.objects.create()
            request.session['carrito_id'] = carrito.id
    
    cart_item, created = Carrito_item.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        aux = int(request.POST.get('contador', 1))
        cart_item.cantidad = F('cantidad') + aux
        cart_item.save()
    else:
        cart_item.cantidad = int(request.POST.get('contador', 1))  # Si es un nuevo item, setea la cantidad a 'contador'
        cart_item.save()


    # Actualizar el total del carrito
    carrito.total = carrito.items.aggregate(total=Sum(F('cantidad') * F('producto__precio')))['total'] or 0
    carrito.save()

    # Redirigir a la página de pago después de agregar al carrito
    return redirect('pagar', username)
###############################################################################

#######################MANDA A PAGAR EL PRODUCTO SIN USUARIO###################
def add_to_cart_and_redirect_anoni(request, product_id):
    producto = get_object_or_404(Producto, id=product_id)

    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        # Limpiar el ID del carrito en la sesión si existe
        if 'carrito_id' in request.session:
            del request.session['carrito_id']
    else:
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = get_object_or_404(Carrito, id=carrito_id)
        else:
            carrito = Carrito.objects.create()
            request.session['carrito_id'] = carrito.id
    
    cart_item, created = Carrito_item.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        cart_item.cantidad = F('cantidad') + 1
        cart_item.save()

    # Actualizar el total del carrito
    carrito.total = carrito.items.aggregate(total=Sum(F('cantidad') * F('producto__precio')))['total'] or 0
    carrito.save()

    # Redirigir a alguna página relevante después de agregar al carrito (aquí se usa una página de ejemplo)
    return redirect('pagar_s')
###############################################################################

#######################PAGAR SIN CUENTA(PIDE LOS DATOS)########################
def pagar_s(request):
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    else:
        # Obtener el ID del carrito desde la sesión para usuarios anónimos
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = get_object_or_404(Carrito, id=carrito_id)
        else:
            carrito = Carrito.objects.create()
            # Guardar el ID del carrito en la sesión del usuario anónimo
            request.session['carrito_id'] = carrito.id
    
    
    
    items = carrito.items.all()
    carrito.total = carrito.items.aggregate(total=Sum(F('cantidad') * F('producto__precio')))['total'] or 0

    datos={
        "carrito":carrito,
        "items":items  
    }
    return render(request,'crud/pagar_s.html',datos)
###############################################################################