from django.contrib import admin
from .models.architecture import ArchitectureModel
from .models.study import InteractionModel, ScenarioModel

# Register your models here.
admin.site.register(ArchitectureModel)
admin.site.register(InteractionModel)
admin.site.register(ScenarioModel)
