from archex_backend.models.architecture import Architecture


class Exporter:
    @staticmethod
    def export_architecture(arch: Architecture, export_type: str, pretty: bool = False):
        # JavaScript
        if export_type == 'JS':
            return 'let graph=' + arch.d3_graph(pretty) + ';'
        # Json
        else:
            return arch.d3_graph(pretty)
