# django-balloon-block-editor

## Installation

1. `pip install django-balloon-block-editor`
2. In `settings.py`, add `balloon_block_editor` to `INSTALLED_APPS`
3. In `urls.py`, add `path('balloon-block-editor/', include('balloon_block_editor.urls'))` to your `urlpatterns`

## Usage

In `models.py`:

```
from balloon_block_editor.fields import BalloonBlockEditorField
from django.db import models


class Test(models.Model):
    content = BalloonBlockEditorField()
```

