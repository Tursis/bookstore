from django.contrib import admin
from .models import Product, Book, Magazine, BookGenre, BookAuthor, Publisher, Category, ProductComment
from profile.models import Profile, Token
from orders.models import Order, Purchase
from cart.models import Cart


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'last_name', 'surname', 'birth_date')
    list_filter = ['user']
    search_fields = ['user']
    radio_fields = {'gender': admin.VERTICAL}


class СartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity',)
    list_filter = ['user']
    search_fields = ['user']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class MagazineAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class BookGenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class BookAuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Magazine, MagazineAdmin)
admin.site.register(BookGenre, BookGenreAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, СartAdmin)
admin.site.register(Purchase)
admin.site.register(ProductComment)
admin.site.register(Token)
