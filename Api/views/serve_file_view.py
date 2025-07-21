# views.py
import os
from urllib.parse import unquote
from django.http import FileResponse, Http404
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils._os import safe_join


@xframe_options_exempt
def serve_protected_media(request, subpath):
    """
    Vista genérica para servir archivos de MEDIA protegidos, compatibles con iframe.
    """

    # Decodifica URL por si contiene espacios o caracteres especiales
    decoded_path = unquote(subpath)

    try:
        # Une de forma segura para evitar path traversal (../../etc/passwd)
        full_path = safe_join(settings.MEDIA_ROOT, decoded_path)
    except ValueError:
        raise Http404("Ruta no permitida")

    if not os.path.exists(full_path):
        raise Http404("Archivo no encontrado")

    return FileResponse(open(full_path, 'rb'))
