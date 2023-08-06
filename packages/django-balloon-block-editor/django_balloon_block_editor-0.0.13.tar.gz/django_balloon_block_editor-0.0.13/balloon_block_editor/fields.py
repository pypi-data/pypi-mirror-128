from django.db import models
from django.forms import Textarea
from django.template.loader import render_to_string


class BalloonBlockEditorWidget(Textarea):
	def render(self, name, value, attrs = {}, **kwargs):
		return render_to_string('balloon_block_editor/widget.html', {
			'name': name,
			'value': value,
		})


class BalloonBlockEditorField(models.TextField):
	def formfield(self, **kwargs):
		kwargs['widget'] = BalloonBlockEditorWidget
		return super().formfield(**kwargs)
