from .models import Product, Book, Magazine, BookGenre, BookAuthor, Category, Publisher


def product_filter_counter(request):
    for model_list in Category.objects.all(), BookGenre.objects.all(), BookAuthor.objects.all(), Publisher.objects.all():
        for model in model_list:
            model.counter(request.GET)


def update_model_counter(request, model):
    model_dict = {}
    for model_item in model:
        model_dict[model_item] = model_item.counter(request.GET)
    return model_dict

