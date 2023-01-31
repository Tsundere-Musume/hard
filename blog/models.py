from django.db import models
from django_editorjs import EditorJsField


class Post(models.Model):
    title = models.CharField(max_length=60)
    body = EditorJsField(
        editorjs_config={
            "tools": {
                "Link": {"config": {"endpoint": "/blog/linkfetching/"}},
                "Image": {
                    "config": {
                        "endpoints": {"byFile": "/blog/uploadImage/", "byUrl": "/blog/uploadImage/"},
                    }
                },
            }
        }
    )
