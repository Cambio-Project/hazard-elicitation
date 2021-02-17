from django.db import models
from rest_framework import serializers, viewsets


class ArchitectureModel(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    content = models.CharField(max_length=1024**2, null=False, blank=False)

    def __str__(self):
        return f'{self.name}'


class ArchitectureModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArchitectureModel
        fields = ('id', 'name', 'content')


class ArchitectureModelViewSet(viewsets.ModelViewSet):
    serializer_class = ArchitectureModelSerializer

    def get_queryset(self):
        queryset = ArchitectureModel.objects.all().order_by('id')
        name = self.request.query_params.get('name')

        if name:
            queryset = queryset.filter(name=name).order_by('id')

        return queryset
