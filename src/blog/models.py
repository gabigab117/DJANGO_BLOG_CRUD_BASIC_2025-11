from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Blogpost(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Titre")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(blank=True, null=True)
    published_on = models.BooleanField(default=False, verbose_name="Publié")
    content = models.TextField(verbose_name="Contenu")
    thumbnail = models.ImageField(verbose_name="Image", null=True, blank=True, upload_to="blog")

    class Meta:
        ordering = ['-last_update']
        verbose_name = "Article"

    def __str__(self):
        return self.title

    def save (self, *args, **kwargs):
        if not self.slug :
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    @property
    def author_or_default(self):
        return self.author.username if self.author else "L'auteur est inconnu"

    def get_absolute_url(self):
        return reverse('blog:home')