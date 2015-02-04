from django.contrib import admin
from main.models import *

class EntryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'author', 'pub_date', 'title']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register(Title)
admin.site.register(Title_Redirect)
admin.site.register(Entry, EntryAdmin)