import json
import zipfile

from django.http import HttpResponse

from architecture_extraction_backend.arch_models.architecture import Architecture
from architecture_extraction_backend.arch_models.jaeger_trace import JaegerTrace
from architecture_extraction_backend.arch_models.misim_model import MiSimModel
from architecture_extraction_backend.arch_models.zipkin_trace import ZipkinTrace
from architecture_extraction_backend.controllers.exporter import Exporter
from architecture_extraction_backend.models import ArchitectureModel
from util.log import error


def upload(request):
    try:
        model = None
        filename = request.FILES['file']
        content = json.load(filename)

        try:
            if isinstance(content, dict):
                if content.get('microservices', False):
                    model = MiSimModel(content)
                elif content.get('data', False):
                    model = JaegerTrace(content)
            elif isinstance(content, list):
                model = ZipkinTrace(content)

        except BaseException as e:
            error(e)
            return HttpResponse('Processing error', status=500)

        if model:
            arch = Architecture(model)
            export = Exporter.export_architecture(arch, 'JSON')

            try:
                ArchitectureModel.objects.create(name=filename, content=export)

            except BaseException as e:
                error(e)
                return HttpResponse('File to big', status=500)

        else:
            return HttpResponse('Wrong format', status=500)

        return HttpResponse(status=200)

    except BaseException as e:
        error(e)
        return HttpResponse('Processing error', status=500)


def export_arch(request):
    try:
        response = HttpResponse(content_type='application/zip')
        archive = zipfile.ZipFile(response, 'w')

        for obj in ArchitectureModel.objects.all():
            archive.writestr(obj.name, obj.content)

        response['Content-Disposition'] = 'attachment; filename={}'.format('export.zip')
        return response

    except BaseException as e:
        error(e)
        return HttpResponse('Processing error', status=500)


def import_arch(request):
    return HttpResponse('', status=200)
