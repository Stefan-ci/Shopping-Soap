from django.conf import settings


def site_name(reqest):
    """
        Displaying site name dynamically. 
        No need to hardcode it. Change it simply in settings.
    """
    _site_name = settings.SITE_NAME
    context = {'site_name': _site_name}
    return context
    