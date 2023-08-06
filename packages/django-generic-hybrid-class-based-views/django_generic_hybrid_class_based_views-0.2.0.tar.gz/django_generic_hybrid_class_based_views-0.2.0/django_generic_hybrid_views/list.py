from typing import MutableMapping
from django.views.generic.list import MultipleObjectTemplateResponseMixin, BaseListView
from django_generic_json_views.base import JsonResponseMixin

class HybridListView(JsonResponseMixin, MultipleObjectTemplateResponseMixin, BaseListView):
    def render_to_response(self, context):
        if self.request.GET.get('format') == 'json':
            return self.render_to_json_response(context=context)
        else:
            super().render_to_response(context)