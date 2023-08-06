from django.db import models
from balloon_block_editor.fields import BalloonBlockEditorField


class Test(models.Model):
	content = BalloonBlockEditorField()
	content2 = BalloonBlockEditorField()
