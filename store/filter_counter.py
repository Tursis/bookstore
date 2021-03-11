from .models import Product, Book, Magazine, BookGenre, BookAuthor, Category, Publisher


def counter(request):
    for filter_list in Category.objects.all(), BookGenre.objects.all(), BookAuthor.objects.all(), Publisher.objects.all():
        for item in filter_list:
            item.counter(request.GET)

    # for item in request.GET:
    #
    #     print(item)
    #     if item == 'category':
    #         queryset = queryset.filter(Q(category__in=request.GET.getlist('category'))).distinct()
    #     if item == 'book__author':
    #         queryset = queryset.filter(Q(book__author__in=request.GET.getlist('book__author'))).distinct()
    #     if item == 'book__genre':
    #         queryset = queryset.filter(Q(book__genre__in=request.GET.getlist('book__genre'))).distinct()
    #     print(queryset.count())


def update_model_counter(request, model):
    model_dict = {}
    for item in model:
        model_dict[item] = item.counter(request.GET)
    return model_dict

