from django.db import models
from django.conf import settings
from django_editorjs import EditorJsField


class Post(models.Model):
    title = models.CharField(max_length=60)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Likes", related_name="liked_posts"
    )
    body = EditorJsField(
        editorjs_config={
            "tools": {
                "Link": {"config": {"endpoint": "/blog/linkfetching/"}},
                "Image": {
                    "config": {
                        "endpoints": {
                            "byFile": "/blog/uploadImage/",
                            "byUrl": "/blog/uploadImage/",
                        },
                    }
                },
            }
        }
    )

    def __str__(self):
        return f"{self.title}({self.id})"


class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username}  liked {self.post.title}({self.post.id})."
