from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class HomeSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['home', 'item-list', 'all-items', 'men-items',
                    'women-items', 'children-items', 'search-items']

    def location(self, item):
        return reverse(item)



class StaticSitemap(Sitemap):
    priority = 0.9
    changefreq = 'daily'

    def items(self):
        return [
            'login',
            'register',
            'user-cart',
            'checkout',
            'confirm-order',
            'add-coupon',
            'request-refund',
            'favourites',
            'country-cities',
            
            'blog:posts',
            
            'about',
            'contact',
            'reset_password',
            'password_reset_done',
            'password_reset_complete',
        ]

    def location(self, item):
        return reverse(item)
