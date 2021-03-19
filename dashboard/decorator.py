from .models import ViewStatistics


def counter(function_to_decorate):
    def decorator(self, request, *args, **kwargs):
        print(request.GET)
        print('Decorator')
        return function_to_decorate(self, request, *args, **kwargs)
    return decorator
