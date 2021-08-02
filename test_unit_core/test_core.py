from io import BytesIO

from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile

from store.models import Category, Publisher, BookAuthor, BookGenre, Book, Magazine, CategoryDiscount
from django.contrib.auth.models import User, Permission


def create_user(username, password, email):
    user = User.objects.create_user(username=username)
    user.set_password(password)
    user.email = email
    user.save()


def create_product_for_test(count):
    number = count + 1
    [Category.objects.create(name=category_item) for category_item in ('Books', 'Magazine')]
    [Publisher.objects.create(name=publisher_item) for publisher_item in range(1, number)]
    [BookAuthor.objects.create(name=author_item) for author_item in range(1, number)]
    [BookGenre.objects.create(name=genre_item) for genre_item in range(1, number)]
    [CategoryDiscount.objects.create(category=Category.objects.get(pk=discount_item), discount=10, active=True) for
     discount_item in range(1, 3)]

    image = Image.new('RGBA', size=(50, 50), color=(256, 0, 0))
    image_file = BytesIO(image.tobytes())
    file = InMemoryUploadedFile(image_file, None, 'test.jpg', 'image/jpg', 1024, None)

    for product_item in range(1, number):
        Book.objects.create(category=Category.objects.get(pk=1), name='book_%s' % product_item,
                            publisher=Publisher.objects.get(pk=product_item),
                            price=product_item * 10, Discounts=0, hard_cover='+', pages=5 * product_item,
                            pub_year=2000 + product_item, size='240x165', image=file
                            )

        Book.objects.get(pk=product_item).author.add(BookAuthor.objects.get(pk=product_item))
        Book.objects.get(pk=product_item).genre.add(BookGenre.objects.get(pk=product_item))
    for product_item in range(1, number):
        Magazine.objects.create(category=Category.objects.get(pk=2), name='magazine_%s' % product_item,
                                publisher=Publisher.objects.get(pk=product_item),
                                price=product_item * 10, Discounts=0, numb=product_item, numb_in_year=product_item,
                                subs_price=20 * product_item, pages=5 * product_item,
                                pub_year=2000 + product_item, size='240x165', image=file)



