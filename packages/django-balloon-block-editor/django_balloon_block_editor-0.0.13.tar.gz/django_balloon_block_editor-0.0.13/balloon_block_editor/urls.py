from django.urls import include, path
from . import views

urlpatterns = [
	path('image-upload/', views.BalloonBlockEditorImageUploadView.as_view(), name='balloon-block-editor-image-upload'),
]
