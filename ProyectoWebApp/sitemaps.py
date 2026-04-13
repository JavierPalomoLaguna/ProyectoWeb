from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'
    
    def get_urls(self, site=None, **kwargs):
        site = type('Site', (), {
            'domain': 'www.codigovivostudio.cloud'
        })()
        return super().get_urls(site=site, **kwargs)

    def items(self):
        return [
            'index',
            'servicios',
            'tienda',
            'contacto',
            'blog',
        ]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'
    protocol = 'https'
    
    def get_urls(self, site=None, **kwargs):
        site = type('Site', (), {
            'domain': 'www.codigovivostudio.cloud'
        })()
        return super().get_urls(site=site, **kwargs)

    def items(self):
        return Post.objects.all().order_by('-updated')

    def lastmod(self, post):
        return post.updated
    
    def location(self, post):
        return reverse('post_detail', args=[post.id])