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
        main_subtitle_content = ""
        subtitle_table = ""

        context.update({
            'CLASS_MENU_DASHBOARD': "menu-open",
            'CLASS_SUBMENU_DASHBOARD': "active",
            'CLASS_SUBMENU_DASHBOARD_LIST': "active",
            'title_page': title_page,
            'main_title_content': main_title_content,
            'main_subtitle_content': main_subtitle_content,
            'subtitle_table': subtitle_table,
            'monto_total_ventas': self.busca_monto_total_ventas(),
            'cant_total_ventas': self.busca_cant_total_ventas(),
            'cant_total_ventas': self.busca_cant_total_ventas(),
            'precio_maximo': self.busca_precio_maximo(),
            'precio_minimo': self.busca_precio_minimo(),
            'evolucion_ventas': self.busca_evolucion_ventas(),
            'cant_item_x_categorias': self.busca_cant_item_x_categorias(),
        })
        return context

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
                select pc.Nombre as "categoria", count(*) as cantidad
                from producto_producto as p
                inner join producto_categoria pc on p.Categoria_id = pc.id
                group by p.Categoria_id;
                """
            )
            for row in cursor.fetchall():
                dict_categorias.update({row[0]: row[1]})
            return json.dumps(dict_categorias)
        except Exception as e:
            print("Error: {}".format(e))
