from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django_generic_json_views.base import JsonResponseMixin

class HybridDetailView(JsonResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
    def render_to_response(self, context):
        if self.request.GET.get('format') == 'json':
            return self.render_to_json_response(context=context)
        else:
            return super().render_to_response(context)
