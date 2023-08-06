from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from . import models


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class BalloonBlockEditorImageUploadView(View):
	def dispatch(self, *args, **kwargs):
		upload = models.ImageUpload.objects.create(
			image=self.request.FILES['upload']
		)
		return JsonResponse({'url': upload.image.url})
