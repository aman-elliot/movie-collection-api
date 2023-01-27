from django.contrib import admin

from .models import Collection,Movies,Genre,GenreStats

admin.site.register(Collection)
admin.site.register(Movies)
admin.site.register(Genre)
admin.site.register(GenreStats)

