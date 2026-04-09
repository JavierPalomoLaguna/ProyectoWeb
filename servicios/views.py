from django.shortcuts import render, redirect
from servicios.models import Servicio, Reserva
from django.contrib import messages
from datetime import date


def index_restaurante(request):
    """
    Vista para la página principal del restaurante
    Muestra hero, pilares de cocina, galería y formulario de reservas
    """
    # Obtener todos los servicios ordenados por categoría
    servicios = Servicio.objects.all()
    
    # Agrupar servicios por categoría
    servicios_por_categoria = {}
    for servicio in servicios:
        categoria = servicio.get_categoria_display()
        if categoria not in servicios_por_categoria:
            servicios_por_categoria[categoria] = []
        servicios_por_categoria[categoria].append(servicio)
    
    # Orden de categorías
    orden_categorias = [
        'Entrantes y Picoteo',
        'Primeros Platos', 
        'Segundos Platos',
        'Postres',
        'Bebidas',
    ]
    
    # Crear lista ordenada de categorías con sus servicios
    categorias_ordenadas = []
    for categoria_nombre in orden_categorias:
        if categoria_nombre in servicios_por_categoria:
            categorias_ordenadas.append({
                'nombre': categoria_nombre,
                'servicios': servicios_por_categoria[categoria_nombre],
                'slug': categoria_nombre.lower().replace(' ', '_').replace('ó', 'o')
            })
    
    context = {
        'categorias_ordenadas': categorias_ordenadas,
        'today': date.today().isoformat(),
    }
    return render(request, "servicios/index_restaurante.html", context)


def carta(request):
    """
    Vista para mostrar la carta completa del restaurante
    Con sidebar de navegación
    """
    # Obtener todos los servicios ordenados por categoría
    servicios = Servicio.objects.all()
    
    # Agrupar servicios por categoría
    servicios_por_categoria = {}
    for servicio in servicios:
        categoria = servicio.get_categoria_display()
        if categoria not in servicios_por_categoria:
            servicios_por_categoria[categoria] = []
        servicios_por_categoria[categoria].append(servicio)
    
    # Ordenar las categorías según el orden deseado
    orden_categorias = [
        'Entrantes y Picoteo',
        'Primeros Platos', 
        'Segundos Platos',
        'Postres',
        'Bebidas',
    ]
    
    # Crear lista ordenada de categorías con sus servicios
    categorias_ordenadas = []
    for categoria_nombre in orden_categorias:
        if categoria_nombre in servicios_por_categoria:
            categorias_ordenadas.append({
                'nombre': categoria_nombre,
                'servicios': servicios_por_categoria[categoria_nombre],
                'slug': categoria_nombre.lower().replace(' ', '_').replace('ó', 'o')
            })
    
    context = {
        'categorias_ordenadas': categorias_ordenadas,
        'today': date.today().isoformat(),
    }
    return render(request, "servicios/carta.html", context)


def procesar_reserva(request):
    """
    Procesa el formulario de reservas
    Puede redirigir tanto a index_restaurante como a carta
    """
    if request.method == 'POST':
        # Procesar datos del formulario manualmente
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        numero_personas = request.POST.get('numero_personas')
        comentarios = request.POST.get('comentarios', '')
        
        # Validaciones básicas
        if not all([nombre, telefono, email, fecha, hora, numero_personas]):
            messages.error(request, 'Por favor, completa todos los campos obligatorios.')
            # Redirigir a la página de origen
            referer = request.META.get('HTTP_REFERER', '')
            if 'carta' in referer:
                return redirect('carta')
            return redirect('index_restaurante')
        
        try:
            # Crear reserva
            reserva = Reserva.objects.create(
                nombre=nombre,
                telefono=telefono,
                email=email,
                fecha=fecha,
                hora=hora,
                numero_personas=numero_personas,
                comentarios=comentarios,
                estado='pendiente'
            )
            
            # Formatear fecha a formato español
            from datetime import datetime
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
            fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
            
            # Enviar email
            from django.core.mail import send_mail
            from django.conf import settings
            
            send_mail(
                subject=f"Nueva reserva - {nombre}",
                message=f"Nueva reserva recibida:\n\n"
                        f"Nombre: {nombre}\n"
                        f"Teléfono: {telefono}\n"
                        f"Email: {email}\n"
                        f"Fecha: {fecha_formateada}\n"
                        f"Hora: {hora}\n"
                        f"Número de personas: {numero_personas}\n"
                        f"Comentarios: {comentarios}\n",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['jpalomolaguna@gmail.com'],
                fail_silently=False,
            )
            
            messages.success(
                request, 
                f'¡Reserva enviada correctamente! Te confirmaremos por teléfono o email. '
                f'Reserva para {reserva.numero_personas} personas el {fecha_formateada} a las {reserva.hora}.'
            )
        except Exception as e:
            messages.error(request, 'Error al procesar la reserva. Por favor, inténtalo de nuevo.')
        
        # Redirigir a la página de origen con ancla a reservas
        from django.urls import reverse
        referer = request.META.get('HTTP_REFERER', '')
        if 'carta' in referer:
            return redirect(reverse('carta') + '#reservas')
        return redirect(reverse('index_restaurante') + '#reservas')
    
    # Si no es POST, redirigir al index
    return redirect('index_restaurante')