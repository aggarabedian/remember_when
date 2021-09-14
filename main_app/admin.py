from django.contrib import admin
from .models import Journal, Memory, Photo, Album

# Register your models here.
admin.site.register(Journal)
admin.site.register(Memory)
admin.site.register(Album)
admin.site.register(Photo)