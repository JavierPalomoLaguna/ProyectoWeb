from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            {'url': '/', 'name': 'index'},
            {'url': '/servicios/', 'name': 'servicios'},
            {'url': '/tienda/', 'name': 'tienda'},
            {'url': '/contacto/', 'name': 'contacto'},
            {'url': '/blog/', 'name': 'blog'},
        ]

    def location(self, item):
        return item['url']


class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        try:
            return Post.objects.all()
        except:
            return []

    def lastmod(self, post):
        return post.updated
    
    def location(self, post):
        return reverse('post_detail', args=[post.id])