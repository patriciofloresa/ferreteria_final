import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from .models import venta
from django.template import Context
from django.utils import timezone
from apps.producto.models import *

def link_callback(uri, rel):
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path

def reportes_compras(request):
        template_path="reportes/compras_print_all.html"
        from django.utils import timezone
        today = timezone.now()

        compras = venta.objects.all()
        context ={
            'obj':compras,
            'today': today,
            'request':request
        }
        response =HttpResponse(content_type='application/pdf')
        response['Context-Disposition']='inline:filename="todas_ventas.pdf"'
        template=get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response






