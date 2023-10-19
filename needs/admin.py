from django.contrib import admin

from .models import User, Need, Action

admin.site.register(User)
admin.site.register(Need)
admin.site.register(Action)
