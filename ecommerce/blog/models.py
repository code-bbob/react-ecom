from django.db import models
from django.utils import timezone
import uuid
from ckeditor.fields import RichTextField

class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    content = RichTextField()
    image = models.ImageField(upload_to='blog/images', default='')
    date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=20, default='Technology')

    def __str__(self):
        return self.title
