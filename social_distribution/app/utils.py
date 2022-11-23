from django.conf import settings


def url_is_local(url):
    return url.startswith(settings.HOSTNAME)
