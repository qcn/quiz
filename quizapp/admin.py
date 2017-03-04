from django.contrib import admin
from .models import Quiz, MCQuestion, SAQuestion, MCAnswer

# Register your models here.

admin.site.register(Quiz)
admin.site.register(MCQuestion)
admin.site.register(SAQuestion)
admin.site.register(MCAnswer)
