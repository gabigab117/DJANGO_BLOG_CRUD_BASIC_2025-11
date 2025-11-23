from django.contrib import admin
from .models import Blogpost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_on", "created_on", "last_update",)
    list_editable = ("published_on",)

admin.site.register(Blogpost, BlogPostAdmin)
# Register your models here.
