from django.views.generic import TemplateView
from . import models


class TestView(TemplateView):
	template_name = 'test.html'

	def get_context_data(self, *args, **kwargs):
		return {
			'test': models.Test.objects.get(pk=kwargs.get('pk'))
		}
