from django.contrib.auth.models import Permission

PERMISSION_ON_SITE = {'moderator': ('store.change_product', 'store.view_product', 'store.delete_product',),
                      'user': ('store.view_product',),
                      }


def permission_for_user(perm):
    try:
        app_label, codename = perm.split('.', 1)
    except IndexError:
        raise AttributeError(
            "The format of identifier string permission (perm) is wrong. "
            "It should be in 'app_label.codename'."
        )
    else:
        permission = Permission.objects.get(content_type__app_label=app_label, codename=codename)
        return permission
