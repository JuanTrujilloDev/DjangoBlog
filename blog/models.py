from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField(max_length=280)
    date_posted = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        super(Post, self).save()
        self.slug = slugify(self.title)
        self.slug += "-" + slugify(self.pk) 
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/post/{self.slug}"


    def countPosts():
        qs = Post.objects.all()
        counter = 0
        for post in qs:
            counter += 1

        return counter
