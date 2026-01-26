from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Item

class ItemSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Item.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return ['values:landing', 'values:item_list', 'values:trade_calculator']

    def location(self, item):
        return reverse(item)

sitemaps = {
    'items': ItemSitemap,
    'static': StaticViewSitemap,
}
