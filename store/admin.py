from django.contrib import admin
from .models import Book, Magazine, BookGenre,BookAuthor
from orders.models import Order, Purchase
# Register your models here.

admin.site.register(Book)
admin.site.register(BookGenre)
admin.site.register(BookAuthor)
admin.site.register(Magazine)
admin.site.register(Order)
admin.site.register(Purchase)

