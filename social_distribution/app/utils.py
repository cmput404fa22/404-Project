from django.conf import settings


def url_is_local(url):
    return url.startswith(settings.HOSTNAME)


def clean_url(url):
    if url[-1] == "/":
        return url[:-1]
    return url
