from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Sucursal, Empleado, Cliente

# =================================
# INICIO
# =================================
def inicio_jugueteria(request):
    contexto = {'fecha': timezone.now()}
    return render(request, 'inicio.html', contexto)


# =================================
# SUCURSALES (CRUD)
# =================================
def agregar_sucursal(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        direccion = request.POST.get('direccion', '')
        ciudad = request.POST.get('ciudad', '')
        estado = request.POST.get('estado', '')
        telefono = request.POST.get('telefono', '')
        codigo_postal = request.POST.get('codigo_postal', '')
        email = request.POST.get('email', '')

        # Crear la sucursal primero
        sucursal = Sucursal.objects.create(
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            estado=estado,
            telefono=telefono,
            codigo_postal=codigo_postal,
            email=email
        )

        # Guardar imagen si se subió (manejo seguro)
        if request.FILES.get('imagen'):
            try:
                sucursal.imagen = request.FILES['imagen']
                sucursal.save()
            except Exception as e:
                # imprimir en consola para depuración en desarrollo
                print('Error guardando imagen de sucursal:', e)

        return redirect('ver_sucursales')

    return render(request, 'sucursal/agregar_sucursal.html')


def ver_sucursales(request):
    sucursales = Sucursal.objects.all().order_by('id')
    return render(request, 'sucursal/ver_sucursales.html', {'sucursales': sucursales})


def actualizar_sucursal(request, id):
    sucursal = get_object_or_404(Sucursal, id=id)
    return render(request, 'sucursal/actualizar_sucursal.html', {'sucursal': sucursal})


def realizar_actualizacion_sucursal(request, id):
    if request.method == 'POST':
        sucursal = get_object_or_404(Sucursal, id=id)
        sucursal.nombre = request.POST.get('nombre', sucursal.nombre)
        sucursal.direccion = request.POST.get('direccion', sucursal.direccion)
        sucursal.ciudad = request.POST.get('ciudad', sucursal.ciudad)
        sucursal.estado = request.POST.get('estado', sucursal.estado)
        sucursal.telefono = request.POST.get('telefono', sucursal.telefono)
        sucursal.codigo_postal = request.POST.get('codigo_postal', sucursal.codigo_postal)
        sucursal.email = request.POST.get('email', sucursal.email)

        if request.FILES.get('imagen'):
            try:
                sucursal.imagen = request.FILES['imagen']
            except Exception as e:
                print('Error al actualizar imagen de sucursal:', e)

        sucursal.save()
        return redirect('ver_sucursales')

    return redirect('actualizar_sucursal', id=id)


def borrar_sucursal(request, id):
    sucursal = get_object_or_404(Sucursal, id=id)
    if request.method == 'POST':
        sucursal.delete()
        return redirect('ver_sucursales')
    return render(request, 'sucursal/borrar_sucursal.html', {'sucursal': sucursal})


# =================================
# EMPLEADOS (CRUD)
# =================================
def ver_empleados(request):
    empleados = Empleado.objects.select_related('id_sucursal').all().order_by('id')
    return render(request, 'empleado/ver_empleados.html', {'empleados': empleados})


def agregar_empleado(request):
    sucursales = Sucursal.objects.all().order_by('nombre')
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        edad = request.POST.get('edad') or None
        direccion = request.POST.get('direccion', '')
        puesto = request.POST.get('puesto', '')
        salario = request.POST.get('salario') or None
        id_sucursal = request.POST.get('id_sucursal')  # puede venir vacío

        empleado = Empleado.objects.create(
            nombre=nombre,
            apellido=apellido,
            edad=edad if edad else None,
            direccion=direccion,
            puesto=puesto,
            salario=salario if salario else None,
            id_sucursal=Sucursal.objects.get(pk=id_sucursal) if id_sucursal else None
        )
        return redirect('ver_empleados')

    return render(request, 'empleado/agregar_empleado.html', {'sucursales': sucursales})


def actualizar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    sucursales = Sucursal.objects.all().order_by('nombre')
    return render(request, 'empleado/actualizar_empleado.html', {'empleado': empleado, 'sucursales': sucursales})


def realizar_actualizacion_empleado(request, id):
    if request.method == 'POST':
        empleado = get_object_or_404(Empleado, id=id)
        empleado.nombre = request.POST.get('nombre', empleado.nombre)
        empleado.apellido = request.POST.get('apellido', empleado.apellido)
        empleado.edad = request.POST.get('edad') or None
        empleado.direccion = request.POST.get('direccion', empleado.direccion)
        empleado.puesto = request.POST.get('puesto', empleado.puesto)
        empleado.salario = request.POST.get('salario') or None

        id_sucursal = request.POST.get('id_sucursal')
        if id_sucursal:
            empleado.id_sucursal = Sucursal.objects.get(pk=id_sucursal)
        else:
            empleado.id_sucursal = None

        empleado.save()
        return redirect('ver_empleados')

    return redirect('ver_empleados')


def borrar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('ver_empleados')
    return render(request, 'empleado/borrar_empleado.html', {'empleado': empleado})


# =================================
# CLIENTES (CRUD)
# =================================
def ver_clientes(request):
    clientes = Cliente.objects.select_related('id_sucursal').all().order_by('id')
    return render(request, 'cliente/ver_clientes.html', {'clientes': clientes})


def agregar_cliente(request):
    sucursales = Sucursal.objects.all().order_by('nombre')
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        apellido = request.POST.get('apellido', '')
        edad = request.POST.get('edad') or None
        direccion = request.POST.get('direccion', '')
        telefono = request.POST.get('telefono', '')
        email = request.POST.get('email', '')
        id_sucursal = request.POST.get('id_sucursal')

        Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            edad=edad if edad else None,
            direccion=direccion,
            telefono=telefono,
            email=email,
            id_sucursal=Sucursal.objects.get(pk=id_sucursal) if id_sucursal else None
        )
        return redirect('ver_clientes')

    return render(request, 'cliente/agregar_cliente.html', {'sucursales': sucursales})


def actualizar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    sucursales = Sucursal.objects.all().order_by('nombre')
    return render(request, 'cliente/actualizar_cliente.html', {'cliente': cliente, 'sucursales': sucursales})


def realizar_actualizacion_cliente(request, id):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=id)
        cliente.nombre = request.POST.get('nombre', cliente.nombre)
        cliente.apellido = request.POST.get('apellido', cliente.apellido)
        cliente.edad = request.POST.get('edad') or None
        cliente.direccion = request.POST.get('direccion', cliente.direccion)
        cliente.telefono = request.POST.get('telefono', cliente.telefono)
        cliente.email = request.POST.get('email', cliente.email)

        id_sucursal = request.POST.get('id_sucursal')
        if id_sucursal:
            cliente.id_sucursal = Sucursal.objects.get(pk=id_sucursal)
        else:
            cliente.id_sucursal = None

        cliente.save()
        return redirect('ver_clientes')

    return redirect('ver_clientes')


def borrar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')
    return render(request, 'cliente/borrar_cliente.html', {'cliente': cliente})
