import json
from django.db import connection

from django.shortcuts import render

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title_page = "Inicio | Dashboard"
        main_title_content = "Dashboard"
        title="Usuarios del sistema"
        main_subtitle_content = ""
        subtitle_table = ""

        context.update({
            'CLASS_MENU_DASHBOARD': "menu-open",
            'CLASS_SUBMENU_DASHBOARD': "active",
            'CLASS_SUBMENU_DASHBOARD_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'title':title,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table,
            'monto_total_ventas': self.busca_monto_total_ventas(),
            'cant_total_ventas': self.busca_cant_total_ventas(),
            'cant_total_ventas': self.busca_cant_total_ventas(),
            'cantidad_cliente': self.cantidadcliente(),
            'cantidad_proveedor':self.cantidadproveedor(),
            'cantidad_empleado':self.cantidadempleado(),
            'cantidad_vendedor':self.cantidadvendedores(),
            'cantidad_administrador':self.cantidadadministrador(),
            'producto_mas_vendidos':self.producto_mas_vendidos(),
            'precio_maximo': self.busca_precio_maximo(),
            'precio_minimo': self.busca_precio_minimo(),
            'evolucion_ventas': self.busca_evolucion_ventas(),
            'cant_item_x_categorias': self.busca_cant_item_x_categorias(),
        })
        return context

    # Se cuenta la cantidad de Clientes en el sistema    
    def cantidadcliente(self):
        try:
            cursor= connection.cursor()
            cursor.execute(
                """
                select count(*) from users_user 
                where cargo ="Cliente";
                """
            )
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print("Error: {}".format(e))

    # Se Cuenta la cantidad de proveedores que hay en el sistema        
    def cantidadproveedor(self):
        try:
            cursor= connection.cursor()
            cursor.execute(
                """
                select count(*) from users_user 
                where cargo ="Proveedor";
                """
            )
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print("Error: {}".format(e))
    # Se cuenta la cantidad total de empleados que hay en el sistema

    def cantidadempleado(self):
        try:
            cursor= connection.cursor()
            cursor.execute(
                """
                select count(*) from users_user 
                where cargo ="Empleado";
                """
            )
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print("Error: {}".format(e))
    # Se cuenta la cantidad total de vendedores en el sistema.
    def cantidadvendedores(self):
        try:
            cursor= connection.cursor()
            cursor.execute(
                """
                select count(*) from users_user 
                where cargo ="Venta";
                """
            )
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print("Error: {}".format(e))
    #Se cuenta la cantidad total de admininistradores del sistema.
    def cantidadadministrador(self):
        try:
            cursor= connection.cursor()
            cursor.execute(
                """
                select count(*) from users_user 
                where cargo ="Administrador";
                """
            )
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print("Error: {}".format(e))

    def busca_monto_total_ventas(self):
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                select sum(precio) as "suma_total" from cmp_venta cv
                """
            )
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print("Error: {}".format(e))

    def busca_cant_total_ventas(self):
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                select count() as cant_ventas from cmp_venta cv
                """
            )
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print("Error: {}".format(e))

    def busca_precio_maximo(self):
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                select max(precio) as precio_maximo from cmp_venta cv
                """
            )
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print("Error: {}".format(e))

    def busca_precio_minimo(self):
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                select min(precio) as precio_minimo from cmp_venta cv
                """
            )
            row = cursor.fetchone()
            return row[0]
        except Exception as e:
            print("Error: {}".format(e))

    def busca_evolucion_ventas(self):
        dict_meses = {
            '01': 0,
            '02': 0,
            '03': 0,
            '04': 0,
            '05': 0,
            '06': 0,
            '07': 0,
            '08': 0,
            '09': 0,
            '10': 0,
            '11': 0,
            '12': 0
        }

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT strftime('%m', v.fc) AS mes,
                           SUM(v.precio) AS total
                    FROM cmp_venta as v;
                """
            )
            for row in cursor.fetchall():
                mes = row[0]    # mes
                dict_meses[mes] = row[1]    # total
            return json.dumps(dict_meses)
        except Exception as e:
            print("Error: {}".format(e))

    def busca_cant_item_x_categorias(self):
        dict_categorias = {}
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                select pc.Nombre ,sum(producto_carritoproducto.cantidad) 
                from 
                cmp_venta,producto_carritoproducto,producto_producto, producto_categoria pc
                where  cmp_venta.carrito_id =producto_carritoproducto.carrito_id 
                and producto_producto.codigo = producto_carritoproducto.producto_id
                and pc.id = producto_producto.Categoria_id 
                group by producto_producto.Nombre  
                order by sum(producto_carritoproducto.cantidad) desc
                limit 3
                ;
                
                """
            )
            for row in cursor.fetchall():
                dict_categorias.update({row[0]: row[1]})
            return json.dumps(dict_categorias)
        except Exception as e:
            print("Error: {}".format(e))
    
    
    def producto_mas_vendidos(self):
        dict_producto = {}
        try:
            cursor= connection.cursor()
            cursor.execute(
                """
                select producto_producto.Nombre,sum(producto_carritoproducto.cantidad) 
                from 
                cmp_venta,producto_carritoproducto,producto_producto
                where  cmp_venta.carrito_id =producto_carritoproducto.carrito_id 
                and producto_producto.codigo = producto_carritoproducto.producto_id 
                group by producto_producto.Nombre  
                order by sum(producto_carritoproducto.cantidad) desc
                limit 3
                ;
                """
            )
            for row in cursor.fetchall():
                dict_producto.update({row[0]: row[1]})
            return json.dumps(dict_producto) 
        except Exception as e:
            print("Error: {}".format(e))
