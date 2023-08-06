from rest_framework import viewsets
from rest_framework.response import Response


class VersionMixin(viewsets.ModelViewSet):
    def _json_by_version(self, obj=None) -> dict:
        instance = obj or self.get_object()
        version = self.request.query_params.get('version')
        json_field_name = self.request.query_params.get('json_name', 'json')
        compare_with_version = self.request.query_params.get('compare_with_version')
        instance_json = instance.get_json_by_version(version, json_field_name, compare_with_version)
        # добавляем версии связанных моделей
        instance.add_version_for_rel_versioned_obj(instance_json)
        instance_json['version_list'] = instance.version_list
        return instance_json

    def retrieve(self, request, *args, **kwargs):
        return Response(self._json_by_version())
