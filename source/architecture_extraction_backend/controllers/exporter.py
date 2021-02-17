from architecture_extraction_backend.arch_models.architecture import Architecture


class Exporter:
    @staticmethod
    def export_architecture(arch: Architecture, export_type: str, pretty: bool = False):
        # JavaScript
        if export_type == 'js':
            return 'const graph=' + arch.export(pretty) + ';'
        # Json
        else:
            return arch.export(pretty)
