from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.abastecimiento.forms import PedidoForm, PedidoDetailForm
from apps.abastecimiento.models import Pedido, DetallePedido
from apps.producto.models import Producto


class PedidoListView(ListView):
    template_name = 'abastecimiento/pedido_list.html'
    model = Pedido
    paginate_by = 100

    # se usa el decorador para evitar el crf_token
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title_page = "Maestro | Pedidos"
        main_title_content = "Pedidos"
        main_subtitle_content = "List"
        subtitle_table = "Lista pedidos"

        context.update({
            'CLASS_MENU_ABASTECIMIENTO': "active",
            'CLASS_SUBMENU_PEDIDOS': "show",
            'CLASS_SUBMENU_PEDIDOS_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table,
        })
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Pedido.objects.all():
                    data.append(i.toJSON())
            elif action == 'confirmar':
                id = request.POST['id']
                pedido = Pedido.objects.get(pk=id)
                pedido.confirmar_pedido()
                pedido.save()
            elif action == 'recepcionar':
                id = request.POST['id']
                pedido = Pedido.objects.get(pk=id)
                pedido.recibir_pedido()
                pedido.actualiza_stock()
                pedido.save()
            else:
                data['error'] = "no tiene acciones ejecutadas"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)


class PedidoAddView(CreateView):
    template_name = 'abastecimiento/pedido_add.html'
    model = Pedido
    form_class = PedidoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title_page = "Maestro | Pedidos"
        main_title_content = "Pedidos"
        main_subtitle_content = "Add"
        subtitle_table = "Agregar pedido"

        context.update({
            'CLASS_MENU_ABASTECIMIENTO': "active",
            'CLASS_SUBMENU_PEDIDOS': "show",
            'CLASS_SUBMENU_PEDIDOS_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table,
        })
        return context

    def get_success_url(self):
        messages.success(self.request, 'Se registro el ingreso exitoso, {}'.format(self.object.numero))
        return reverse('abastecimiento:pedido_list', kwargs={})

    def form_valid(self, form):
        context = self.get_context_data()
        form = self.form_class(self.request.POST, self.request.FILES)
        try:
            with transaction.atomic():
                if form.is_valid():

                    if not self.request.POST.getlist('producto[]'):
                        msj = 'Debe ingresar productos en el detalle'
                        messages.warning(self.request, msj)
                        return self.form_invalid(form)
                    if not self.request.POST.getlist('cantidad[]'):
                        msj = 'Un problema con las cantidades, favor de revisar'
                        messages.warning(self.request, msj)
                        return self.form_invalid(form)

                    # obtener el usuario logueado
                    usuario = self.request.user

                    # creando el diccionario de item y limpieza
                    lista_productos = self.request.POST.getlist('producto[]')
                    lista_cantidad = self.request.POST.getlist('cantidad[]')
                    lista_precio = self.request.POST.getlist('precio[]')
                    lista_subtotal = self.request.POST.getlist('subtotal[]')
                    list_items = []
                    index = 0
                    for id_producto in lista_productos:
                        if id_producto.isnumeric():
                            list_items.append({
                              'id_producto': id_producto,
                              'cantidad': lista_cantidad[index],
                              'precio': lista_precio[index],
                              'subtotal': lista_subtotal[index],
                            })
                        index += 1

                    # guardamos la cabecera
                    form.instance.usuario = usuario
                    form.save()

                    # guardamos detalles
                    self.crear_detalles_pedido(form.instance, list_items)

                    return super().form_valid(form)
                else:
                    return self.form_invalid(form)
        except Exception as e:
            print(e)
            messages.warning(self.request, 'Ocurrió un error vuelva a intentarlo : {}'.format(e))
            return self.form_invalid(form)

    def crear_detalles_pedido(self, obj_pedido,  list_items):
        for item in list_items:
            det = DetallePedido()
            det.pedido = obj_pedido
            det.producto = Producto.objects.get(pk=item['id_producto'])
            det.precio = item['precio']
            det.cantidad = item['cantidad']
            det.total = item['subtotal']
            try:
                det.save()
            except Exception as e:
                print(e)
                mensaje = 'Error al guardar el detalle del pedido | det = {} | Error => {}'.format(str(e), list_items)
                messages.warning(self.request, mensaje)


class PedidoEditView(UpdateView):
    template_name = 'abastecimiento/pedido_add.html'
    model = Pedido
    form_class = PedidoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title_page = "Maestro | Pedidos"
        main_title_content = "Pedidos"
        main_subtitle_content = "Add"
        subtitle_table = "Editar pedido"

        context.update({
            'CLASS_MENU_ABASTECIMIENTO': "active",
            'CLASS_SUBMENU_PEDIDOS': "show",
            'CLASS_SUBMENU_PEDIDOS_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table
        })
        return context

    def get_success_url(self):
        messages.success(self.request, 'Se actualizo el ingreso, {}'.format(self.object.numero))
        return reverse('abastecimiento:pedido_list', kwargs={})

    def form_valid(self, form):
        context = self.get_context_data()
        # form = self.form_class(self.request.POST, self.request.FILES)
        try:
            with transaction.atomic():
                if form.is_valid():
                    pedido = form.save(commit=False)
                    if not self.request.POST.getlist('producto[]'):
                        msj = 'Debe ingresar productos en el detalle'
                        messages.warning(self.request, msj)
                        return self.form_invalid(form)
                    if not self.request.POST.getlist('cantidad[]'):
                        msj = 'Un problema con las cantidades, favor de revisar'
                        messages.warning(self.request, msj)
                        return self.form_invalid(form)

                    # creando el diccionario de item y limpieza
                    lista_items_eliminar = self.request.POST.getlist('eliminar_item[]')
                    lista_detalle_id = self.request.POST.getlist('detalle_id[]')
                    lista_productos = self.request.POST.getlist('producto[]')
                    lista_cantidad = self.request.POST.getlist('cantidad[]')
                    lista_precio = self.request.POST.getlist('precio[]')
                    lista_subtotal = self.request.POST.getlist('subtotal[]')
                    list_items = []
                    index = 0
                    for id_producto in lista_productos:
                        if id_producto.isnumeric():
                            list_items.append({
                              'id_detalle': lista_detalle_id[index],
                              'id_producto': id_producto,
                              'cantidad': lista_cantidad[index],
                              'precio': lista_precio[index],
                              'subtotal': lista_subtotal[index],
                            })
                        index += 1

                    # guardamos detalles
                    self.crear_detalles_pedido(self.object, list_items)

                    # eliminar items
                    self.eliminar_items(lista_items_eliminar)

                    return super().form_valid(form)
                else:
                    return self.form_invalid(form)
        except Exception as e:
            print(e)
            messages.warning(self.request, 'Ocurrió un error vuelva a intentarlo : {}'.format(e))
            return self.form_invalid(form)

    def crear_detalles_pedido(self, obj_pedido,  list_items):
        for item in list_items:
            if item['id_detalle']:
                det = DetallePedido.objects.get(pk=item['id_detalle'])
            else:
                det = DetallePedido()
            det.pedido = obj_pedido
            det.producto = Producto.objects.get(pk=item['id_producto'])
            det.precio = float(item['precio'].replace(',', '.'))
            det.cantidad = float(item['cantidad'].replace(',', '.'))
            det.total = float(item['subtotal'].replace(',', '.'))
            try:
                det.save()
            except Exception as e:
                print(e)
                mensaje = 'Error al guardar el detalle del pedido | det = {} | Error => {}'.format(str(e), list_items)
                messages.warning(self.request, mensaje)

    def eliminar_items(self, lista_items_eliminar):
        DetallePedido.objects.filter(id__in=lista_items_eliminar).delete()


class PedidoDeleteView(DeleteView):
    template_name = 'abastecimiento/pedido_delete.html'
    model = Pedido

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title_page = "Maestro | Pedidos"
        main_title_content = "Pedidos"
        main_subtitle_content = "Eliminar"
        subtitle_table = "Eliminar pedido"

        context.update({
            'CLASS_MENU_ABASTECIMIENTO': "active",
            'CLASS_SUBMENU_PEDIDOS': "show",
            'CLASS_SUBMENU_PEDIDOS_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table,
        })
        return context

    def get_success_url(self):
        messages.success(self.request, 'Se elimino el registro, {}'.format(self.object.numero))
        return reverse('abastecimiento:pedido_list', kwargs={})


class PedidoShowView(UpdateView):
    template_name = 'abastecimiento/pedido_view_det.html'
    model = Pedido
    form_class = PedidoDetailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title_page = "Maestro | Pedidos"
        main_title_content = "Pedidos"
        main_subtitle_content = "Ver"
        subtitle_table = "Ver detalle pedido"

        context.update({
            'CLASS_MENU_ABASTECIMIENTO': "active",
            'CLASS_SUBMENU_PEDIDOS': "show",
            'CLASS_SUBMENU_PEDIDOS_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table
        })
        return context


class PedidoListPendientesView(ListView):
    template_name = 'abastecimiento/pedido_list_pendientes.html'
    model = Pedido
    paginate_by = 100

    # se usa el decorador para evitar el crf_token
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title_page = "Maestro | Pedidos"
        main_title_content = "Pedidos"
        main_subtitle_content = "List"
        subtitle_table = "Lista pedidos"

        context.update({
            'CLASS_MENU_ABASTECIMIENTO': "active",
            'CLASS_SUBMENU_PEDIDOS': "show",
            'CLASS_SUBMENU_PEDIDOS_PEND_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table,
        })
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                pedidos = Pedido.objects.filter(estado__in=['PENDIENTE', 'ACEPTADO', 'ENVIADO', 'RECIBIDO']
                                                ).order_by('-id')
                for i in pedidos:
                    data.append(i.toJSON())
            elif action == 'recepcionar':
                id = request.POST['id']
                pedido = Pedido.objects.get(pk=id)
                pedido.aceptar_pedido()
                pedido.save()
            elif action == 'enviar_pedido':
                id = request.POST['id']
                pedido = Pedido.objects.get(pk=id)
                pedido.enviar_pedido()
                pedido.save()
            else:
                data['error'] = "no tiene acciones ejecutadas"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
