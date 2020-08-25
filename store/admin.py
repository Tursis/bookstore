from django.contrib import admin
from .models import Book, Magazine, BookGenre, BookAuthor
from profile.models import Profile
from orders.models import Order, Purchase


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'last_name', 'surname', 'birth_date')
    list_filter = ['user']
    search_fields = ['user']
    radio_fields = {'gender': admin.VERTICAL}



class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class MagazineAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class BookGenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('genre',)}


class BookAuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Magazine, MagazineAdmin)
admin.site.register(BookGenre, BookGenreAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(Order)
admin.site.register(Purchase)
