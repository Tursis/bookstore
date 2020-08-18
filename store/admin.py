from django.contrib import admin
from .models import Book, Magazine, BookGenre, BookAuthor
from accounts.models import Profile
from orders.models import Order, Purchase


# Register your models here.



class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class MagazineAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class BookGenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('genre',)}


class BookAuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Book, BookAdmin)
admin.site.register(Magazine, MagazineAdmin)
admin.site.register(BookGenre, BookGenreAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(Purchase)
