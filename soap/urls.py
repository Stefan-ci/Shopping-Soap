from products.models import Soap
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from django.contrib.sitemaps import GenericSitemap
from soap.sitemaps import HomeSitemap, StaticSitemap

items_dict = {
    'queryset': Soap.objects.filter(is_public=True, is_deleted=False)
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    path('', include('website.urls')),
    path('blog/', include('blog.urls', namespace='blog')),

    path('robots.txt/', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain')),
    
    
    path('sitemap.xml/', sitemap,
        {
            'sitemaps': {
                'home': HomeSitemap,
                'static': StaticSitemap,
                'item-detail': GenericSitemap(items_dict, priority=1.0),
            },
        },
        name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += static(settings.STATIC_URL, serve, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, serve, document_root=settings.MEDIA_ROOT)
