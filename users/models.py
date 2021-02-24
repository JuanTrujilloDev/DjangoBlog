from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image
# Create your models here.

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(default="Hello, I'm a new user!", blank=True, max_length=120)
    birthday = models.DateField(blank=True, null=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        user = self.user
        self.slug = slugify(user.username)
        super(Profile, self).save(*args, **kwargs)

        image = Image.open(self.image.path)

        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)



    def get_absolute_url(self):
       return f"/profile/{self.slug}"

    def __str__(self):
        return f'{self.user.username} Profile'

    def countUsers():
        qs = User.objects.all()
        counter = 0
        for users in qs:
            if users.is_staff:
                continue
            counter += 1

        return counter
