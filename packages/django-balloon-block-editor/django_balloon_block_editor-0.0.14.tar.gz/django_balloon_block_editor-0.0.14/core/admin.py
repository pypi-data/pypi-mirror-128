from django.contrib import admin
from . import models


@admin.register(models.Test)
class TestAdmin(admin.ModelAdmin):
	pass
